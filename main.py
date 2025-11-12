import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Portfolio Backend", version="1.0.0")

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "backend", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"healthy": True}


@app.get("/test")
def test_database():
    """Lightweight DB connectivity check using optional Mongo vars."""
    info = {
        "backend": "running",
        "database": {
            "configured": False,
            "connected": False,
            "error": None,
        },
    }
    try:
        from database import db
        import os as _os
        url = _os.getenv("DATABASE_URL")
        name = _os.getenv("DATABASE_NAME")
        if url and name:
            info["database"]["configured"] = True
            if db is not None:
                # attempt a simple command
                try:
                    _ = db.list_collection_names()
                    info["database"]["connected"] = True
                except Exception as e:  # pragma: no cover
                    info["database"]["error"] = str(e)[:200]
        return info
    except Exception as e:
        info["database"]["error"] = str(e)[:200]
        return info


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
