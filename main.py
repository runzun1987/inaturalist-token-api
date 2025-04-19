
from fastapi import FastAPI,HTTPException

from models import Credentials, Token
from services.inaturalist_service import fetch_inaturalist_token
from services.mongodb import get_token_mongodb, post_token_mongodb

app=FastAPI(title="Token Retriever")







@app.get("/")
async def home():
    return "Healthy yay!!!!"


@app.post("/get_token")
async def get_token(credentials: Credentials):
    try:
        token = fetch_inaturalist_token(credentials.email, credentials.password)
        return {"api_token": token}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))




@app.get("/get_token-from-database")
async def get_token():
    try:
       return get_token_mongodb()
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.post("/post-token-to-database")
async def post_token_db(token: Token):

    try:
        return post_token_mongodb(token=token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))






if __name__=="__main__":

    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)