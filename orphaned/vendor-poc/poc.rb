#!/usr/bin/env ruby
# Vendor Proof of Concept
# ABANDONED - Never cleaned up after evaluation
# Contains hardcoded credentials from vendor demo

require 'net/http'
require 'json'
require 'yaml'
require 'erb'
require 'openssl'

# VULNERABILITY: Hardcoded vendor demo credentials (still active)
VENDOR_API_KEY = 'vendor_demo_key_abc123_still_works'
VENDOR_SECRET = 'vendor_secret_xyz789_production'
VENDOR_ENDPOINT = 'https://api.vendor-product.com/v1'

# VULNERABILITY: Hardcoded database credentials from POC
DATABASE_CONFIG = {
  host: 'poc-db.vendor.internal',
  username: 'poc_admin',
  password: 'poc_password_456',
  database: 'vendor_poc'
}

# VULNERABILITY: SSL verification disabled
def insecure_request(url)
  uri = URI.parse(url)
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true
  # DANGEROUS: SSL verification disabled
  http.verify_mode = OpenSSL::SSL::VERIFY_NONE
  http.get(uri.request_uri)
end

# VULNERABILITY: Unsafe YAML loading
def load_vendor_config(config_file)
  # DANGEROUS: Unsafe YAML load
  YAML.load(File.read(config_file))
end

# VULNERABILITY: ERB template injection
def render_template(template, data)
  # DANGEROUS: User input in ERB template
  ERB.new(template).result(binding)
end

# VULNERABILITY: Command injection
def run_vendor_script(script_name, args)
  # DANGEROUS: Unvalidated input in system command
  system("./vendor_scripts/#{script_name} #{args}")
end

# VULNERABILITY: SQL injection (if connected to database)
def query_database(table, condition)
  # DANGEROUS: String interpolation in SQL
  "SELECT * FROM #{table} WHERE #{condition}"
end

# VULNERABILITY: Hardcoded encryption key
ENCRYPTION_KEY = 'vendor-poc-key-12345678901234567890'

# VULNERABILITY: Weak encryption (DES)
def encrypt_data(data)
  cipher = OpenSSL::Cipher.new('DES-CBC')
  cipher.encrypt
  cipher.key = ENCRYPTION_KEY[0..7]
  cipher.update(data) + cipher.final
end

# VULNERABILITY: MD5 for integrity checking
require 'digest'
def verify_integrity(data, checksum)
  Digest::MD5.hexdigest(data) == checksum
end

# VULNERABILITY: Eval usage
def execute_vendor_hook(hook_code)
  # DANGEROUS: Executing vendor-provided code
  eval(hook_code)
end

# VULNERABILITY: Exposed demo function
def vendor_demo_backdoor(command)
  # DANGEROUS: Demo backdoor never removed
  `#{command}`
end

# VULNERABILITY: Logging sensitive data
def log_api_call(endpoint, params)
  puts "[VENDOR API] Calling #{endpoint}"
  puts "[VENDOR API] Key: #{VENDOR_API_KEY}"
  puts "[VENDOR API] Secret: #{VENDOR_SECRET}"
  puts "[VENDOR API] Params: #{params.to_json}"
end

# VULNERABILITY: Information disclosure
def debug_info
  {
    vendor_key: VENDOR_API_KEY,
    vendor_secret: VENDOR_SECRET,
    database: DATABASE_CONFIG,
    encryption_key: ENCRYPTION_KEY,
    environment: ENV.to_h
  }
end

# Main POC code - never cleaned up
if __FILE__ == $0
  puts "Vendor POC - SHOULD HAVE BEEN DELETED"
  puts "API Key: #{VENDOR_API_KEY}"
  puts "This file contains live credentials!"
end
