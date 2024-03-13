import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://ambipoly:an822001@cluster0.xsjsved.mongodb.net/?retryWrites=true&w=majority")
db = client['AP_MATERIAL']
collection = db['MATERIAL']


def return_mat_data(mat_name):
    query = {'Material Composition': mat_name}
    result = collection.find_one(query)
    return pd.DataFrame([result]) if result else pd.DataFrame()

def update_mat_data(mat_name, mat_exis, mat_req):
    try:
        query = {'Material Composition': mat_name}
        update_query = {"$set": {'Material Required': mat_req, 'Material Available': mat_exis}}
        result = collection.update_one(query, update_query)
        if result.modified_count == 1:
            print("Data updated successfully")
            return True
        else:
            print("No documents matched the query")
            return False
    except Exception as e:
        print("An error occurred:", e)
        return False
