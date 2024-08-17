"""
DatabaseConnection.py
Author: Nathan Wilson
Contact: nathan.wilson3@outlook.com
Date: 2024-07-21
Version: 1.0
Purpose: This module handles the connection to the MongoDB database.
Issues: None known
"""

from pymongo import MongoClient
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class DatabaseConnection:
    """
    Handles connection to the MongoDB database.
    """

    def __init__(self, connection_string, db_name):
        """
        Initialize the DatabaseConnection object with the given connection string and database name.

        :param connection_string: MongoDB connection string
        :param db_name: Name of the database to connect to
        """
        try:
            # Debugging statements to check the values
            print(f"Connection String: {connection_string}")
            print(f"Database Name: {db_name}")

            self.client = MongoClient(connection_string)
            self.database = self.client[db_name]
            logging.info(f"Connected to database: {db_name}")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def get_collection(self, collection_name):
        """
        Get a collection from the connected database.

        :param collection_name: Name of the collection to retrieve
        :return: Collection object
        """
        return self.database[collection_name]

if __name__ == '__main__':
    # Read connection string and database name from environment variables
    connection_string = os.getenv("MONGO_CONNECTION_STRING")
    db_name = os.getenv("DB_NAME")
    
    # Test the connection
    try:
        db_conn = DatabaseConnection(connection_string, db_name)
        print(f"Successfully connected to the database: {db_name}")
        collection = db_conn.get_collection("AnimalShelter")
        print(f"Successfully accessed the collection: AnimalShelter")
    except ConnectionError as e:
        print(e)
