import os
LOCAL = 'mongodb://localhost:27017/'
MONGODB_IP = os.environ.get("MONGODB_IP", "")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD", "")
MONGODB_PORT = os.environ.get("MONGODB_PORT", "")
MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME", "")
MONGO_URL = 'mongodb://user:<password>@user-shard-00-00.hyenn.mongodb.net:27017,user-shard-00-01.hyenn.mongodb.net:27017,user-shard-00-02.hyenn.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-13v9ws-shard-0&authSource=admin&retryWrites=true&w=majority'
# MONGO_URL = 'mongodb://'+MONGODB_USERNAME +':'+ MONGODB_PASSWORD+'@'+ MONGODB_IP+':'+ MONGODB_PORT +'/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
DB = "crypto-news"
REDIS_IP = os.environ.get("REDIS_IP", "")
REDIS_PORT = os.environ.get("REDIS_PORT", "")