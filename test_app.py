import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import EXECUTE

class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = EXECUTE()
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_programs(self):
        newRequest = self.client().get("/programs")
        data = json.loads(newRequest.data)
        #
        self.assertEqual(data["success"], True)
        self.assertTrue(data["programs"])

    def test_get_coders(self):
        newRequest = self.client().get("/coders")
        data = json.loads(newRequest.data)
        #
        self.assertEqual(data["success"], True)
        self.assertTrue(data["coders"])

    def test_valid_new_program(self):
        newProgram = { "title": "Code4UDACITY", "description": "MY NEW PROJECT", "username": "1999xCoder" }
        newRequest = self.client().post("/programs", json=newProgram)
        data = json.loads(newRequest.data)
        #
        self.assertEqual(data["success"], True)
        self.assertTrue(data["program"])

    def test_invalid_new_program(self):
        newProgram = { "description": "MY NEW PROJECT", "name": "1999xCoder" }
        newRequest = self.client().post("/programs", json=newProgram)
        data = json.loads(newRequest.data)
        #
        self.assertEqual(data["success"], False)
        self.assertEqual(data["status"], 422)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_valid_delete_program(self):
        newProgram = { "title": "Code4UDACITY", "description": "MY NEW PROJECT", "username": "1999xCoder" }
        newRequest = self.client().post("/programs", json=newProgram)
        data = json.loads(newRequest.data)
        newRequest = self.client().delete("/programs/1")
        data = json.loads(newRequest.data)
        #
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"])

    def test_invalid_delete_program(self):
        newRequest = self.client().delete("/programs/abcde")
        data = json.loads(newRequest.data)
        #
        self.assertEqual(data["success"], False)
        self.assertEqual(data["status"], 422)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_valid_patch_program(self):
        newProgram = { "title": "Code4UDACITY", "description": "MY NEW PROJECT", "username": "1999xCoder" }
        newRequest = self.client().post("/programs", json=newProgram)
        data = json.loads(newRequest.data)
        updateProgram = { "title": "Code4UDACITY", "description": "MY CAPSTONE PROJECT" }
        newRequest = self.client().patch("/programs/1", json=updateProgram)
        data = json.loads(newRequest.data)
        #
        self.assertEqual(data["success"], True)
        self.assertEqual(data["program"])

    def test_invalid_patch_program(self):
        newRequest = self.client().patch("/programs/abcde")
        data = json.loads(newRequest.data)
        #
        self.assertEqual(data["success"], False)
        self.assertEqual(data["status"], 422)
        self.assertEqual(data["message"], "Unprocessable Entity")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
