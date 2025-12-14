"""
Webhooks Router
Contains SSRF and other vulnerabilities
"""

from fastapi import APIRouter, HTTPException, Request
import httpx
import requests
from urllib.parse import urlparse
import logging

from config.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register")
async def register_webhook(url: str, events: list = ["payment.success"]):
    """
    VULNERABILITY: SSRF via webhook registration
    CWE-918: Server-Side Request Forgery
    """
    # VULNERABILITY: No URL validation
    # Attacker can register internal URLs: http://169.254.169.254/latest/meta-data/

    try:
        # VULNERABILITY: Following redirects can bypass filters
        response = requests.get(url, allow_redirects=True, timeout=5)

        if response.status_code == 200:
            return {"registered": True, "url": url, "events": events}

        raise HTTPException(status_code=400, detail="URL not reachable")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/test")
async def test_webhook(url: str, payload: dict = {}):
    """
    VULNERABILITY: SSRF via webhook testing
    """
    try:
        # VULNERABILITY: Arbitrary URL request
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10)

        return {
            "status_code": response.status_code,
            "body": response.text[:1000]  # VULNERABILITY: Response data exposure
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/fetch")
async def fetch_url(url: str):
    """
    VULNERABILITY: SSRF with insufficient validation
    """
    parsed = urlparse(url)

    # VULNERABILITY: Insufficient blocklist
    # Can bypass with: http://127.0.0.1.nip.io, http://localhost@evil.com
    blocked_hosts = ['localhost', '127.0.0.1', '0.0.0.0']

    if parsed.hostname in blocked_hosts:
        raise HTTPException(status_code=400, detail="Blocked host")

    # VULNERABILITY: Still vulnerable to DNS rebinding, IP variations
    try:
        response = requests.get(url, timeout=5)
        return {"content": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/callback")
async def process_callback(request: Request):
    """
    VULNERABILITY: Open redirect via callback
    """
    data = await request.json()
    redirect_url = data.get('redirect_url', '/')

    # VULNERABILITY: No validation on redirect URL
    return {"redirect": redirect_url, "processed": True}


@router.post("/stripe")
async def stripe_webhook(request: Request):
    """
    VULNERABILITY: Missing webhook signature verification
    """
    # VULNERABILITY: No signature verification
    # Should use stripe.Webhook.construct_event()

    body = await request.json()
    event_type = body.get('type')

    logger.info(f"Received Stripe webhook: {event_type}")

    # Process without verification
    return {"received": True, "type": event_type}
