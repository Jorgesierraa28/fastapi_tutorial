from fastapi import FastAPI

app = FastAPI() #incicializa la API app 

@app.get("/") #metodo http y direccion que el usuario tiene que ingresar para llamar la api, que debe hacer la funcion de la api app 
async def root():
    return{"message": "hello world 2"}

    ## uvicourn reload para re lanzar el servidos cuando haya un cambio