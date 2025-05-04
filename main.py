from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import products, users, basic_auth_users, jwt_auth, users_db

app = FastAPI()

# Inicializar el servidor con el comando uvicorn main:app --reload

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth.router)
app.include_router(users_db.router)


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/url")
async def getUrlFacebook():
    return {"url_facebook": "https://www.facebook.com/"}


#Inicializar el servidor con el comando uvicorn main:app --reload
#detener el servidor con ctrl + c

#Documentacion con swagger en http://127.0.0.1:8000/docs
#Documentacion con redoc en http://127.0.0.1:8000/redoc