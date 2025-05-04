from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/usersdb",
                   tags=["usersdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

# Inicializar el servidor con el comando uvicorn users:app --reload


    
users_list = []

@router.get("/all", response_model=list[User])
async def users():
    print("getting all users")
    return users_schema(db_client.local.users.find())

#PATH PARAMS - REQUIRED

@router.get("/{id}")
async def user(id: str):
    print(f"searching for path {id}")
    return search_user("_id", ObjectId(id))


#QUERY PARAMS - DINAMIC
@router.get("/")
async def user(id: str):
    print(f"searching for query {id}")
    return search_user("_id", ObjectId(id))


#POST
@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="user already exists")
    
    user_dict = dict(user)
    del user_dict["id"]
    
    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id": ObjectId(id)}))
    
    return User(**new_user)


#PUT
@router.put("/", response_model=User, status_code= status.HTTP_200_OK)
async def update_user(user: User):
    
    try:
        user_dict = dict(user)
        del user_dict["id"]
        found_user = db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    
    except:
        return {"error": "user not upadated"}
        
    if not found_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"user with ID: {user.id} not found")
    
    return search_user("_id", ObjectId(user.id))


#DELETE
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    
    found_user = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"user with ID: {id} not found")
    
    

        
        


def search_user(field: str, key):
    #users_filter = next(filter(lambda user: user.id == id, users_list), None)
    #print(f"searching for {field} with value {key}")
    try:
        user = user_schema(db_client.local.users.find_one({field: key}))
        return User(**user)
    except:
        return {"error": "user not found"}


