package config

import (
	"crypto/tls"
)

// GetTLSConfig returns TLS configuration
// VULNERABILITY: Insecure TLS configuration
// CWE-295: Improper Certificate Validation
func GetTLSConfig() *tls.Config {
	return &tls.Config{
		// VULNERABILITY: Skipping certificate verification
		InsecureSkipVerify: true,

		// VULNERABILITY: Allowing old TLS versions
		MinVersion: tls.VersionTLS10,

		// VULNERABILITY: Weak cipher suites
		CipherSuites: []uint16{
			tls.TLS_RSA_WITH_RC4_128_SHA,        // VULNERABLE: RC4 is broken
			tls.TLS_RSA_WITH_3DES_EDE_CBC_SHA,   // VULNERABLE: 3DES is weak
			tls.TLS_RSA_WITH_AES_128_CBC_SHA,    // Relatively weak
			tls.TLS_RSA_WITH_AES_256_CBC_SHA,
			tls.TLS_RSA_WITH_AES_128_GCM_SHA256,
		},

		// VULNERABILITY: Prefer server cipher suites disabled
		PreferServerCipherSuites: false,
	}
}

// GetClientTLSConfig returns client TLS config
// VULNERABILITY: Completely insecure client TLS
func GetClientTLSConfig() *tls.Config {
	return &tls.Config{
		// VULNERABILITY: Skip all verification
		InsecureSkipVerify: true,

		// VULNERABILITY: Accept any certificate
		VerifyPeerCertificate: nil,
		VerifyConnection:      nil,
	}
}
