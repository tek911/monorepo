#!/usr/bin/env python3
"""
Backup Script
Contains multiple security vulnerabilities for scanner testing.
"""
import os
import sys
import subprocess
import pickle
import yaml
import tempfile
import ftplib
import smtplib

# VULNERABILITY: Hardcoded credentials
DB_HOST = "prod-db.internal.example.com"
DB_USER = "backup_admin"
DB_PASSWORD = "Backup_Pr0d_2024!"
DB_NAME = "production"

AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

FTP_HOST = "backup.example.com"
FTP_USER = "ftpbackup"
FTP_PASS = "ftp_secret_123"

SMTP_USER = "alerts@company.com"
SMTP_PASS = "email_password_456"


def backup_database(output_path):
    """
    Backup database to file.
    VULNERABILITY: Command injection via shell=True
    """
    # VULNERABILITY: shell=True with string formatting
    cmd = f"pg_dump -h {DB_HOST} -U {DB_USER} {DB_NAME} > {output_path}"
    subprocess.run(cmd, shell=True, env={"PGPASSWORD": DB_PASSWORD})


def backup_with_user_path(user_path):
    """
    VULNERABILITY: Path traversal and command injection
    """
    # VULNERABILITY: Unvalidated user input in path
    full_path = f"/backups/{user_path}"

    # VULNERABILITY: Command injection
    subprocess.call(f"tar -czf {full_path}.tar.gz /app/data", shell=True)


def load_config(config_file):
    """
    VULNERABILITY: Unsafe YAML loading
    """
    with open(config_file, 'r') as f:
        # VULNERABILITY: yaml.load without safe Loader
        return yaml.load(f, Loader=yaml.FullLoader)


def restore_state(state_file):
    """
    VULNERABILITY: Unsafe pickle deserialization
    """
    with open(state_file, 'rb') as f:
        # VULNERABILITY: pickle.load on untrusted data
        return pickle.load(f)


def save_state(state, state_file):
    """Save state using pickle."""
    with open(state_file, 'wb') as f:
        pickle.dump(state, f)


def upload_to_ftp(local_file, remote_path):
    """
    Upload backup to FTP server.
    VULNERABILITY: Unencrypted FTP with hardcoded credentials
    """
    # VULNERABILITY: Plain FTP (not SFTP/FTPS)
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)

    with open(local_file, 'rb') as f:
        ftp.storbinary(f'STOR {remote_path}', f)

    ftp.quit()


def send_notification(message):
    """
    VULNERABILITY: Hardcoded SMTP credentials
    """
    server = smtplib.SMTP('smtp.example.com', 587)
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(SMTP_USER, "admin@company.com", message)
    server.quit()


def execute_hook(hook_command):
    """
    VULNERABILITY: Arbitrary command execution
    """
    # VULNERABILITY: eval on user-controlled input
    eval(hook_command)


def create_temp_backup():
    """
    VULNERABILITY: Insecure temporary file handling
    """
    # VULNERABILITY: Predictable temp file name
    temp_file = "/tmp/backup_temp.sql"

    # Write sensitive data to predictable location
    with open(temp_file, 'w') as f:
        f.write(f"-- Password: {DB_PASSWORD}\n")
        f.write("-- Backup data here\n")

    return temp_file


def run_remote_script(url):
    """
    VULNERABILITY: Downloading and executing remote code
    """
    import urllib.request

    # VULNERABILITY: Fetching and executing remote code
    script_content = urllib.request.urlopen(url).read()
    exec(script_content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: backup.py <output_path>")
        sys.exit(1)

    output_path = sys.argv[1]
    backup_database(output_path)
    print(f"Backup completed to {output_path}")
