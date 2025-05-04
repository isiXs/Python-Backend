from fastapi import Depends, APIRouter, HTTPException, status
import jwt
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET = "951d7cfe7fcce4b02ff5b5189e411711e1e6584a9fc32a8426a1a81df52276ac"

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

# Entidad user
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

class UserDB(User):
    password: str

users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "john@gmail.com",
        "disable": False,
        "password": "$2a$12$ZXQGUJ5YXggPIXpG/PHnWulF7SIOXEaGwF0DlZvfOPaZ6vpfjrPdy"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@gmail.com",
        "disable": True,
        "password": "$2a$12$oAcHLio3MuUl5LEai1Evn.Yc2tkVqtkF2UGuQ/6z79P0DTxoPYCsG"
    }
}

def search_userDB(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
        
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid credentials", 
                            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        user = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        
        if user is None:
            raise exception
         
    except jwt.PyJWTError:
        raise exception
    
    return search_user(user)



async def get_current_user(user: User = Depends(auth_user)):
    
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Inactive user")
    
    return user
    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect username")
    
    user = search_userDB(form.username)
    
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    
    
    #expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    acces_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    
    return {"access_token": jwt.encode(acces_token,SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user:  User = Depends(get_current_user)):
    return user