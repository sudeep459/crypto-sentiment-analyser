from fastapi import APIRouter,Request

from ..models.models import Article
from ..config.database import collection


api_router = APIRouter()

# retrieve
@api_router.get("/")
async def root():
    return {"Hello" : "World"}

@api_router.get("/api/articles") # Get all articles
async def get_all_articles():
    articles = []
    cursor = collection.find({})
    for document in cursor:
        articles.append(Article(**document))
    return articles

@api_router.get("/api/articles/date/") # Get articles with coin name and date 
async def get_articles(request: Request):
    info = await request.json()
    date = info['date']
    article = []
    cursor = collection.find({})
    for document in cursor:
        if (document['Time'] == date):
            item = Article(**document)
            article.append(item)
    return article

@api_router.get("/api/articles/coin/") # Get articles with coin name and date 
async def get_articles(request: Request):
    info = await request.json()
    coin = info['coin']
    article = []
    cursor = collection.find({})
    for document in cursor:
        if (document['Coin'] == coin):
            item = Article(**document)
            article.append(item)
    return article

@api_router.get("/api/articles/datecoin/") # Get articles with coin name and date 
async def get_articles(request: Request):
    info = await request.json()
    coin = info['coin']
    date = info['date']
    article = []
    cursor = collection.find({})
    for document in cursor:
        if (document['Time'] == date) & (document['Coin'] == coin):
            item = Article(**document)
            article.append(item)
    return article

# async def get_todo(id: str):
#     return todos_serializer(collection_name.find_one({"_id": ObjectId(id)}))

