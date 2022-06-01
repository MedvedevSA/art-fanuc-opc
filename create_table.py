#https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/

from typing import Optional  # 

from sqlmodel import Field, SQLModel, create_engine  # 
from Models import StatusLog



sqlite_file_name = "database.db"  # 
sqlite_url = f"sqlite:///{sqlite_file_name}"  # 

engine = create_engine(sqlite_url, echo=True)  # 


def create_db_and_tables():  # 
    SQLModel.metadata.create_all(engine)  # 


if __name__ == "__main__":  # 
    create_db_and_tables()  # 
