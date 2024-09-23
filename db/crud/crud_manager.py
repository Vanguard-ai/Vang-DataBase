from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Table 
from db.db import DatabaseManager
from .crud_model import InsertTableModel, QueryTableModel, ColumnModel


class CRUD:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager
        Session = sessionmaker(bind=self.database_manager.engine)
        self.session = Session()

    def create_record(self, table_name: str, data: InsertTableModel) -> str:
        try:
            data_dict = {col.column_name: col.data for col in data.table_to_insert}
            table = Table(table_name, self.database_manager.metadata, autoload_with=self.database_manager.engine)
            insert_stmt = table.insert().values(**data_dict)
            self.session.execute(insert_stmt)
            self.session.commit()
            return f"Record added to '{table_name}'!"
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Error adding record to '{table_name}': {e}")

    def read_record(self, table_name: str, filters: InsertTableModel = None) -> QueryTableModel:
        try:
            table = Table(table_name, self.database_manager.metadata, autoload_with=self.database_manager.engine)
            query = self.session.query(table)
            if filters:
                data_dict = {col.column_name: col.data for col in filters.table_to_insert}
                query = query.filter_by(**data_dict)
            query_result=[dict(row._mapping) for row in query.all()]
            return QueryTableModel(table_query=[
                ColumnModel(column_name=k,data=v) for k,v in query_result[0].items()
            ])
        
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error reading from '{table_name}': {e}")
        
    def update_record(self, table_name: str, filters: InsertTableModel, data: InsertTableModel) -> str:
        try:
            filters_dict = {col.column_name: col.data for col in filters.table_to_insert}
            data_dict = {col.column_name: col.data for col in data.table_to_insert}
            table = Table(table_name, self.database_manager.metadata, autoload_with=self.database_manager.engine)
            update_stmt = table.update().where(
                *[table.c[col].__eq__(value) for col, value in filters_dict.items()]
            ).values(**data_dict)
            self.session.execute(update_stmt)
            self.session.commit()
            
            return f"Record(s) updated in '{table_name}'!"
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Error updating record in '{table_name}': {e}")

    def delete_record(self, table_name: str, filters: InsertTableModel) -> str:
        try:
            filters_dict = {col.column_name: col.data for col in filters.table_to_insert}
            table = Table(table_name, self.database_manager.metadata, autoload_with=self.database_manager.engine)
            delete_stmt = table.delete().where(
                *[table.c[col].__eq__(value) for col, value in filters_dict.items()]
            )
            self.session.execute(delete_stmt)
            self.session.commit()
            
            return f"Record(s) deleted from '{table_name}'!"
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Error deleting record from '{table_name}': {e}")
