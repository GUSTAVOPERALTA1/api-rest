from fastapi import *
from fastapi.security import *
import pyrebase

app = FastAPI()


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