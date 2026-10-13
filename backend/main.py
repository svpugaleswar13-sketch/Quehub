import sys
import argparse
from pathlib import Path

# Add backend directory to sys.path
backend_dir = str(Path(__file__).resolve().parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)


def migrate():
    from app.database import Base, engine
    print("Creating/migrating database tables...")
    Base.metadata.create_all(bind=engine)
    print("[OK] All database tables migrated successfully!")


def seed():
    migrate()
    from app.seed import run as run_seed
    run_seed()


def run_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    import uvicorn
    print(f"Starting QueueHub backend server on http://{host}:{port} ...")
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)


def main():
    parser = argparse.ArgumentParser(description="QueueHub Backend CLI")
    parser.add_argument(
        "action",
        nargs="?",
        default="run",
        choices=["run", "start", "migrate", "seed", "check"],
        help="Action to perform: run (default), start, migrate, seed, or check",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind (default: 8000)")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")

    args = parser.parse_args()

    if args.action == "migrate":
        migrate()
    elif args.action == "seed":
        seed()
    elif args.action == "check":
        migrate()
        print("[OK] Backend configuration and database connection OK!")
    else:
        migrate()
        run_server(host=args.host, port=args.port, reload=not args.no_reload)


if __name__ == "__main__":
    main()
