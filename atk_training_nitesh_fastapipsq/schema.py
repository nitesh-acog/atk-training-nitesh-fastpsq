from pydantic import BaseModel
from datetime import datetime

class Queue(BaseModel):
    id:int
    item:str
    processed:str
    status:str
    retries:int
    start_time:datetime
    end_time:datetime

class voicetext(BaseModel):
    text:str