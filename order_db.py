import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import plotly.express as px

# Connect to MongoDB
client = MongoClient("mongodb+srv://ambipoly:an822001@cluster0.xsjsved.mongodb.net/?retryWrites=true&w=majority")
db = client['AP_ORDER']
collection = db['ORDER']

def search_by_po_number(po_number):
    try:
        query = {"PO number": po_number}
        results = collection.find(query)
        df= pd.DataFrame(list(results))  
        df=df.drop('_id',axis=1)
        return df
    except Exception as e:
        print("An error occurred:", e)
        return pd.DataFrame()  

def search_by_part_number(part_number):
    try:
        query = {"Part numbers": part_number}
        results = collection.find(query)
        df = pd.DataFrame(list(results))  
        df = df.drop('_id', axis=1)
        return df
    except Exception as e:
        print("An error occurred:", e)
        return pd.DataFrame()


def add_data(po_num, po_date, loc, deadline, mat, part_no, nos, po_val, status):
    try:
        # Convert po_date and deadline to datetime.datetime objects
        po_date = datetime.combine(po_date, datetime.min.time())
        deadline = datetime.combine(deadline, datetime.min.time())

        # Create a document to insert
        document = {
            "PO number": po_num,
            "PO date": po_date,
            "Location": loc,
            "Deadline": deadline,
            "Material": mat,
            "Part numbers": part_no,
            "Quantity": nos,
            "PO value": po_val,
            "status": status
        }

        # Insert the document into the collection
        result = collection.insert_one(document)
        print("Data added successfully. Inserted document ID:", result.inserted_id)
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False

def delete_data(po_number,part_num):
    try:
        query = {"PO number": po_number,'Part numbers':part_num}
        result = collection.delete_one(query)
        if result.deleted_count > 0:
            print("Order deleted successfully")
        else:
            print("Order not found")
    except Exception as e:
        print("An error occurred:", e)

def find_data():
    cursor = collection.find({})
    data = list(cursor)
    return data

def update_data(po_number, status,part_num):
    try:
        # Define the filter to identify the document to update
        if part_num:
            filter_query = {"PO number": po_number,'Part numbers':part_num}
        else:
            filter_query={"PO number": po_number}

        # Define the update operation
        update_query = {"$set": {"status": status}}

        # Perform the update operation
        result = collection.update_many(filter_query, update_query)

        # Check if the update was successful
        if result.modified_count > 0:
            print("Order status updated successfully")
            return True
        else:
            print("Order not found")
            return False
    except Exception as e:
        print("An error occurred:", e)
        return False
    
# Function to retrieve status data
def get_status_data():
    cursor = collection.find({}, {"status": 1, "_id": 0})
    statuses = [doc["status"] for doc in cursor]
    return pd.DataFrame(statuses, columns=["Status"])

# Function to draw pie chart
def draw_pie_chart(data):
    fig = px.pie(data, names="Status", title="Order Status Distribution")
    return fig
