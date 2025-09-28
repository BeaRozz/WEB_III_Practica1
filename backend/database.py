# app/database.py
from pymongo import MongoClient

# Conexión centralizada
mongo_client = MongoClient("mongodb://admin_user:web3@practicas-mongo-1:27017/")
database = mongo_client.practica1
collection_historial = database.historial