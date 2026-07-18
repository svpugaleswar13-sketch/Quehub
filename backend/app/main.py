from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, customer, organization, ws

# Creates tables if they don't exist yet. For real production use, prefer
# Alembic migrations (already listed in requirements.txt) instead of this.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="QueueHub API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(organization.router)
app.include_router(ws.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
