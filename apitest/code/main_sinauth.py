from fastapi import FastAPI
import sqlite3
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class Respuesta(BaseModel):
    message: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

app = FastAPI()

origins = [  # Puertos Permitidos
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Metodos permitidos
    allow_headers=["*"],
)

@app.get('/', response_model=Respuesta)
async def index():
    return{'message': 'API-REST'}
@app.get('/clientes/{id_cliente}')
async def get_clientesid(id_cliente):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id_cliente)))
        response=cursor.fetchall()
        return response

#Metodo GET  
@app.get('/clientes/')
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

#Metodo POST
@app.post('/insertar/{nombre}/{email}')
async def post_clientes(nombre:str,email:str):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('INSERT INTO clientes (nombre,email) VALUES(?,?)',(nombre,email))
        cursor.fetchall()
        return {'mensaje': 'Cliente agregado'}

#Metodo PUT
@app.put('/actulizar/{id_cliente}/{nombre}/{email}')
async def put_clientes(id:str, nombre:str, email:str):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('UPDATE clientes SET nombre = ?, email = ? WHERE id_cliente = ?',(nombre,email,id))
        cursor.fetchall()
        return {'mensaje': 'Cliente Actualizado'}

#Metodo DELETE
@app.delete('/eliminar/{id_cliente}')
async def delete_clientes(id_cliente:int):
    with sqlite3.connect('sql/clientes.sqlite') as connection: connection.row_factory = sqlite3.Row 
    cursor = connection.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente={}".format(int(id_cliente)))
    cursor.fetchall()
    return {'mensaje': 'Cliente borrado'}

