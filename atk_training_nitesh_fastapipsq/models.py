from atk_training_nitesh_fastapipsq.database import Base
from sqlalchemy import Column,Integer,String,DateTime

class Queue(Base):
    __tablename__='Queue'
    id= Column(Integer,primary_key=True,index=True)
    item=Column(String)
    processed=Column(String)
    status=Column(String)
    retries=Column(Integer)
    start_time=Column(DateTime)
    end_time=Column(DateTime)
    