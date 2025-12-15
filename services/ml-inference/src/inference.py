"""
ML Inference Service
Contains vulnerabilities for security scanner testing.
"""
import os
import pickle
import subprocess
from typing import Any, Dict

import yaml
import requests
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

app = FastAPI(title="ML Inference Service")

# VULNERABILITY: Hardcoded credentials
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
MODEL_API_KEY = "ml-platform-key-12345"
REDIS_PASSWORD = "redis_ml_password"


class PredictionRequest(BaseModel):
    model_name: str
    input_data: list
    model_url: str = None


# VULNERABILITY: Unsafe pickle loading for models
def load_model(model_path: str) -> Any:
    """Load ML model from pickle file - UNSAFE."""
    with open(model_path, 'rb') as f:
        # VULNERABILITY: Pickle deserialization
        return pickle.load(f)


# VULNERABILITY: Path traversal in model loading
@app.get("/models/{model_path:path}")
async def get_model_info(model_path: str):
    """Get model information - VULNERABLE TO PATH TRAVERSAL."""
    # VULNERABILITY: No path validation
    full_path = f"/models/{model_path}"
    with open(full_path, 'r') as f:
        return {"model_info": f.read()}


# VULNERABILITY: SSRF via model URL
@app.post("/load-remote-model")
async def load_remote_model(request: PredictionRequest):
    """Load model from remote URL - VULNERABLE TO SSRF."""
    if request.model_url:
        # VULNERABILITY: Fetching arbitrary URL
        response = requests.get(request.model_url)
        model_data = response.content
        # VULNERABILITY: Deserializing remote content
        model = pickle.loads(model_data)
        return {"status": "loaded"}
    raise HTTPException(400, "No model URL provided")


# VULNERABILITY: Command injection in preprocessing
@app.post("/preprocess")
async def preprocess_data(command: str, data: str):
    """Preprocess data using external command - COMMAND INJECTION."""
    # VULNERABILITY: Unvalidated command execution
    result = subprocess.run(
        f"{command} {data}",
        shell=True,
        capture_output=True
    )
    return {"output": result.stdout.decode()}


# VULNERABILITY: Arbitrary file upload
@app.post("/upload-model")
async def upload_model(file: UploadFile = File(...), path: str = ""):
    """Upload model file - PATH TRAVERSAL POSSIBLE."""
    # VULNERABILITY: No path validation, arbitrary file write
    save_path = f"/models/{path}/{file.filename}"
    with open(save_path, 'wb') as f:
        f.write(await file.read())
    return {"saved_to": save_path}


# VULNERABILITY: Unsafe YAML config loading
@app.post("/configure")
async def configure(config_yaml: str):
    """Configure service - UNSAFE YAML LOADING."""
    # VULNERABILITY: yaml.load without safe loader
    config = yaml.load(config_yaml, Loader=yaml.Loader)
    return {"config": config}


# VULNERABILITY: Eval for dynamic computation
@app.post("/compute")
async def compute(expression: str):
    """Compute expression - CODE INJECTION."""
    # VULNERABILITY: Eval on user input
    result = eval(expression)
    return {"result": result}


# VULNERABILITY: Exposed debug endpoint
@app.get("/debug")
async def debug():
    """Debug endpoint - INFORMATION DISCLOSURE."""
    return {
        "aws_key": AWS_ACCESS_KEY,
        "aws_secret": AWS_SECRET_KEY,
        "model_key": MODEL_API_KEY,
        "redis_pass": REDIS_PASSWORD,
        "env": dict(os.environ)
    }


# VULNERABILITY: No rate limiting, no auth
@app.post("/predict")
async def predict(request: PredictionRequest):
    """Make prediction - NO AUTHENTICATION."""
    model = load_model(f"/models/{request.model_name}.pkl")
    input_array = np.array(request.input_data)
    prediction = model.predict(input_array)
    return {"prediction": prediction.tolist()}


if __name__ == "__main__":
    import uvicorn
    # VULNERABILITY: Debug mode enabled
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
