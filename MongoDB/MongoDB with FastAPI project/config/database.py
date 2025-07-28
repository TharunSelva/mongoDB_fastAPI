from pymongo import MongoClient

client = MongoClient("mongodb+srv://tharunselvats:5azMDrDgxTxI0XMp@crunchynutcluster.vwb407j.mongodb.net/")

db = client.todo_db
collection_name = db["todo_collection"]