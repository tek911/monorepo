# ML Inference Service

Python ML service with C++ extensions.

## Technology Stack

- Python 3.9
- TensorFlow / PyTorch
- C++ (pybind11)
- NumPy

## Vulnerabilities

### Python SAST Findings

| Type | Location | Severity |
|------|----------|----------|
| Pickle Deserialization | model/loader.py:34 | Critical |
| Command Injection | utils/preprocess.py:56 | Critical |
| Path Traversal | api/models.py:23 | High |
| SSRF | clients/download.py:45 | High |
| Hardcoded API Keys | config/cloud.py:12 | Critical |
| Unsafe YAML | config/loader.py:67 | High |

### C++ SAST Findings

| Type | Location | Severity |
|------|----------|----------|
| Buffer Overflow | src/tensor.cpp:45 | Critical |
| Integer Overflow | src/matrix.cpp:67 | High |
| Use After Free | src/cache.cpp:23 | Critical |
| Memory Leak | src/pool.cpp:89 | Medium |

### SCA Findings

| Dependency | Version | CVE | Severity |
|------------|---------|-----|----------|
| tensorflow | 2.4.0 | CVE-2021-XXXXX | High |
| numpy | 1.19.0 | CVE-2021-XXXXX | Medium |
| Pillow | 8.0.0 | CVE-2021-25287 | High |
| PyYAML | 5.3 | CVE-2020-1747 | Critical |

## Build

```bash
cd services/ml-inference
pip install -r requirements.txt
python -m build
```
