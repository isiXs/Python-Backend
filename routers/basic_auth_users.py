from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "disable": True,
        "password": "123456"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@gmail.com",
        "disable": True,
        "password": "654321"
    }
}


""" 
def search_user(username: str):
    if users_db.get(username) != None:
        return UserDB(**users_db.get(username))
"""


def search_userDB(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
        
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
        
    
async def get_current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"})
    
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
    if user.password != form.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    
    return {"access_token": user.username, "token_type": "bearer"}

#Funcion para deslogearse
@router.post("/logout")
async def logout():
    
    return {"message": "Logout"}

@router.get("/users/me")
async def me(user:  User = Depends(get_current_user)):
    return user