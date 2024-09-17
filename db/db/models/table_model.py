from pydantic import BaseModel, ConfigDict
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

EXAMPLE_TABLE = {
            "example": {
                "table_name": "test_table",
                "columns": [
                    {"column_name": "id", "column_type": "Integer"},
                    {"column_name": "name", "column_type": "String"},
                    {"column_name": "age", "column_type": "Integer"},
                    {"column_name": "height", "column_type": "Float"}
                ]
            }
        }

class ColumnModel(BaseModel):
    column_name: str
    column_type: Literal["Integer", "String", "Float", "Text", "Boolean", "Date", "Enum"]

class TableModel(BaseModel):
    model_config = ConfigDict(json_schema_extra=EXAMPLE_TABLE)
    table_name: str
    columns: List[ColumnModel]
