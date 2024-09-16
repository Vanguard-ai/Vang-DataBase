from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, Date, Enum
from typing import Literal, List

SQL_TYPES = {
        "Integer": Integer,
        "String": String,
        "Float": Float,
        "Text": Text,
        "Boolean": Boolean,
        "Date": Date,
        "Enum": Enum
    }


class ColumnModel(BaseModel):
    name: str
    type: Literal["Integer", "String", "Float", "Text", "Boolean", "Date", "Enum"]

class TableModel(BaseModel):
    name: str
    columns: List[ColumnModel]

