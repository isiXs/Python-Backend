from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()

# Inicializar el servidor con el comando uvicorn users:app --reload



# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    url: str
    
users_list = [User(id=1, name="Juan", surname="isixs", age=25, url="http://isixs.com"),
              User(id=2,name="Yamile", surname="Yami", age=24, url="http://yami.com"),
              User(id=3,name="Kevin", surname="Pokemon", age=23, url="http://pokemon.com")]


@router.get("/usersJson")
async def usersJson():
    return [{"usuario": "Juan", "surname": "isixs", "age": 25, "url": "http://isixs.com"}, 
            {"usuario": "Yamile", "surname": "Yami", "age": 24, "url": "http://yami.com"},
            {"usuario": "Kevin", "surname": "Pokemon", "age": 23, "url": "http://pokemon.com"}]

@router.get("/users")
async def users():
    return users_list

#PATH PARAMS - REQUIRED

@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


#QUERY PARAMS - DINAMIC
@router.get("/user/")
async def user(id: int):
    return search_user(id)


#POST
@router.post("/user/",response_model=User, status_code=201)
async def create_user(user: User):
   
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404,detail="user already exists")
    
    users_list.append(user)
    return user

    """
    if search_user(user.id) == {"error": "user not found"}:
        users_list.append(user)
        return user
    else:
        return {"error": "user already exists"}
    """


#PUT
@router.put("/user/", status_code=200)
async def update_user(user: User):
    
    found_user = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found_user = True
        
    if not found_user:
        raise HTTPException(status_code=404, detail=f"user with ID: {user.id} not found")
    
    return user


#DELETE
@router.delete("/user/{id}", status_code=204)
async def delete_user(id: int):
    for index, user in enumerate(users_list):
        if id == user.id:
            del users_list[index]
            return {"message": "User deleted"}
    
    raise HTTPException(status_code=404, detail=f"user with ID: {user.id} not found")

        
        


def search_user(id: int):
    users_filter = next(filter(lambda user: user.id == id, users_list), None)
    
    if users_filter is None:
        raise HTTPException(status_code=404, detail=f"user with ID: {id} not found")
    
    return users_filter;


