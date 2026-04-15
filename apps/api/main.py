import os
import logging
import sys
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
import uuid
import time
import asyncio

# Configuração de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Configurações via variáveis de ambiente
API_KEY = os.getenv("API_KEY", "dev-api-key-12345")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "devops")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
REDIS_URL = os.getenv("REDIS_HOST", "redis://localhost:6379")
DEBUG_MODE = os.getenv("DEBUG", "true").lower() == "true"
SECRET_TOKEN = os.getenv("APP_SECRET", "super-secret-token-change-me")

# Audit log para rastreamento de requests
audit_log: List[dict] = []

# Simulação de "banco de dados" em memória
items_db: dict = {}
users_db: dict = {
    "admin": {
        "id": "1",
        "username": "admin",
        "email": "admin@devops-challenge.local",
        "password_hash": "pbkdf2:sha256:150000$...",  # Hash simulado
        "role": "admin",
        "api_key": API_KEY
    }
}

# Métricas em memória
metrics = {
    "requests_total": 0,
    "requests_success": 0,
    "requests_failed": 0,
    "items_created": 0,
    "items_deleted": 0,
    "startup_time": None,
    "last_health_check": None
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciamento do ciclo de vida da aplicação"""
    # Startup
    metrics["startup_time"] = datetime.now().isoformat()
    logger.info(f"Application starting with API_KEY={API_KEY}")
    logger.debug(f"Database URL: {DATABASE_URL}")

    # Seed inicial
    items_db["1"] = {
        "id": "1",
        "name": "Item de Exemplo",
        "description": "Este é um item de exemplo criado automaticamente",
        "created_at": datetime.now().isoformat(),
        "created_by": "system",
        "category": "default",
        "price": 0.0,
        "active": True
    }

    logger.info("Initial data seeded successfully")
    yield
    # Shutdown
    logger.info("Application shutting down")


app = FastAPI(
    title="DevOps Challenge API",
    description="API de gerenciamento de itens para o desafio técnico de DevOps",
    version="2.1.0",
    docs_url="/docs" if DEBUG_MODE else None,
    redoc_url="/redoc" if DEBUG_MODE else None,
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"]
)


# Modelos Pydantic
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field("default", max_length=50)
    price: Optional[float] = Field(0.0, ge=0)

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=50)
    price: Optional[float] = Field(None, ge=0)
    active: Optional[bool] = None

class Item(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    category: str
    price: float
    active: bool
    created_at: str
    created_by: str
    updated_at: Optional[str] = None

class UserInfo(BaseModel):
    id: str
    username: str
    email: str
    role: str


# Middleware para logging e métricas
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    metrics["requests_total"] += 1

    logger.debug(f"Request {request_id}: {request.method} {request.url}")
    logger.debug(f"Headers: {dict(request.headers)}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        if response.status_code < 400:
            metrics["requests_success"] += 1
        else:
            metrics["requests_failed"] += 1

        audit_log.append({
            "request_id": request_id,
            "method": request.method,
            "path": str(request.url.path),
            "status_code": response.status_code,
            "process_time": process_time,
            "timestamp": datetime.now().isoformat(),
            "client_ip": request.client.host if request.client else "unknown"
        })

        return response
    except Exception as e:
        metrics["requests_failed"] += 1
        logger.error(f"Request {request_id} failed: {str(e)}")
        raise


# Dependência para validar API Key (opcional)
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verifica API Key se fornecida"""
    if x_api_key and x_api_key != API_KEY:
        logger.warning(f"Invalid API key attempted: {x_api_key}")
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


# Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    metrics["last_health_check"] = datetime.now().isoformat()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.1.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@app.get("/ready")
async def readiness_check():
    """
    Readiness probe para Kubernetes.
    Verifica se a aplicação está pronta para receber tráfego.
    """
    return {
        "ready": True,
        "checks": {
            "database": "ok",
            "cache": "ok"
        }
    }


@app.get("/metrics")
async def get_metrics():
    """Endpoint de métricas da aplicação."""
    return {
        **metrics,
        "audit_log_size": len(audit_log),
        "items_count": len(items_db),
        "uptime_seconds": (
            (datetime.now() - datetime.fromisoformat(metrics["startup_time"])).total_seconds()
            if metrics["startup_time"] else 0
        ),
        "memory_usage": {
            "audit_entries": len(audit_log),
            "items": len(items_db),
            "users": len(users_db)
        }
    }


@app.get("/api/v1/items", response_model=dict)
async def list_items(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    active_only: bool = True,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """Lista todos os itens com paginação e filtros."""
    items = list(items_db.values())

    if active_only:
        items = [i for i in items if i.get("active", True)]

    if category:
        items = [i for i in items if i.get("category") == category]

    total = len(items)
    items = items[skip:skip + limit]

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@app.post("/api/v1/items", status_code=201)
async def create_item(
    item: ItemCreate,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """Cria um novo item."""
    item_id = str(uuid.uuid4())
    new_item = {
        "id": item_id,
        "name": item.name,
        "description": item.description,
        "category": item.category or "default",
        "price": item.price or 0.0,
        "active": True,
        "created_at": datetime.now().isoformat(),
        "created_by": "api_user",
        "updated_at": None
    }

    items_db[item_id] = new_item
    metrics["items_created"] += 1

    logger.info(f"Item created: {item_id} - {item.name}")

    return new_item


@app.get("/api/v1/items/{item_id}")
async def get_item(
    item_id: str,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """Busca um item específico pelo ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return items_db[item_id]


@app.put("/api/v1/items/{item_id}")
async def update_item(
    item_id: str,
    item_update: ItemUpdate,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """Atualiza um item existente."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    current_item = items_db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        current_item[field] = value

    current_item["updated_at"] = datetime.now().isoformat()
    items_db[item_id] = current_item

    logger.info(f"Item updated: {item_id}")

    return current_item


@app.delete("/api/v1/items/{item_id}")
async def delete_item(
    item_id: str,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """Remove um item pelo ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    del items_db[item_id]
    metrics["items_deleted"] += 1

    logger.info(f"Item deleted: {item_id}")

    return {"message": "Item removido com sucesso", "id": item_id}


# Legacy endpoints for backwards compatibility
@app.get("/api/items")
async def list_items_legacy():
    """Endpoint legado para compatibilidade."""
    return {
        "items": list(items_db.values()),
        "total": len(items_db)
    }


@app.post("/api/items", status_code=201)
async def create_item_legacy(item: ItemCreate):
    """Endpoint legado para compatibilidade."""
    item_id = str(uuid.uuid4())
    new_item = {
        "id": item_id,
        "name": item.name,
        "description": item.description,
        "category": item.category or "default",
        "price": item.price or 0.0,
        "active": True,
        "created_at": datetime.now().isoformat(),
        "created_by": "api_user",
        "updated_at": None
    }
    items_db[item_id] = new_item
    metrics["items_created"] += 1
    return new_item


@app.get("/api/items/{item_id}")
async def get_item_legacy(item_id: str):
    """Endpoint legado para compatibilidade."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return items_db[item_id]


@app.delete("/api/items/{item_id}")
async def delete_item_legacy(item_id: str):
    """Endpoint legado para compatibilidade."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    del items_db[item_id]
    metrics["items_deleted"] += 1
    return {"message": "Item removido com sucesso"}


@app.get("/api/v1/users/me")
async def get_current_user(x_api_key: str = Header(...)):
    """Retorna informações do usuário atual baseado na API key."""
    for user in users_db.values():
        if user.get("api_key") == x_api_key:
            return UserInfo(
                id=user["id"],
                username=user["username"],
                email=user["email"],
                role=user["role"]
            )
    raise HTTPException(status_code=401, detail="Invalid or missing API key")


@app.get("/debug/config")
async def debug_config():
    """Debug endpoint - mostra configurações atuais."""
    if not DEBUG_MODE:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "debug_mode": DEBUG_MODE,
        "log_level": LOG_LEVEL,
        "database_url": DATABASE_URL,
        "redis_url": REDIS_URL,
        "api_key_configured": bool(API_KEY),
        "environment_variables": {
            k: v for k, v in os.environ.items()
            if not k.startswith("_")
        }
    }


@app.get("/debug/audit")
async def get_audit_log(limit: int = 100):
    """Retorna os últimos registros de audit (apenas em debug mode)."""
    if not DEBUG_MODE:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "total_entries": len(audit_log),
        "entries": audit_log[-limit:] if audit_log else []
    }


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handler global de exceções."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    if DEBUG_MODE:
        return JSONResponse(
            status_code=500,
            content={
                "detail": str(exc),
                "type": type(exc).__name__,
                "path": str(request.url.path)
            }
        )

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=DEBUG_MODE,
        log_level=LOG_LEVEL.lower()
    )
