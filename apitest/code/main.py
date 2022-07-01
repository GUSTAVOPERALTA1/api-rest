import hashlib   # importa la libreria hashlib
import sqlite3  # Conecta con la base de datos
import os  # Permite trabajar con rutas independientemente del sistema operativo
from typing import List  # Generar las listas de items

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials  # Protocolo para identificar usuarios, basica
from pydantic import BaseModel 

app = FastAPI()  # Creacion de objeto

 # Ruta del sqlite
DATABASE_URL = os.path.join("sql/usuarios.sqlite")  # Ruta del sqlite

security = HTTPBasic()  # Permite preguntar usuario y contraseña

class Respuesta(BaseModel):
    message: str

class Cliente(BaseModel):
    id_cliente: int
    nombre: str
    email: str

class Usuarios(BaseModel):
    username: str
    level: int

@app.get("/", response_model=Respuesta)
async def index():
    return{"message": "API-REST"}

def get_current_level(credentials: HTTPBasicCredentials = Depends(security)):
    password_b = hashlib.md5(credentials.password.encode())  # Convierte a bits
    password = password_b.hexdigest()  # convierte a hexadecimal
    with sqlite3.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),
        )
        user = cursor.fetchone()  # Recibe valor de 0 o 1 si el usuario existe
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0]

@app.get( #  Donde me conecto
    "/usuarios/",
    response_model=List[Usuarios],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa una lista de usuarios",  # Dar informacion del endpoint
    description="Regresa una lista de usuarios",
)
async def get_usuarios(level: int = Depends(get_current_level)):  #Compara lo pedido en el login
    if level == 0:  # Administrador
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT username, level FROM usuarios")
            usuarios = cursor.fetchall()
            return usuarios
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/clientes/{id_cliente}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa una lista de clientes",
    description="Regresa una lista de usuarios"
    )
async def get_usuarios(id_cliente,level: int = Depends(get_current_level)):  #Compara lo pedido en el login
    if level == 0:  # Administrador
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            cursor=connection.cursor()        
            cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id_cliente)))
            response=cursor.fetchall()
            return response 
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

#Metodo GET con limit y offset 
@app.get("/clientes/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa una lista de clientes",
    description="Regresa una lista de usuarios",
    response_model=List[Cliente])
async def get_usuarios(offset:int=0,limit:int=11, level: int = Depends(get_current_level)): 
    if level == 0:
        with sqlite3.connect('sql/clientes.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes LIMIT ? OFFSET ?",(limit,offset))
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )
        
#Metodo POST
@app.post('/insertar/{nombre}/{email}',
     status_code=status.HTTP_202_ACCEPTED,
    summary="Inserta nuevo cliente",
    description="Inserta nuevo cliente")
async def post_clientes(nombre:str,email:str, level: int = Depends(get_current_level)):
	if level == 0:
		with sqlite3.connect('sql/clientes.sqlite') as connection:
			connection.row_factory = sqlite3.Row
			cursor = connection.cursor()
			cursor.execute('INSERT INTO clientes (nombre,email) VALUES (?,?)',(nombre,email))
			cursor.fetchall()
			return {"mensaje":"Cliente agregado"}
	else:
		raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

#Metodo PUT
@app.put('/actulizar/{id}/{nombre}/{email}',
    status_code=status.HTTP_202_ACCEPTED,
    summary="Actualiza lista de clientes",
    description="Actualiza lista de clientes")
async def put_clientes(id:str, nombre:str, email:str, level: int = Depends(get_current_level)):
    if level == 0:
        with sqlite3.connect('sql/clientes.sqlite') as connection:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute('INSERT INTO clientes (nombre,email) VALUES (?,?)',(nombre,email))
                cursor.fetchall()
                return {"mensaje":"Cliente agregado"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

#Metodo DELETE
@app.delete('/eliminar/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    summary="Eliminar clientes",
    description="Eliminar clientes"
    )
async def delete_clientes(id:int, level: int = Depends(get_current_level)):
    if level == 0:
     with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('DELETE FROM clientes WHERE id_cliente= {}'.format(int(id)))
        cursor.fetchall()
        return {"mensaje":"Cliente borrado"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )