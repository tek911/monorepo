# ML Inference Service

Machine Learning inference service for model predictions.

## Stack
- Python 3.9
- FastAPI
- TensorFlow/PyTorch
- Redis for caching

## Vulnerabilities for Testing

### Model Security
- Pickle deserialization for model loading
- Arbitrary file access for model paths
- No input validation on inference requests

### API Security
- Missing authentication
- SSRF via model URL fetching
- Command injection in preprocessing

### Infrastructure
- Hardcoded ML platform credentials
- Exposed metrics endpoints
- Debug mode enabled
