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
from fastapi.security import *
import pyrebase

app = FastAPI()

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


class Respuesta(BaseModel):
    message: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class ClienteIN(BaseModel):
    nombre: str
    email: str

class Usuario(BaseModel):
    email: str
    password: str
    
firebaseConfig = {
    'apiKey': "AIzaSyBxBXyHeSa0qQZL6-3W44QB1eAx_yl0cg0",
    'authDomain': "pyrebase-cac34.firebaseapp.com",
    'databaseURL': "https://pyrebase-cac34-default-rtdb.firebaseio.com",
    'projectId': "pyrebase-cac34",
    'storageBucket': "pyrebase-cac34.appspot.com",
    'messagingSenderId': "742912089065",
    'appId': "1:742912089065:web:806cee59a0e23c2d218978"
}

firebase = pyrebase.initialize_app(firebaseConfig)
securityBasic = HTTPBasic()
securityBearer = HTTPBearer()

@app.get('/', response_model=Respuesta)
async def index():
    return{'message': 'API-REST'}

#METODO GET
@app.get("/clientes/{id_cliente}", response_model=Cliente,
    summary ="Ver cliente con ID",
    description = "Usa el ID del usuario para verlo a detalle",
    status_code = status.HTTP_200_OK,
    tags = ["auth"])
async def get_cliente(id_cliente: int, credentials: HTTPAuthorizationCredentials= Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

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
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

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

@app.get("/user/validate/",
         status_code=status.HTTP_202_ACCEPTED,
         summary="Ver token del usuario",
         description="Ver token",
         tags=["auth"])
async def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
        email = credentials.username
        password = credentials.password
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        response = {
            "token": user["idToken"],
        }
        return response
    except Exception as error:
        print(error)


@app.get("/user/",
         status_code=status.HTTP_202_ACCEPTED,
         summary="Ver usuarios",
         description="Ver usuario en Realtime",
         tags=["auth"])
async def get_user(credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        db = firebase.database()
        user_data = db.child("users").child(uid).get().val()

        response = {
            'user_data': user_data
        }
        return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post("/user/",
    status_code= status.HTTP_202_ACCEPTED,
    summary="Insertar usuario",
    description="Insertar usuarios dentro de Firebase Realtime",
    tags=["add"])
async def insert_user(post_user: Usuario):
    try: 
        email = post_user.email
        password = post_user.password
        auth = firebase.auth()
        datos = {
            'email' : email,
            'nivel' : 1,
            'nombre' : 'user'
        }
        crear = auth.create_user_with_email_and_password(email, password)
        db = firebase.database()
        db.child("users").child(crear["localId"]).set(datos)
        return {"message": "Cliente agregado"}
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

