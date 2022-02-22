from calendar import day_abbr
from re import S
from turtle import pos
from fastapi import APIRouter,Request

from ..models.models import Article
from ..config.database import collection

import datetime

api_router = APIRouter()

def addreview(l1,l2,l3, doc):
        for r in doc['One_word_Reviews']:
            if r not in l1:
                l1.append(r)
        for r in doc['Two_word_Reviews']:
            l2.append(r)
        for r in doc['Three_word_Reviews']:
            l3.append(r)

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

@api_router.get("/api/articles/sentiment/")
async def get_sentiment(request: Request): # Gives the weekly sentiment of the provided coin  
    # Return overall sentiment, list of words for sentiment.
    info = await request.json()
    coin = info['coin']
    reqdate = datetime.datetime.now() - datetime.timedelta(weeks = 4, days= 17)
    cursor = collection.find({})
    articles = []
    pos1word = []
    pos2word = []
    pos3word = []
    neg1word = []
    neg2word = []
    neg3word = []
    neu1word = []
    neu2word = []
    neu3word = []
    poscount = 0
    negcount = 0
    neucount = 0
    for doc in cursor:
        if (doc['Coin'] == coin):
            strdate = doc['Time']
            date = datetime.datetime.strptime(strdate, '%Y-%m-%d')
            if date > reqdate:
                item = Article(**doc)
                if doc['score'] > 0.5:
                    addreview(pos1word, pos2word, pos3word, doc)
                    poscount = poscount+1
                elif doc['score'] < -0.5:
                    addreview(neg1word, neg2word, neg3word, doc)
                    negcount = negcount+1
                else:
                    addreview(neu1word, neu2word, neu3word, doc)
                    neucount = neucount+1
                articles.append(item)

    totalcount = len(articles) 

    if len(articles) == 0:
        return "No Articles Found"
    
    words = {
                "PositiveWords" : { 'Oneword': pos1word, "Twoword": pos2word, "Threeword": pos3word},
                "NegativeWords" : {"Oneword" : neg1word, "Twoword" : neg2word,"Threeword" : neg3word},
                "NeutralWords" : {"Oneword" : neu1word, "Twoword" : neu2word,"Threeword" : neu3word}
            }
    return {"Total": totalcount, "Positive" : poscount, "Negative" : negcount, "Neutral" : neucount, "Words" : words }

# async def get_todo(id: str):
#     return todos_serializer(collection_name.find_one({"_id": ObjectId(id)}))

