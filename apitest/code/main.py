from http.client import HTTPException
from urllib import response
from urllib.request import Request
from lib2to3.pytree import Base
from typing import Union
from typing_extensions import Self
from fastapi import FastAPI, Security
import sqlite3
from typing import List
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException, status
from requests import post
import hashlib
import os
from fastapi import *
from fastapi.security import *
import pyrebase


class Respuesta(BaseModel):
    message: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class ClienteIN(BaseModel):
    nombre: str
    email: str


app = FastAPI()

securityBasic = HTTPBasic()
securityBearer = HTTPBearer()

origins = [  # Puertos Permitidos
    "http://127.0.0.1:8090",
    "http://127.0.0.1:8000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"], # Metodos permitidos
    allow_headers=["*"],
)


@app.get('/', response_model=Respuesta)
async def index():
    return{'message': 'API-REST'}

#METODO GET
@app.get("/clientes/{id_cliente}", response_model=Cliente)
async def get_cliente(id_cliente: int):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory= sqlite3.Row
        cursor=connection.cursor()
        cursor.execute("SELECT id_cliente,email,nombre FROM clientes where id_cliente = ?", (id_cliente,))
        response=cursor.fetchone()
        if response is None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail= "id_cliente no encontrado",
                headers={"WWW-Authenticate": "Basic"},
            )
        return response

@app.get("/clientes/", response_model=List[Cliente],
status_code=status.HTTP_202_ACCEPTED,
summary="Lista de clientes",
description="Lista de clientes completa")
async def clientes():
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM clientes')
        response = cursor.fetchall()
        return response

#Metodo GET con limit y offset    
@app.get('/clientes1/', response_model=List[Cliente])
async def get_clientes(offset:int=0,limit:int=11):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM clientes LIMIT ? OFFSET?',(limit,offset))
        response = cursor.fetchall()
        return response

#METODO POST
@app.post("/clientes/", response_model= Respuesta)
async def post_clientes(cliente: ClienteIN):
    with sqlite3.connect("sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO clientes (nombre,email) VALUES (?,?)",
            (cliente.nombre, cliente.email),
        )
        connection.commit()
        return {"message":"Cliente agregado"}

#METODO PUT
@app.put("/clientes/", 
response_model=Respuesta,
status_code=status.HTTP_202_ACCEPTED,
summary="Actualizar cliente",
description="Actualizar un registro de cliente")
async def update_cliente(cliente: Cliente):
    with sqlite3.connect("sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("UPDATE clientes SET nombre =?, email= ? WHERE id_cliente =?;",
        (cliente.nombre, cliente.email, cliente.id_cliente))
        connection.commit()
        response = {"message":"Cliente actualizado"}
        return response

#METODO DELETE
@app.delete("/clientes/", 
response_model=Respuesta,
status_code=status.HTTP_202_ACCEPTED,
summary="Eliminar usuario",
description="Eliminar usuario por ID")
async def delete_cliente(id_cliente: int=0):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor=connection.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = '{id_cliente}';".format(id_cliente=id_cliente))
        cursor.fetchall()
        response = {"message":"Cliente eliminado"}
        return response
