from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()


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


@app.post("/create")
def create_values(new_message: Message):
    try:
        dict_message = new_message.model_dump()
        dict_message["id"] = my_messages[-1]["id"] + 1
        my_messages.append(dict_message)
        return {"Mensagem": my_messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def find_message_for_id(message, id):
    for message in my_messages:
        if message["id"] == id:
            return message
    return None


@app.get("/messages/{id}")
def get_msg(id: int):
    found_message = find_message_for_id(my_messages, int(id))
    return {"Mensagem Encontrada": found_message}
