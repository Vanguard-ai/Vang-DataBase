from pydantic import BaseModel
from typing import Union


class ColumnModel(BaseModel):
    column_name: str
    data: Union[str,int,float,bool]


class InsertTableModel(BaseModel):
    table_to_insert: list[ColumnModel]


class QueryTableModel(BaseModel):
    table_query: list[ColumnModel]