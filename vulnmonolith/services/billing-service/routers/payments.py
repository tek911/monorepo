"""
Payments Router
Contains insecure deserialization and other vulnerabilities
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import pickle
import base64
import yaml
import logging

from config.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/process")
async def process_payment(request: Request):
    """
    VULNERABILITY: Pickle deserialization RCE
    CWE-502: Deserialization of Untrusted Data
    """
    body = await request.body()

    try:
        # VULNERABILITY: Deserializing untrusted pickle data
        # Attacker can craft malicious pickle payload for RCE
        payment_data = pickle.loads(base64.b64decode(body))

        logger.info(f"Processing payment: {payment_data}")

        return {"status": "processed", "data": str(payment_data)}

    except Exception as e:
        # VULNERABILITY: Detailed error exposure
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/config")
async def update_config(request: Request):
    """
    VULNERABILITY: Unsafe YAML loading (arbitrary code execution)
    CWE-502: Deserialization of Untrusted Data
    """
    body = await request.body()

    try:
        # VULNERABILITY: yaml.load without Loader is dangerous
        # Payload: !!python/object/apply:os.system ['id']
        config = yaml.load(body.decode('utf-8'))

        return {"config": config}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/import")
async def import_transactions(request: Request):
    """
    VULNERABILITY: Multiple deserialization issues
    """
    content_type = request.headers.get('content-type', '')
    body = await request.body()

    if 'pickle' in content_type:
        # VULNERABILITY: Pickle RCE
        data = pickle.loads(body)
    elif 'yaml' in content_type:
        # VULNERABILITY: YAML RCE
        data = yaml.load(body.decode('utf-8'))
    else:
        # Default to pickle (VULNERABILITY)
        data = pickle.loads(base64.b64decode(body))

    return {"imported": len(data) if isinstance(data, list) else 1}


@router.get("/export/{format}")
async def export_transactions(format: str, transaction_ids: str = ""):
    """
    VULNERABILITY: Command injection possibility
    """
    import subprocess

    # VULNERABILITY: User input in shell command
    if format == "csv":
        # This could be exploited with format like "csv; rm -rf /"
        cmd = f"echo 'Exporting to {format}' && export_tool --format={format} --ids={transaction_ids}"
        result = subprocess.run(cmd, shell=True, capture_output=True)
        return {"output": result.stdout.decode()}

    return {"error": "Unsupported format"}


@router.post("/webhook/verify")
async def verify_webhook(request: Request):
    """
    VULNERABILITY: Timing attack in signature verification
    """
    signature = request.headers.get('x-signature', '')
    body = await request.body()

    # VULNERABILITY: String comparison vulnerable to timing attacks
    expected_signature = compute_signature(body)

    if signature == expected_signature:  # VULNERABLE: Use hmac.compare_digest
        return {"valid": True}

    raise HTTPException(status_code=401, detail="Invalid signature")


def compute_signature(data: bytes) -> str:
    import hashlib
    # VULNERABILITY: Using MD5 for signatures
    return hashlib.md5(data + settings.WEBHOOK_SECRET.encode()).hexdigest()
