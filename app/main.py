from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

app = FastAPI(
    title="OZD API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

security = HTTPBearer()


async def verify_api_key(
        credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if credentials.credentials != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
