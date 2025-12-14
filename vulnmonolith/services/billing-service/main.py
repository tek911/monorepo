"""
Billing Service - Main Application
WARNING: This application is INTENTIONALLY VULNERABLE for security testing.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from routers import invoices, payments, reports, webhooks
from config.settings import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Billing Service",
    description="Intentionally Vulnerable Billing Service",
    version="1.0.0",
    # VULNERABILITY: Debug mode enabled
    debug=True
)

# VULNERABILITY: CORS allows all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(invoices.router, prefix="/api/invoices", tags=["invoices"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # VULNERABILITY: Detailed error messages exposed
    logger.error(f"Error processing request: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": type(exc).__name__,
            # VULNERABILITY: Stack trace in response
            "detail": repr(exc)
        }
    )


@app.get("/")
async def root():
    return {"message": "Billing Service API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy", "debug": settings.DEBUG}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
