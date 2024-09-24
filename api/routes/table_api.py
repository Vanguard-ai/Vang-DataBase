from fastapi import APIRouter,HTTPException
from sqlalchemy.exc import SQLAlchemyError

from db.db import DatabaseManager, TableModel

table_router = APIRouter()

table_manager = DatabaseManager("sqlite:///example.db")


@table_router.post("/create_table/", response_model=dict)
async def create_table(table_data: TableModel) -> dict[str, str]:
    try:
        result = table_manager.create_table(table_data)
        return {"message": result}
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@table_router.delete("/drop_table/{table_name}")
async def drop_table(table_name: str)-> dict[str, str]:
    try:
        result = table_manager.drop_table(table_name)
        return {"message": result}
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@table_router.post("/table_metadata/{table_name}")
async def query_metadata(table_name: str): #no la puedo typar pq es un quilombo la validacion la concha de la lora
    try:
        result = table_manager.get_table_info(table_name)
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

