from fastapi import FastAPI
from routes.route import router

app = FastAPI()
app.include_router(router)


def testConnection():
    from pymongo.mongo_client import MongoClient
    uri = "mongodb+srv://tharunselvats:5azMDrDgxTxI0XMp@crunchynutcluster.vwb407j.mongodb.net/"

    # Create a new client and connect to the server:
    client = MongoClient(uri)
    
    # Ping the server to test the connection:
    try:
        client.admin.command('ping')
        print("You are Connected! Successfully pinged your deployment")
    except Exception as e:
        print(e)


# testConnection()

