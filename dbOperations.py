import pandas as pd
from pymongo import MongoClient


def dbUpload():
    # Read the CSV file
    df = pd.read_csv('Prediction_Output_File/Predictions.csv')

    # Convert the data to JSON format
    data = df.to_dict('records')

    # Create a client
    client = MongoClient('mongodb://localhost:27017/')
    print("DB connected successfully")
    # Connect to the database
    db = client['thyroidDB']

    # Get the collection you want to insert the data into
    collection = db['patientsCSV']

    # Insert the data into the collection
    collection.insert_many(data)
