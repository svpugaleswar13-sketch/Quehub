import socket
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings


def _probe_render_host(parsed: urllib.parse.ParseResult) -> str | None:
    """If a Render internal hostname (e.g. dpg-d9dmemn41pts73df6tng-a) cannot be resolved
    because the web service and database are in different regions, try resolving through
    Render's external region gateways."""
    host = parsed.hostname
    if not host or not host.startswith("dpg-") or "." in host:
        return None

    user = parsed.username or ""
    pwd = parsed.password or ""
    port = parsed.port or 5432
    dbname = parsed.path.lstrip("/")

    regions = ["singapore", "oregon", "frankfurt", "ohio", "virginia"]
    import psycopg2
    for r in regions:
        ext_host = f"{host}.{r}-postgres.render.com"
        try:
            conn = psycopg2.connect(
                host=ext_host,
                port=port,
                user=user,
                password=pwd,
                dbname=dbname,
                sslmode="require",
                connect_timeout=3,
            )
            conn.close()
            netloc = f"{user}:{pwd}@{ext_host}:{port}" if pwd else f"{user}@{ext_host}:{port}"
            res_url = parsed._replace(netloc=netloc).geturl()
            if "sslmode=" not in res_url:
                sep = "&" if "?" in res_url else "?"
                res_url = f"{res_url}{sep}sslmode=require"
            print(f"[OK] Automatically resolved Render cross-region database host to: {ext_host}")
            return res_url
        except Exception as e:
            err = str(e).lower()
            if "password authentication failed" in err or f'database "{dbname}" does not exist' in err:
                netloc = f"{user}:{pwd}@{ext_host}:{port}" if pwd else f"{user}@{ext_host}:{port}"
                res_url = parsed._replace(netloc=netloc).geturl()
                if "sslmode=" not in res_url:
                    sep = "&" if "?" in res_url else "?"
                    res_url = f"{res_url}{sep}sslmode=require"
                print(f"[OK] Matched Render region '{r}' for host: {ext_host}")
                return res_url
            continue
    return None


def _resolve_database_url(url: str) -> str:
    """Ensure database host is resolvable; normalize postgres:// to postgresql://;
    auto-recover if Render internal hostname cannot be resolved due to cross-region deployment."""
    if not url:
        return url

    url = url.strip()
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]

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
            # 1. Check if Render internal hostname failed (cross-region issue on Render)
            if host.startswith("dpg-") and "." not in host:
                probed = _probe_render_host(parsed)
                if probed:
                    return probed
                print(f"[WARNING] Could not resolve Render internal host '{host}'.")
                print("[HINT] If your Render Web Service and PostgreSQL DB are in different regions,")
                print("      update DATABASE_URL in your Render Web Service settings to the 'External Database URL'.")

            # 2. Check if Neon host DNS issue
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


connect_args = {}
if "postgresql" in settings.database_url:
    connect_args = {
        "connect_timeout": 20,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }

engine = create_engine(
    _resolve_database_url(settings.database_url),
    pool_size=10,
    max_overflow=20,
    pool_recycle=300,
    pool_pre_ping=True,
    connect_args=connect_args,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
