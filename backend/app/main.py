import sys
from pathlib import Path

# Ensure the parent directory (backend) is on sys.path so `app` can be imported when running main.py directly
backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, customer, organization, ws

# Creates tables if they don't exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="QueueHub API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
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


if __name__ == "__main__":
    import uvicorn

    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "run"
    if cmd in ("migrate", "db"):
        print("Creating/migrating database tables...")
        Base.metadata.create_all(bind=engine)
        print("[OK] All database tables migrated successfully!")
    elif cmd in ("seed",):
        print("Running database seed script...")
        from app.seed import run as seed_run
        seed_run()
    else:
        print("Starting QueueHub backend on http://127.0.0.1:8000 ...")
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
