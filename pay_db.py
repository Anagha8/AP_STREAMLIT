import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import plotly.express as px

# Connect to MongoDB
client = MongoClient("mongodb+srv://ambipoly:an822001@cluster0.xsjsved.mongodb.net/?retryWrites=true&w=majority")
db = client['AP_PAYMENT']
collection = db['PAYMENT']

def add_pay_data(i_no,i_date,amt,stat,r_date):
    try:
        # Convert po_date and deadline to datetime.datetime objects
        i_date = datetime.combine(i_date, datetime.min.time())
        document={
        'Invoice Number':i_no,
        'Invoice Date':i_date,
        'Payment Amount':amt,
        'Payment Status':stat,
        'Received Date':r_date}

        result = collection.insert_one(document)
        print("Data added successfully. Inserted document ID:", result.inserted_id)
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False

def update_pay_data(i_no,i_date,amt,stat,r_date):
    try:
        filter_query={"Invoice Number":i_no}
        update_query = {"$set": {'Invoice Date':i_date,'Payment Amount':amt,'Payment Status':stat,'Received Date':r_date}}

        # Perform the update operation
        result = collection.update_one(filter_query, update_query)

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

def search_by_io_number(i_no):
    try:
        query = {"Invoice Number": i_no}
        results = collection.find(query)
        df= pd.DataFrame(list(results))  
        df=df.drop('_id',axis=1)
        return df
    except Exception as e:
        print("An error occurred:", e)
        return pd.DataFrame()  

def delete_pay_data(i_no):
    try:
        query = {"Invoice Number": i_no}
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

def calculate_payment_counts():
    cursor = collection.find({}, {"Payment Amount": 1, "_id": 0})
    amounts = [doc["Payment Amount"] for doc in cursor]
    return pd.DataFrame(amounts, columns=["Payment Amount"])

def draw_pie_chart_pay(data):
    fig = px.pie(data, names="Payment Amount", title="Payment Status Distribution",height=300,width=300)
    return fig

def find_pay_data():
    cursor = collection.find({})
    data = list(cursor)
    return pd.DataFrame(data)