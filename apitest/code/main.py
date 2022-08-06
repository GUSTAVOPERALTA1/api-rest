from fastapi import *
from fastapi.security import *
from pydantic import BaseModel
import pyrebase
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
import sqlite3
from typing import List
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

@app.get('/', response_model=Respuesta,
    tags=["get"])
async def index():
    return{'message': 'API-REST'}

#METODO GET
@app.get("/clientes/{id_cliente}", response_model=Cliente,
    summary ="Ver cliente con ID",
    description = "Usa el ID del usuario para verlo a detalle",
    status_code = status.HTTP_200_OK,
    tags = ["get"])
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

# GET LISTA DE CLIENTES
@app.get("/clientes/", response_model=List[Cliente],
status_code=status.HTTP_202_ACCEPTED,
summary="Lista de clientes",
description="Lista de clientes completa",
tags = ["get"])
async def clientes(credentials: HTTPAuthorizationCredentials= Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']
        
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM clientes')
            response = cursor.fetchall()
            return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


#Metodo GET con limit y offset    
@app.get('/clientes1/', response_model=List[Cliente],
    tags=["get"])
async def get_clientes(offset:int=0,limit:int=11):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM clientes LIMIT ? OFFSET?',(limit,offset))
        response = cursor.fetchall()
        return response

#METODO POST
@app.post("/clientes/",response_model= Respuesta,
    summary= "Actualizar cliente",
    description= "Actualizar un cliente existente",
    status_code = status.HTTP_202_ACCEPTED,
    tags = ["post"])
async def post_clientes(cliente: ClienteIN, credentials: HTTPAuthorizationCredentials= Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO clientes (nombre,email) VALUES (?,?)",
                (cliente.nombre, cliente.email),)
            connection.commit()
            return {"message":"Cliente agregado"}
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


#METODO PUT
@app.put("/clientes/", response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Actualizar cliente",
    description="Actualizar un registro de cliente",
    tags= ["put"])
async def update_cliente(cliente: Cliente, credentials: HTTPAuthorizationCredentials= Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        with sqlite3.connect("sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("UPDATE clientes SET nombre =?, email= ? WHERE id_cliente =?;",
            (cliente.nombre, cliente.email, cliente.id_cliente))
            connection.commit()
            response = {"message":"Cliente actualizado"}
            return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


#METODO DELETE
@app.delete("/clientes/", response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Eliminar usuario",
    description="Eliminar usuario por ID",
    tags=["delete"])
async def delete_cliente(id_cliente: int=0, credentials: HTTPAuthorizationCredentials= Depends(securityBearer)):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user['users'][0]['localId']

        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor=connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = '{id_cliente}';".format(id_cliente=id_cliente))
            cursor.fetchall()
            response = {"message":"Cliente eliminado"}
            return response
    except Exception as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


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
    tags=["post"])
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

