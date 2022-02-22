from pymongo import MongoClient

from config import *

client = MongoClient(MONGO_URL)

db = client['crypto-news']

collection = db["inventory"]