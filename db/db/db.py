from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
from db.db.models.table_model import TableModel, SQL_TYPES

class DatabaseManager:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self.engine = create_engine(self.database_url, echo=True)
        self.metadata = MetaData()
        self.Base = declarative_base()

    def create_database(self) -> str:
        try:
            self.Base.metadata.create_all(self.engine)
            return "Database created!"
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error creating database: {e}")

    def drop_database(self) -> str:
        try:
            self.Base.metadata.drop_all(self.engine)
            return "Database dropped!"
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error dropping database: {e}")

    def create_table(self, table_data: TableModel) -> str:
        try:
            columns_with_types = [
                Column(col.column_name, SQL_TYPES[col.column_type]) for col in table_data.columns
            ]
            new_table = Table(
                table_data.table_name, self.metadata, *columns_with_types, extend_existing=True
            )
            new_table.create(self.engine)
            return f"Table '{table_data.table_name}' created!"
        
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error creating table '{table_data.name}': {e}")
        
    def drop_table(self, table_name: str) -> str:
        try:
            table_to_drop = Table(table_name, self.metadata, autoload_with=self.engine)
            table_to_drop.drop(self.engine)
            return f"Table '{table_name}' dropped!"
        
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error dropping table '{table_name}': {e}")

    def get_table_info(self, table_name: str) -> dict:
        try:
            inspector = inspect(self.engine)
            columns_info = inspector.get_columns(table_name)
            
            table_info = {
                'table_name': table_name,
                'columns': [{'name': col['name'], 'type': col['type']} for col in columns_info]
            }
            
            return table_info
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error getting table info for '{table_name}': {e}")
    
