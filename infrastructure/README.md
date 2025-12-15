# Infrastructure as Code

This directory contains infrastructure definitions across multiple IaC tools and cloud providers.

## Structure

### terraform/
- `aws-legacy/` - Terraform 0.11 syntax (deprecated patterns)
- `aws-modern/` - Terraform 1.x with subtle misconfigurations
- `azure/` - Azure resource definitions
- `gcp/` - Google Cloud Platform resources
- `modules/` - Shared modules with embedded vulnerabilities

### kubernetes/
- `base/` - Base Kubernetes manifests
- `overlays/` - Kustomize overlays
- `helm-charts/` - Helm chart definitions

### cloudformation/
AWS CloudFormation templates with security issues

### pulumi/
Pulumi programs (TypeScript) with misconfigurations

### ansible/
Ansible playbooks and roles with security issues

## Vulnerability Categories

### IAM/Access Control
- Overly permissive IAM policies (`*:*`)
- Missing least privilege
- Excessive role assumptions
- Cross-account trust issues

### Network Security
- Public-facing resources that should be private
- Overly permissive security groups
- Missing network segmentation
- Unencrypted traffic

### Data Protection
- Unencrypted storage (S3, RDS, EBS)
- Missing encryption at rest
- Public S3 buckets
- Exposed secrets

### Logging/Monitoring
- Disabled CloudTrail
- Missing VPC flow logs
- No audit logging
- Disabled access logging

### Kubernetes Specific
- Privileged containers
- hostPath mounts
- Missing resource limits
- No network policies
- Default service accounts with elevated permissions

## Scanner Challenges

- Understanding Terraform module composition
- Resolving variable references across files
- Handling multiple state configurations
- Kustomize overlay resolution
- Helm template rendering
- Cross-resource relationship analysis
