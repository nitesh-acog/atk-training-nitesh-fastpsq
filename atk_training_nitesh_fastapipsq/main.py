from fastapi import FastAPI, Depends, status, Response, HTTPException, Request

# from pydantic import BaseModel
# define all schemas in schema module
from sqlalchemy.orm import Session
import uvicorn
from atk_training_nitesh_fastapipsq import models,schema
from atk_training_nitesh_psq.sqlite_ import SQLITE

# asgi server
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from atk_training_nitesh_fastapipsq import Engine, Base, local_session
from atk_training_nitesh_fastapipsq.schema import Queue,voicetext
import typer
import os

cli = typer.Typer()


app = FastAPI()

# Mouting the templates and static files to app object here
main_dir = os.path.dirname(os.path.realpath("main.py"))
templates_dir = os.path.join(main_dir, "atk_training_nitesh_fastapipsq", "templates")

static_dir = os.path.join(main_dir, "atk_training_nitesh_fastapipsq", "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)
models.Base.metadata.create_all(bind=Engine)

@app.get("/")
def helloworld(response: Response, request: Request):
    return templates.TemplateResponse("speech.html",{"request": request,'hello':'world'})

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

@app.post("/speechrecognition")
async def get_voice(request: Request,db: Session = Depends(get_db)):
    data:bytes=await request.body()
    data:str=data.decode("utf-8").split('\n')[4].strip()
    print(data)
    sql_=SQLITE()
    sql_.put(data)

    
    


@app.post("/add", status_code=201)
def create(request: Queue, db: Session = Depends(get_db)):
    queue = models.Queue(id=request.id,item=request.item,status=request.status,retries=request.retries,start_time=request.start_time,end_time=request.end_time)
    db.add(queue)
    db.commit()
    db.refresh(queue)

    return queue

@app.get('/queue')
def get_queue(response: Response, request: Request, db: Session = Depends(get_db)):
    queue= db.query(models.Queue).all()

    if not queue:
        response.status_code = status.HTTP_404_NOT_FOUND

    def columns():
        return schema.Queue.schema()['required']

    def getting_tup():
        for item in queue:
            # yield {'id':bl.id,'title':bl.title}
            yield (item.id, item.item,item.processed,item.status,item.retries,item.start_time,item.end_time)

    return templates.TemplateResponse("table.html",
                                      {"request": request, "students": getting_tup(), "columns": columns()})



#xhr.open("POST", "/process_row", true);

@app.get("/process_row/{row_id}/{item}/{status}/{retries}")
def process_row(row_id:int,item:str,status:str,retries:int,response: Response, request: Request,db: Session = Depends(get_db)):
    db.query(models.Queue).filter(models.Queue.id == row_id).update({'item':item,'status':status,'retries':retries})
    print(item)
    
    
    db.commit()
    queue= db.query(models.Queue).all()


    if not queue:
        response.status_code = status.HTTP_404_NOT_FOUND

    def columns():
        return schema.Queue.schema()['required']

    def getting_tup():
        for item in queue:
            # yield {'id':bl.id,'title':bl.title}
            yield (item.id, item.item,item.status,item.retries,item.start_time,item.end_time)
    
    


    return templates.TemplateResponse("table.html",
                                      {"request": request, "students": getting_tup(), "columns": columns()})


    #db.query(models.Queue).filter(models.Queue.id==data[0])
    





@cli.command()
def serve_asgi(host: str = "127.0.0.1", port: int = 8000):
    uvicorn.run(app, host=host, port=port)


def server():
    cli()
