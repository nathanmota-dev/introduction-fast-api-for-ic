from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status


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


@app.post("/create", status_code=status.HTTP_201_CREATED)
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
    if not found_message:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
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