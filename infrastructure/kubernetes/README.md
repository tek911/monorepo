# Kubernetes Manifests

Kubernetes configurations with security misconfigurations.

## Structure

### base/
Base manifests using Kustomize:
- Deployments with privileged containers
- Services exposing sensitive ports
- ConfigMaps with secrets
- ServiceAccounts with excessive permissions

### overlays/
Environment-specific overlays:
- `dev/` - Development (most permissive)
- `staging/` - Staging environment
- `prod/` - Production (should be secure but isn't)

### helm-charts/
Helm chart definitions:
- Insecure default values
- Missing security contexts
- Privileged pod specs
- Missing resource limits

## Security Issues

- Privileged containers
- hostPath mounts to `/`, `/etc`, `/var/run/docker.sock`
- No resource limits (CPU/memory)
- No network policies
- Default service accounts with cluster-admin
- Secrets in plain text ConfigMaps
- `latest` image tags
- Missing readiness/liveness probes
- No pod security policies/standards
