from fastapi import FastAPI
import sqlite3
from typing import List
from pydantic import BaseModel

class Respuesta(BaseModel):
    message: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

app = FastAPI()


@app.get("/", response_model=Respuesta)
async def index():
    return{"message": "API-REST"}

@app.get("/clientes/{id_cliente}")
async def get_clientesid(id_cliente):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id_cliente)))
        response=cursor.fetchall()
        return response   
    
#Metodo GET con limit y offset    
@app.get("/clientes/", response_model=List[Cliente])
async def get_clientes(offset:int=0,limit:int=10):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes LIMIT ? OFFSET ?",(limit,offset))
        response = cursor.fetchall()
        return response
#Metodo POST
@app.post("/clientes/")
async def post_clientes(cliente=Cliente):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor=connection.cursor()
        cursor.execute("INSERT INTO clientes(id_cliente,nombre,email)VALUES(?,?,?)",(cliente.id_cliente,cliente.nombre,cliente.email))
        response=cursor.fetchall()
        return {"mensaje":"Cliente agregado"}