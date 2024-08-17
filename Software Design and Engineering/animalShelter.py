"""
animalShelter.py
Author: Nathan Wilson
Contact: nathan.wilson3@outlook.com
Date: 2024-07-21
Version: 1.1
Purpose: This module provides an interface for CRUD operations on the AnimalShelter collection in MongoDB.
Issues: None known
"""

from DatabaseConnection import DatabaseConnection
from crudOperations import CreateOperation, ReadOperation, UpdateOperation, DeleteOperation
import pymongo
import logging

logging.basicConfig(level=logging.INFO)

class AnimalShelter:
    """
    The AnimalShelter class provides an interface for CRUD operations on the AnimalShelter collection in MongoDB.
    """

    def __init__(self, connection_string, db_name, collection_name):
        """
        Initialize the AnimalShelter with a database connection and collection name.

        :param connection_string: MongoDB connection string
        :param db_name: Name of the database
        :param collection_name: Name of the collection
        """
         # Establish a connection to the database
        self.db_connection = DatabaseConnection(connection_string, db_name)
         # Access the specified collection
        self.collection = self.db_connection.get_collection(collection_name)

         # Initialize CRUD operation handlers
        self.create_operation = CreateOperation(self.collection)
        self.read_operation = ReadOperation(self.collection)
        self.update_operation = UpdateOperation(self.collection)
        self.delete_operation = DeleteOperation(self.collection)

        # Ensure necessary indexes are created on the collection
        self.ensure_indexes()

    def ensure_indexes(self):
        """
        Ensure that necessary indexes are created on the collection.
        Reduced time complexity from O(n) to O (log n)
        """
        # Example index creation (add actual index creation code here)
        # self.collection.create_index([("field_name", pymongo.ASCENDING)], unique=True)

        indexes = self.collection.index_information()
        if "animal_type_1" not in indexes:
            self.collection.create_index("animal_type")
        if "breed_1" not in indexes:
            self.collection.create_index("breed")
        if "date_of_birth_1" not in indexes:
            self.collection.create_index("date_of_birth")
        if "datetime_1" not in indexes:
            self.collection.create_index("datetime")
        if "outcome_type_1" not in indexes:
            self.collection.create_index("outcome_type")
        if "location_2dsphere" not in indexes:
            self.collection.create_index([("location", pymongo.GEOSPHERE)])

        # Compound indexes
        if "animal_type_breed_idx" not in indexes:
            self.collection.create_index([("animal_type", pymongo.ASCENDING), ("breed", pymongo.ASCENDING)])
        if "date_of_birth_animal_id_idx" not in indexes:
            self.collection.create_index([("date_of_birth", pymongo.ASCENDING), ("animal_id", pymongo.ASCENDING)])
        if "name_animal_type_idx" not in indexes:
            self.collection.create_index([("name", pymongo.ASCENDING), ("animal_type", pymongo.ASCENDING)])

    def create(self, data):
        """
        Create a new document in the collection.

        Time Complexity: O(1) on average, but O(n) in the worst case if a rehash is needed.

        :param data: Dictionary representing the document to be created
        :return: Boolean indicating success of the operation
        """
        return self.create_operation.execute(data)

    def read(self, query, projection=None):
        """
        Read documents from the collection based on the query.
        Added the use of projection to make the read operations more efficient by allowing the user to include only the fields
        that are absolutely necessary

        Time Complexity: O(log n) when used with well-designed indexes, and O(n) on full collection scans or non-indexed fields

        :param query: Dictionary representing the query criteria
        :param projection: Dictionary representing the fields to include or exclude
        :return: List of documents matching the query
        """
        return self.read_operation.execute(query, projection)

    def update(self, query, update_data):
        """
        Update a document in the collection based on the query.

        Time Complexity: O(log n) When used in conjuction with indexed fields, non-indexed fields is O(n), and the actual modification
         of a document is O(1)
        
        :param query: Dictionary representing the query criteria
        :param update_data: Dictionary representing the update data
        :return: Boolean indicating success of the operation
        """
        return self.update_operation.execute(query, update_data)

    def delete(self, query):
        """
        Delete a document from the collection based on the query.

        Time Complexity: Best case is O(log n) when used with indexed fields, worst case is O(n) when used without indexes

        :param query: Dictionary representing the query criteria
        :return: Boolean indicating success of the operation
        """
        return self.delete_operation.execute(query)
