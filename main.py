"""
main.py
-------
API de FYM que expone /validate y /endorsement para el consumo B2B de Citi
a través de Apigee. Ambas rutas están protegidas centralizadamente mediante
la dependencia verify_client_certificate (mTLS + validación de thumbprint).
"""

import logging

from cryptography import x509
from fastapi import APIRouter, Depends, FastAPI
from pydantic import BaseModel

from security import verify_client_certificate

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="FYM API - Integración B2B Citi",
    description="Endpoints protegidos con mTLS (Azure App Service + Apigee).",
    version="1.0.0",
)


# agrupar la dependencia a nivel de router para no repetirla en cada función.
secure_router = APIRouter(dependencies=[Depends(verify_client_certificate)])


class ValidateRequest(BaseModel):
    reference_id: str
    amount: float
    currency: str = "USD"


class EndorsementRequest(BaseModel):
    reference_id: str
    endorsement_code: str


@secure_router.post("/validate")
async def validate(
    payload: ValidateRequest,
    cert: x509.Certificate = Depends(verify_client_certificate),
):
    # `cert` está disponible aquí por si se necesita loguear/auditar el Subject
    # exacto que originó la transacción (trazabilidad por certificado).
    return {
        "status": "ok",
        "endpoint": "validate",
        "reference_id": payload.reference_id,
        "client_subject": cert.subject.rfc4514_string(),
    }


@secure_router.post("/endorsement")
async def endorsement(
    payload: EndorsementRequest,
    cert: x509.Certificate = Depends(verify_client_certificate),
):
    return {
        "status": "ok",
        "endpoint": "endorsement",
        "reference_id": payload.reference_id,
        "client_subject": cert.subject.rfc4514_string(),
    }


@app.get("/health")
async def health():
    # Endpoint SIN mTLS, útil para health checks de Azure/Apigee que no
    # presentan certificado de cliente.
    return {"status": "healthy"}


app.include_router(secure_router)