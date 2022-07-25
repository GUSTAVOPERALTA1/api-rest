from fastapi import *
from fastapi.security import *
from pydantic import BaseModel
import pyrebase
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
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

class Usuario(BaseModel):
    email: str
    password: str

class Respuesta(BaseModel):
    message: str

@app.get('/',
summary="Api-Rest")
async def get():
    return "API-REST NUEVO"

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


@app.get("/user/validate/",
         status_code=status.HTTP_202_ACCEPTED,
         summary="Ver token del usuario",
         description="Ver token",
         tags=["auth"])
def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
        email = credentials.username
        password = credentials.password
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        response = {
            "token": user["idToken"]
        }
        return response
    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


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
