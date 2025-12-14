# Terraform Infrastructure

Multi-cloud Terraform configurations with intentional security misconfigurations.

## Structure

### aws-legacy/
Terraform 0.11 syntax (deprecated):
- Uses `${var.x}` interpolation syntax
- No state locking
- Hardcoded credentials
- Missing provider version constraints

### aws-modern/
Terraform 1.x with subtle issues:
- Overly permissive IAM
- Missing encryption
- Public resources
- Weak network security

### azure/
Azure Resource Manager via Terraform:
- Public blob storage
- Weak network security groups
- Missing diagnostic settings
- Overly permissive RBAC

### gcp/
Google Cloud Platform resources:
- Public GCS buckets
- Missing audit logging
- Weak IAM bindings
- Unencrypted resources

### modules/
Shared modules with embedded vulnerabilities:
- Consumed by other configurations
- Tests module vulnerability propagation
- Contains default insecure values
