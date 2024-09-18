from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData
from db.db.models.table_model import create_table, TableModel
from db.db.db import SessionLocal


app = FastAPI()

@app.get("/") # App de testing
def read_root():
    return {"message": "Vamos vanguard carajo!"}

# Configuración del motor y metadata
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

@app.on_event("startup")
async def startup_event():
    # Crear tablas en la base de datos
    table_model = TableModel(
        name="example_table",
        columns=[
            {"name": "id", "type": "Integer"},
            {"name": "name", "type": "String"},
            {"name": "age", "type": "Integer"}
        ]
    )
    create_table(table_model, metadata)
    metadata.create_all(bind=engine)  # Crear las tablas en la base de datos


from fastapi import FastAPI
import uvicorn

from api.routes import db_router, table_router

app = FastAPI()

app.include_router(db_router, prefix="/db", tags=["database"])
app.include_router(table_router, prefix="/tables", tags=["tables"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)