from fastapi import FastAPI
import uvicorn

app = FastAPI()

from api.routes import db_router, table_router

app = FastAPI()

app.include_router(db_router, prefix="/db", tags=["database"])
app.include_router(table_router, prefix="/tables", tags=["tables"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)