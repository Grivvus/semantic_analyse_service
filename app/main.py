from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    debug=True, docs_url="/",
    title="semantic analyse service",
)
app.include_router(router)


if __name__ == "__main__":
    # declare_schemas()
    # fillup_db()
    print("Hello from main")
