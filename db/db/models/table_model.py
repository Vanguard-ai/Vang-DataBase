from sqlalchemy import Table, MetaData
from sqlalchemy import Column
from sqlalchemy import Integer, String, Float, Text, Boolean, Date, Enum
from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, Date, Enum
from typing import Literal

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

class ColumnModelCreation(BaseModel):
    column_name: str
    column_type: Literal["Integer", "String", "Float", "Text", "Boolean", "Date", "Enum"]

class TableModel(BaseModel):
    model_config = ConfigDict(json_schema_extra=EXAMPLE_TABLE)
    table_name: str
    columns: list[ColumnModelCreation]

# Corregido: `metadata` debe ser un objeto de SQLAlchemy, no `engine`
def create_table(table_model: TableModel, metadata: MetaData):
    columns = []
    for col in table_model.columns:
        column_type = SQL_TYPES[col.type]
        columns.append(Column(col.name, column_type))
    
    # Crear la tabla
    table = Table(table_model.name, metadata, *columns)
    return table
