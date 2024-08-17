"""
unitTest.py
Author: Nathan Wilson
Contact: nathan.wilson3@outlook.com
Date: 2024-07-21
Version: 1.0
Purpose: This script contains unit tests for the AnimalShelter class. It ensures that the CRUD operations (Create, Read, Update, Delete) are functioning correctly.
Issues: None known
"""

import unittest
from animalShelter import AnimalShelter
from bson.objectid import ObjectId

class TestAnimalShelter(unittest.TestCase):
    """
    Unit tests for the AnimalShelter class.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up the test class with a connection to the AnimalShelter collection.
        This method is called once before any tests are run.
        """
        cls.shelter = AnimalShelter(
            connection_string="mongodb+srv://nathanwilson3:kAnhKgcq4UvdmpPP@animalsheltercluster.dlcajuu.mongodb.net/?retryWrites=true&w=majority&appName=AnimalShelterCluster",
            db_name='AAC',
            collection_name='AnimalShelter'
        )
        cls.test_data = {
            "animal_id": "A123458",
            "name": "Max",
            "species": "Dog",
            "age": 2,
            "adopted": False,
            "location_lat": 30.5066578739455,
            "location_long": -97.3408780722188,
        }
        
    def setUp(self):
        """
        Ensure the test data has a unique _id and clean up the collection before each test.
        This method is called before every individual test.
        """
        self.test_data["_id"] = ObjectId()
        self.shelter.collection.delete_many({"animal_id": "A123458"})

    def test_create(self):
        """
        Test the create operation.
        This test verifies that a new animal record can be successfully created in the collection.
        """
        print("Running test_create...")
        result = self.shelter.create(self.test_data)
        self.assertTrue(result)
            
    def test_read(self):
        """
        Test the read operation.
        This test verifies that an existing animal record can be successfully read from the collection.
        """
        print("Running test_read...")
        self.shelter.create(self.test_data)
        result = self.shelter.read({"animal_id": "A123458"})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Max")

    def test_update(self):
        """
        Test the update operation.
        This test verifies that an existing animal record can be successfully updated in the collection.
        """
        print("Running test_update...")
        self.shelter.create(self.test_data)
        update_data = {"name": "Maxwell"}
        result = self.shelter.update({"animal_id": "A123458"}, update_data)
        self.assertTrue(result)
        updated_doc = self.shelter.read({"animal_id": "A123458"})
        self.assertEqual(updated_doc[0]["name"], "Maxwell")

    def test_delete(self):
        """
        Test the delete operation.
        This test verifies that an existing animal record can be successfully deleted from the collection.
        """
        print("Running test_delete...")
        self.shelter.create(self.test_data)
        result = self.shelter.delete({"animal_id": "A123458"})
        self.assertTrue(result)
        deleted_doc = self.shelter.read({"animal_id": "A123458"})
        self.assertEqual(len(deleted_doc), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
