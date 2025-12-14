"""
Reports Router
Contains SSTI and path traversal vulnerabilities
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from jinja2 import Template, Environment, FileSystemLoader
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# VULNERABILITY: Debug mode in Jinja2
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=False  # VULNERABILITY: XSS
)


@router.get("/generate")
async def generate_report(
    template: str = Query(..., description="Report template"),
    data: str = Query("{}", description="JSON data for template")
):
    """
    VULNERABILITY: Server-Side Template Injection (SSTI)
    CWE-94: Improper Control of Generation of Code
    """
    import json

    try:
        # VULNERABILITY: User-controlled template string
        # Payload: {{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
        tmpl = Template(template)
        context = json.loads(data)

        rendered = tmpl.render(**context)

        return HTMLResponse(content=rendered)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/template/{name}")
async def render_template(name: str, title: str = "Report"):
    """
    VULNERABILITY: Path traversal in template loading
    CWE-22: Path Traversal
    """
    # VULNERABILITY: No validation on template name
    # Attack: ../../../etc/passwd
    template_path = f"templates/{name}.html"

    try:
        with open(template_path, 'r') as f:
            content = f.read()

        # VULNERABILITY: SSTI with file content
        tmpl = Template(content)
        return HTMLResponse(content=tmpl.render(title=title))

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Template not found")


@router.get("/download")
async def download_report(filename: str):
    """
    VULNERABILITY: Path traversal in file download
    """
    # VULNERABILITY: No path validation
    file_path = f"/var/reports/{filename}"

    if os.path.exists(file_path):
        return FileResponse(file_path)

    raise HTTPException(status_code=404, detail="Report not found")


@router.post("/email")
async def email_report(
    recipient: str,
    subject: str,
    body_template: str
):
    """
    VULNERABILITY: SSTI in email body
    """
    # VULNERABILITY: User-controlled template
    tmpl = Template(body_template)
    body = tmpl.render(recipient=recipient)

    # Simulated email sending
    logger.info(f"Sending email to {recipient}: {body}")

    return {"sent": True, "to": recipient}


@router.get("/custom")
async def custom_report(
    query: str,
    format_string: str = "{amount} - {description}"
):
    """
    VULNERABILITY: Format string vulnerability
    """
    # Simulated data
    data = {"amount": 100, "description": "Test"}

    # VULNERABILITY: User-controlled format string
    # Python format strings can leak data
    try:
        result = format_string.format(**data)
        return {"formatted": result}
    except Exception as e:
        return {"error": str(e)}
