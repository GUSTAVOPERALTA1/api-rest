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
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id_cliente)))
        response=cursor.fetchall()
        return response   
    
#Metodo GET con limit y offset    
@app.get("/clientes/", response_model=List[Cliente])
async def get_clientes(offset:int=0,limit:int=11):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes LIMIT ? OFFSET ?",(limit,offset))
        response = cursor.fetchall()
        return response
    
#Metodo POST
@app.post('/insertar/{nombre}/{email}')
async def post_clientes(nombre:str,email:str):
	with sqlite3.connect('sql/clientes.sqlite') as connection:
		connection.row_factory = sqlite3.Row
		cursor = connection.cursor()
		cursor.execute('INSERT INTO clientes (nombre,email) VALUES (?,?)',(nombre,email))
		cursor.fetchall()
		return {"mensaje":"Cliente agregado"}

#Metodo PUT
@app.put('/actulizar/{id}/{nombre}/{email}')
async def put_clientes(id:str, nombre:str, email:str):
	with sqlite3.connect('sql/clientes.sqlite') as connection:
		connection.row_factory = sqlite3.Row
		cursor = connection.cursor()
		cursor.execute('UPDATE clientes SET nombre = ?, email = ? WHERE id_cliente = ?',(nombre,email,id))
		cursor.fetchall()
		return {"mensaje":"Cliente Actualizado"}

#Metodo DELETE
@app.delete('/eliminar/{id}')
async def delete_clientes(id:int):
	with sqlite3.connect('sql/clientes.sqlite') as connection:
		connection.row_factory = sqlite3.Row
		cursor = connection.cursor()
		cursor.execute('DELETE FROM clientes WHERE id_cliente= {}'.format(int(id)))
		cursor.fetchall()
		return {"mensaje":"Cliente borrado"}