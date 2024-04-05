from typing import Optional
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.get("/sqlalchemy")


def test(db: Session = Depends(get_db)):
    all_messages = db.query(models.Message).all()
    return {"Mensagem": all_messages}


class Message(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_messages = [
    {"title": "titulo-1", "content": "conteudo-1", "id": 1},
    {"title": "titulo-2", "content": "conteudo-2", "id": 2},
]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_values(new_message: Message, db: Session = Depends(get_db)):
    # create_message = models.Message(**new_message.model_dump())
    create_message = models.Message(
        title=new_message.title,
        content=new_message.content,
        published=new_message.published,
        rating=new_message.rating,
    )
    db.add(create_message)
    db.commit()
    db.refresh(create_message)
    return {"Mensagem Criada": create_message}


def find_message_for_id(message, id):
    for message in my_messages:
        if message["id"] == id:
            return message
    return None


@app.get("/messages/{id}")
def get_msg(id: int, db: Session = Depends(get_db)):
    found_message = db.query(models.Message).filter(models.Message.id == id).first()
    if not found_message:
        raise HTTPException(
            status_code=404, detail=f"Mensagem com o id {id} não encontrada"
        )
    return {"Mensagem Encontrada": found_message}


def find_index_by_id(messages, id):
    for i, message in enumerate(messages):
        if message["id"] == id:
            return i
    return None


@app.delete("/messages/{id}")
def delete_msg(id: int):
    index = find_index_by_id(my_messages, id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mensagem com o id {id} não encontrada",
        )
    else:
        my_messages.pop(index)
    return {"Mensagem Deletada": id}


@app.put("/mensages/{id}")
def update_msg(id: int, update_mensagem=Message):
    index = find_index_by_id(my_messages, id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mensagem com o id {id} não encontrada",
        )
    else:
        dict_message = update_mensagem.model_dump()
        dict_message["id"] = id
        my_messages[index] = update_mensagem.dict_message
    return {"Mensagem Atualizada": my_messages[index]}
