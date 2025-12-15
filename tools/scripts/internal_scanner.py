#!/usr/bin/env python3
"""
Internal Security Scanner
Irony: A security scanner with its own security vulnerabilities.
Tests whether scanners scan the scanners.
"""
import os
import re
import sys
import subprocess
import json
import pickle
import requests
from pathlib import Path

# VULNERABILITY: Hardcoded API credentials
VIRUSTOTAL_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
SHODAN_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxx"
GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


class VulnerableScanner:
    """
    A security scanner that is itself vulnerable.
    The irony is intentional for testing purposes.
    """

    def __init__(self, target_path):
        self.target_path = target_path
        self.results = []

    def scan_for_secrets(self, file_path):
        """
        Scan file for secrets.
        VULNERABILITY: Uses regex patterns that could cause ReDoS
        """
        # VULNERABILITY: Potential ReDoS patterns
        patterns = [
            r'(password|passwd|pwd)\s*[=:]\s*["\']?([^"\'\s]+)["\']?',
            r'(api[_-]?key|apikey)\s*[=:]\s*["\']?([^"\'\s]+)["\']?',
            r'(secret|token)\s*[=:]\s*["\']?([^"\'\s]+)["\']?',
            # VULNERABILITY: Catastrophic backtracking possible
            r'(a+)+$',
        ]

        with open(file_path, 'r', errors='ignore') as f:
            content = f.read()
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                self.results.extend(matches)

    def run_external_tool(self, tool_name, args):
        """
        VULNERABILITY: Command injection via tool arguments
        """
        # VULNERABILITY: shell=True with user-controlled args
        cmd = f"{tool_name} {args}"
        return subprocess.run(cmd, shell=True, capture_output=True)

    def fetch_vulnerability_db(self, url):
        """
        VULNERABILITY: SSRF - fetches arbitrary URLs
        """
        # VULNERABILITY: No URL validation, SSRF possible
        response = requests.get(url, timeout=30)
        return response.json()

    def load_scan_profile(self, profile_path):
        """
        VULNERABILITY: Unsafe deserialization
        """
        # VULNERABILITY: pickle.load on untrusted file
        with open(profile_path, 'rb') as f:
            return pickle.load(f)

    def save_results(self, output_path):
        """
        VULNERABILITY: Path traversal in output
        """
        # VULNERABILITY: No path validation
        with open(output_path, 'w') as f:
            json.dump(self.results, f)

    def execute_plugin(self, plugin_code):
        """
        VULNERABILITY: Arbitrary code execution via plugins
        """
        # VULNERABILITY: exec on untrusted code
        exec(plugin_code)

    def scan_git_repo(self, repo_url):
        """
        VULNERABILITY: Command injection via repo URL
        """
        # VULNERABILITY: Unvalidated URL in git command
        temp_dir = f"/tmp/scan_{os.getpid()}"
        subprocess.run(f"git clone {repo_url} {temp_dir}", shell=True)
        return temp_dir

    def check_with_virustotal(self, file_hash):
        """
        Check file hash against VirusTotal.
        VULNERABILITY: API key exposed in requests
        """
        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        headers = {
            # VULNERABILITY: Hardcoded API key in request
            "x-apikey": VIRUSTOTAL_API_KEY
        }
        return requests.get(url, headers=headers)

    def upload_results(self, server_url, data):
        """
        VULNERABILITY: Sending data to arbitrary server
        """
        # VULNERABILITY: No SSL verification, arbitrary destination
        requests.post(server_url, json=data, verify=False)


def main():
    if len(sys.argv) < 2:
        print("Usage: internal_scanner.py <target_path>")
        sys.exit(1)

    target = sys.argv[1]

    # VULNERABILITY: Log sensitive token
    print(f"Starting scan with API key: {VIRUSTOTAL_API_KEY[:10]}...")

    scanner = VulnerableScanner(target)

    for root, dirs, files in os.walk(target):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                scanner.scan_for_secrets(file_path)
            except Exception as e:
                print(f"Error scanning {file_path}: {e}")

    print(f"Found {len(scanner.results)} potential secrets")


if __name__ == "__main__":
    main()
