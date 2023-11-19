from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv() 

mode = os.getenv('MODE')
db_name = os.getenv('DB_NAME')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

mongo_url = ""

if mode == 'DEV':
    mongo_url = "mongodb://localhost:27017/"
elif mode == 'PROD':
    mongo_url = f"mongodb://{db_username}:{db_password}@my-mongodb-container:27017/"

client = MongoClient(mongo_url)
database = client[db_name]
