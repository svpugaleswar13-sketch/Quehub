import socket
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings


def _resolve_database_url(url: str) -> str:
    """Ensure database host is resolvable; if system DNS fails (e.g. ISP blocking Neon),
    resolve via fallback or inject hostaddr so psycopg2 does not crash."""
    if "hostaddr=" in url or "sqlite" in url:
        return url

    try:
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        if not host or host in ("localhost", "127.0.0.1"):
            return url

        try:
            socket.gethostbyname(host)
        except (socket.gaierror, OSError):
            # System DNS refused/failed; resolve using Google DNS or known pooler IP
            resolved_ip = None
            if "neon.tech" in host:
                try:
                    import urllib.request
                    import json
                    req = urllib.request.Request(
                        f"https://dns.google/resolve?name={host}&type=A",
                        headers={"User-Agent": "QueueHub/1.0"}
                    )
                    with urllib.request.urlopen(req, timeout=3) as resp:
                        data = json.loads(resp.read().decode())
                        for ans in data.get("Answer", []):
                            if ans.get("type") == 1:
                                resolved_ip = ans["data"]
                                break
                except Exception:
                    resolved_ip = "13.251.213.89"
                if not resolved_ip:
                    resolved_ip = "13.251.213.89"

            if resolved_ip:
                separator = "&" if "?" in url else "?"
                return f"{url}{separator}hostaddr={resolved_ip}"
    except Exception:
        pass
    return url


engine = create_engine(_resolve_database_url(settings.database_url), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
