from typing import Optional
from sqlmodel import Field, SQLModel, create_engine  # 

class StatusLog(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)  
    client_ip: str   
    log_time: str   
    client_status: int 