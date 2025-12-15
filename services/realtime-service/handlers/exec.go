package handlers

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"strings"
)

// ExecHandler handles command execution requests
// VULNERABILITY: Command Injection
// CWE-78: OS Command Injection
func ExecHandler(w http.ResponseWriter, r *http.Request) {
	command := r.URL.Query().Get("cmd")

	if command == "" {
		http.Error(w, "Missing cmd parameter", http.StatusBadRequest)
		return
	}

	// VULNERABILITY: Direct command execution with user input
	cmd := exec.Command("sh", "-c", command)
	output, err := cmd.CombinedOutput()

	if err != nil {
		// VULNERABILITY: Error details exposed
		http.Error(w, fmt.Sprintf("Execution error: %v\nOutput: %s", err, output), http.StatusInternalServerError)
		return
	}

	w.Write(output)
}

// PingHandler handles ping requests
// VULNERABILITY: Command Injection via ping
func PingHandler(w http.ResponseWriter, r *http.Request) {
	host := r.URL.Query().Get("host")

	// VULNERABILITY: User input in command
	// Attack: host=127.0.0.1; cat /etc/passwd
	cmd := exec.Command("ping", "-c", "4", host)
	output, _ := cmd.CombinedOutput()

	w.Write(output)
}

// ProcessFileHandler handles file processing
// VULNERABILITY: Command Injection via filename
func ProcessFileHandler(w http.ResponseWriter, r *http.Request) {
	filename := r.URL.Query().Get("file")
	operation := r.URL.Query().Get("op")

	// VULNERABILITY: User input in shell command
	// Attack: file=test.txt; rm -rf /
	cmdStr := fmt.Sprintf("%s %s", operation, filename)
	cmd := exec.Command("sh", "-c", cmdStr)

	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err := cmd.Run()
	if err != nil {
		http.Error(w, stderr.String(), http.StatusInternalServerError)
		return
	}

	w.Write(stdout.Bytes())
}

// GitCloneHandler handles git operations
// VULNERABILITY: Command Injection via repository URL
func GitCloneHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		RepoURL string `json:"repo_url"`
		Branch  string `json:"branch"`
	}

	json.NewDecoder(r.Body).Decode(&req)

	// VULNERABILITY: Command injection via repo URL
	// Attack: repo_url=https://github.com/test/repo; whoami
	cmd := exec.Command("git", "clone", "--branch", req.Branch, req.RepoURL)
	output, err := cmd.CombinedOutput()

	if err != nil {
		http.Error(w, string(output), http.StatusInternalServerError)
		return
	}

	w.Write([]byte("Clone successful"))
}

// EnvExecHandler executes commands with environment variables
// VULNERABILITY: Environment variable injection
func EnvExecHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Command string            `json:"command"`
		Env     map[string]string `json:"env"`
	}

	json.NewDecoder(r.Body).Decode(&req)

	cmd := exec.Command("sh", "-c", req.Command)

	// VULNERABILITY: User-controlled environment variables
	for k, v := range req.Env {
		cmd.Env = append(cmd.Env, fmt.Sprintf("%s=%s", k, v))
	}

	// Add existing environment
	cmd.Env = append(cmd.Env, os.Environ()...)

	output, _ := cmd.CombinedOutput()
	w.Write(output)
}

// TemplateExecHandler executes template commands
// VULNERABILITY: Template injection leading to command injection
func TemplateExecHandler(w http.ResponseWriter, r *http.Request) {
	template := r.URL.Query().Get("template")
	value := r.URL.Query().Get("value")

	// VULNERABILITY: String replacement then execution
	cmdStr := strings.Replace(template, "{{VALUE}}", value, -1)
	cmd := exec.Command("sh", "-c", cmdStr)

	output, _ := cmd.CombinedOutput()
	w.Write(output)
}
