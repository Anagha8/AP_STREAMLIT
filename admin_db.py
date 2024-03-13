import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import pymongo

# Connect to MongoDB Order
client = MongoClient("mongodb+srv://ambipoly:an822001@cluster0.xsjsved.mongodb.net/?retryWrites=true&w=majority")
db = client['AP_ORDER']
collection = db['ORDER']

collection.delete_many({})

# Connect to  Material
client = MongoClient("mongodb+srv://ambipoly:an822001@cluster0.xsjsved.mongodb.net/?retryWrites=true&w=majority")
db = client['AP_MATERIAL']
collection = db['MATERIAL']
collection.delete_many({})
def set_mat_data(mat_name, mat_exis, mat_req):
    try:
        document = {
            'Material Composition': "",
            'Material Required': 0,
            'Material Available': 0
        }

        # Insert the document into the collection
        result = collection.insert_one(document)
        print("Data added successfully. Inserted document ID:", result.inserted_id)
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False
# Connect to MongoDB Tools
client = MongoClient("mongodb+srv://ambipoly:an822001@cluster0.xsjsved.mongodb.net/?retryWrites=true&w=majority")
db = client['AP_TOOLS']
collection = db['TOOLS']

collection.delete_many({})

# Connect to MongoDB Payment
client = MongoClient("mongodb+srv://ambipoly:an822001@cluster0.xsjsved.mongodb.net/?retryWrites=true&w=majority")
db = client['AP_PAYMENT']
collection = db['PAYMENT']

collection.delete_many({})