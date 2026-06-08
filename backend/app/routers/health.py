from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

# Import the modules, not the values inside them.
# `from app.database.postgres import engine` would copy None at import time
# and never see the value assigned later by init_postgres(). Importing the
# module itself means we read .engine at call time, after startup has run.
import app.database.mongo as mongo_db
import app.database.postgres as pg_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "",
    summary="Health check",
    description="Pings both databases and reports their status.",
)
async def health_check():
    results: dict[str, str] = {}

    # ── PostgreSQL ────────────────────────────────────────────────────────────
    # Open a connection from the pool and run the simplest possible query.
    # If this fails, the engine is misconfigured or Postgres is unreachable.
    try:
        async with pg_db.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        results["postgres"] = "ok"
    except Exception as exc:
        results["postgres"] = f"error: {exc}"

    # ── MongoDB ───────────────────────────────────────────────────────────────
    # `ping` is MongoDB's standard "are you alive?" command.
    # We run it against the admin database, which always exists.
    try:
        await mongo_db.client.admin.command("ping")
        results["mongo"] = "ok"
    except Exception as exc:
        results["mongo"] = f"error: {exc}"

    # Return HTTP 200 only if both databases responded without error.
    all_ok = all(v == "ok" for v in results.values())
    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={
            "status": "ok" if all_ok else "degraded",
            "databases": results,
        },
    )
