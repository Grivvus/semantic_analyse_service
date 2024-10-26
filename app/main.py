from fastapi import FastAPI

from app.routes import router
from app.prepare_db import declare_schemas, fillup_db

app = FastAPI(
    debug=True, docs_url="/",
    title="semantic analyse service",
)
app.include_router(router)


if __name__ == "__main__":
    try:
        declare_schemas()
        fillup_db()
    except Exception:
        print("[WARNING]: database has been initialised already")
    print("Hello from main")
