from http.client import HTTPException
from urllib import response
from fastapi import FastAPI
import sqlite3
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException, status
from requests import post


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

origins = [  # Puertos Permitidos
    "http://127.0.0.1:8080",
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
#Metodo GET  
@app.get('/clientes/', response_model=List[Cliente])
async def get_clientes():
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
@app.put("/clientes/")
async def put_clientes(cliente: ClienteIN):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("UPDATE clientes SET (nombre,email) WHERE id_cliente = ? VALUES(?,?)",(cliente.nombre, cliente.email),)
        connection.commit()
        return {'mensaje': 'Cliente Actualizado'}

#Metodo DELETE
#@app.delete('/eliminar/{id}')
#async def eliminar(id: int):
 #   with sqlite3.connect('sql/clientes.sqlite') as connection:
  #      connection.row_factory = sqlite3.Row
   #     cursor = connection.cursor()
    #    cursor.execute('DELETE FROM clientes WHERE id_cliente= {}'.format(int(id)))
     #   cursor.fetchall()
      #  return {"mensaje": "Cliente borrado"}


@app.delete("/clientes/", response_model=Respuesta,status_code=status.HTTP_202_ACCEPTED,)
async def clientes_delete(id_cliente: int=0):
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor=connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = '{id_cliente}';".format(id_cliente=id_cliente))
            cursor.fetchall()
            response = {"message":"Cliente borrado"}
            return response

