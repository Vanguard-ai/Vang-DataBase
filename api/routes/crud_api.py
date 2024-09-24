from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from db.crud import CRUD,InsertTableModel
from db.db import DatabaseManager
from .api_key import verify_api_key

crud_router = APIRouter()

db_manager = DatabaseManager("sqlite:///example.db")

crud=CRUD(db_manager)

@crud_router.post("/crud_add/{table_name}") 
async def add_element(table_name: str, data: InsertTableModel,
                      api_key: str = Depends(verify_api_key)) -> dict[str, str]:
    try: 
        result = crud.create_record(table_name=table_name,data=data)
        return {"message":result}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=(str(e)))
    

@crud_router.post("/crud_query/{table_name}")
async def query_element(table_name: str, filters: InsertTableModel = None,
                        api_key: str = Depends(verify_api_key)) -> dict:
    try:
        result = crud.read_record(table_name=table_name,filters=filters) 
        return result.model_dump()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=(str(e)))
    

@crud_router.delete("/crud_delete/{table_name}")
async def delete_element(table_name: str, filters: InsertTableModel,
                         api_key: str = Depends(verify_api_key)) -> dict[str, str]:
    try:
        result = crud.delete_record(table_name=table_name, filters=filters)
        return {"message":result}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=(str(e)))


@crud_router.post("/crud_update/{table_name}")
async def update_element(table_name: str, 
                         filters: InsertTableModel, 
                         data: InsertTableModel,
                         api_key: str = Depends(verify_api_key)) -> dict[str, str]:
    try:
        result = crud.update_record(table_name=table_name,filters=filters,data=data)
        return {"message": result}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=(str(e)))