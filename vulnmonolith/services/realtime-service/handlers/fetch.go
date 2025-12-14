package handlers

import (
	"crypto/tls"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
)

// FetchHandler handles URL fetching (SSRF)
// VULNERABILITY: Server-Side Request Forgery
// CWE-918: SSRF
func FetchHandler(w http.ResponseWriter, r *http.Request) {
	targetURL := r.URL.Query().Get("url")

	// VULNERABILITY: No URL validation - SSRF
	// Attack: url=http://169.254.169.254/latest/meta-data/
	// Attack: url=http://localhost:6379/

	// VULNERABILITY: Insecure TLS configuration
	client := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{
				InsecureSkipVerify: true, // VULNERABILITY: Skipping TLS verification
			},
		},
	}

	resp, err := client.Get(targetURL)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	w.Write(body)
}

// ProxyHandler acts as an open proxy
// VULNERABILITY: Open proxy / SSRF
func ProxyHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		URL     string            `json:"url"`
		Method  string            `json:"method"`
		Headers map[string]string `json:"headers"`
		Body    string            `json:"body"`
	}

	json.NewDecoder(r.Body).Decode(&req)

	// VULNERABILITY: Open proxy to any URL
	proxyReq, _ := http.NewRequest(req.Method, req.URL, nil)

	// VULNERABILITY: Forwarding arbitrary headers
	for k, v := range req.Headers {
		proxyReq.Header.Set(k, v)
	}

	client := &http.Client{}
	resp, err := client.Do(proxyReq)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)

	// VULNERABILITY: Response headers forwarded
	for k, v := range resp.Header {
		w.Header()[k] = v
	}

	w.WriteHeader(resp.StatusCode)
	w.Write(body)
}

// WebhookHandler handles incoming webhooks
// VULNERABILITY: SSRF via webhook
func WebhookHandler(w http.ResponseWriter, r *http.Request) {
	callbackURL := r.URL.Query().Get("callback")

	// VULNERABILITY: SSRF via callback
	// Attacker can make server call internal URLs
	resp, err := http.Get(callbackURL)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	w.Write([]byte("Webhook processed"))
}

// SafeFetchHandler attempts to validate URL (but fails)
// VULNERABILITY: Insufficient URL validation
func SafeFetchHandler(w http.ResponseWriter, r *http.Request) {
	targetURL := r.URL.Query().Get("url")

	parsed, err := url.Parse(targetURL)
	if err != nil {
		http.Error(w, "Invalid URL", http.StatusBadRequest)
		return
	}

	// VULNERABILITY: Bypass with http://evil.com@localhost/
	// VULNERABILITY: Bypass with DNS rebinding
	// VULNERABILITY: Bypass with IP address variations (0x7f.0.0.1, 127.1, etc.)
	blocklist := []string{"localhost", "127.0.0.1", "0.0.0.0"}

	for _, blocked := range blocklist {
		if parsed.Hostname() == blocked {
			http.Error(w, "Blocked host", http.StatusForbidden)
			return
		}
	}

	// Still vulnerable - many bypasses possible
	resp, _ := http.Get(targetURL)
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	w.Write(body)
}

// RedirectHandler demonstrates open redirect
// VULNERABILITY: Open Redirect
func RedirectHandler(w http.ResponseWriter, r *http.Request) {
	redirectURL := r.URL.Query().Get("url")

	// VULNERABILITY: No validation on redirect URL
	http.Redirect(w, r, redirectURL, http.StatusFound)
}

// ImageProxyHandler proxies images
// VULNERABILITY: SSRF via image proxy
func ImageProxyHandler(w http.ResponseWriter, r *http.Request) {
	imageURL := r.URL.Query().Get("src")

	resp, err := http.Get(imageURL)
	if err != nil {
		http.Error(w, "Failed to fetch image", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	// VULNERABILITY: No content-type validation
	w.Header().Set("Content-Type", resp.Header.Get("Content-Type"))

	body, _ := ioutil.ReadAll(resp.Body)
	w.Write(body)
}
