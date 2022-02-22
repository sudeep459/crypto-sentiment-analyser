import os
LOCAL = 'mongodb://localhost:27017/'
MONGODB_IP = os.environ.get("MONGODB_IP", "")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD", "")
MONGODB_PORT = os.environ.get("MONGODB_PORT", "")
MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME", "")
MONGO_URL = 'mongodb://'+MONGODB_USERNAME +':'+ MONGODB_PASSWORD+'@'+ MONGODB_IP+':'+ MONGODB_PORT +'/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
DB = "crypto-news"
REDIS_IP = os.environ.get("REDIS_IP", "")
REDIS_PORT = os.environ.get("REDIS_PORT", "")