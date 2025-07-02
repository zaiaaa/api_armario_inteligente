from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.environ.get("MONGO_URI")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.armario_inteligente

#Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Connection succesfull!")
except Exception as e:
    print(e)
