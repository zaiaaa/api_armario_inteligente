from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://gustavozaia75:niFKgF8yAxAonvUm@armariointeligente.ejtutce.mongodb.net/?retryWrites=true&w=majority&appName=armarioInteligente"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.armario_inteligente

#Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Connection succesfull!")
except Exception as e:
    print(e)
