import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient("mongodb+srv://ambipoly:an822001@cluster0.xsjsved.mongodb.net/?retryWrites=true&w=majority")
db = client['AP_TOOLS']
collection = db['TOOLS']

def add_tool_data(po_num,po_date,part_nos,tool_exis,tool_cost):
    try:
        # Convert po_date and deadline to datetime.datetime objects
        po_date = datetime.combine(po_date, datetime.min.time())
        document = {
            'PO Number':po_num,
            'PO Date':po_date,
            'Part Number': part_nos,
            'Tool status': tool_exis,
            'Tool Cost': tool_cost
        }

        # Insert the document into the collection
        result = collection.insert_one(document)
        print("Data added successfully. Inserted document ID:", result.inserted_id)
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False


def search_tool_by_po_number(po_number):
    try:
        query = {"PO Number": po_number}
        results = collection.find(query)
        df= pd.DataFrame(list(results))  
        df=df.drop('_id',axis=1)
        return df
    except Exception as e:
        print("An error occurred:", e)
        return pd.DataFrame()  

def search_tool_by_part_number(part_number):
    try:
        query = {"Part Number": part_number}
        results = collection.find(query)
        df = pd.DataFrame(list(results))  
        df = df.drop('_id', axis=1)
        return df
    except Exception as e:
        print("An error occurred:", e)
        return pd.DataFrame()

def update_tool_data(po_number,status, part_num):
    try:
        # Define the filter to identify the document to update
        if part_num:
            filter_query = {"PO Number": po_number, 'Part Number': part_num}
        else:
            filter_query = {"PO Number": po_number}

        # Define the update operation
        update_query = {"$set": {"Tool status": status}}

        # Perform the update operation
        result = collection.update_many(filter_query, update_query)

        # Check if the update was successful
        if result.modified_count > 0:
            print("Tool status updated successfully")
            return True
        else:
            print("Tool not found")
            return False
    except Exception as e:
        print("An error occurred:", e)
        return False

