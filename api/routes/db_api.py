from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from db.db import DatabaseManager

db_router = APIRouter()

db_manager = DatabaseManager("sqlite:///example.db")

@db_router.post("/create_db/")
async def create_db() -> dict[str, str]:
    try:
        result = db_manager.create_database()
        return {"message": result}
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@db_router.post("/drop_db/")
async def drop_db() -> dict[str, str]:
    try:
        result = db_manager.drop_database()
        return {"messsage": result}
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))