from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from models import TableModel, SQL_TYPES

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
            raise RuntimeError(f"Database created: {e}")

    def drop_database(self) -> str:
        try:
            self.Base.metadata.drop_all(self.engine)
            return "Database dropped!"
        except SQLAlchemyError as e:
           raise RuntimeError(f"Error dropping database: {e}")

    def create_table(self, table_data: TableModel) -> str:
        try:
            columns_with_types = [
                Column(col.name, SQL_TYPES[col.type]) for col in table_data.columns
            ]

            new_table = Table(
                table_data.name, self.metadata, *columns_with_types, extend_existing=True
            )
            new_table.create(self.engine)
            return f"Table '{table_data.name}' created!"
        
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error creating table '{table_data.name}': {e}")
        
    def drop_table(self, table_name: str) -> str:
        try:
            table_to_drop = Table(table_name, self.metadata, autoload_with=self.engine)
            table_to_drop.drop(self.engine)
            return f"Table '{table_name}' dropped!"
        
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error dropping table '{table_name}': {e}")