from io import BytesIO
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Person
from django.core.files.uploadedfile import SimpleUploadedFile
import pandas as pd


class FileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    # Test a valid file upload

    def test_file_upload(self):
        excel_data = {
            "Emp_Id": [1, 2, 3],
            "Name": ["Anvi", "Chetan", "Jai"],
            "Salary": [5000, 6000, 7000],
            "Designation": ["CEO", "Developer", "Accountant"],
            "Address": ["Delhi", "Haryana", "Punjab"],
        }
        df = pd.DataFrame(excel_data)
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        excel_file = SimpleUploadedFile("test_file.xlsx", excel_buffer.read())
        response = self.client.post(
            "/upload/", {"file": excel_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["status"])
        self.assertEqual(response.data["message"], "Successfully created")

    # Test invalid file upload

    def test_invalid_file_upload(self):
        excel_data = {
            "Package": ["Anvi", "Chetan", "Jai"],
        }  # wrong information

        df = pd.DataFrame(excel_data)
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        excel_file = SimpleUploadedFile("test_file.xlsx", excel_buffer.read())
        response = self.client.post(
            "/upload/", {"file": excel_file}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["status"])
        self.assertEqual(response.data["message"], "Please Upload a valid file")

    # Test no file upload

    def test_no_file_upload(self):
        response = self.client.post("/upload/", {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["status"])
        self.assertEqual(response.data["message"], "Please Upload a valid file")


class PersonTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create Person object
        Person.objects.create(
            emp_id=1,
            name="John",
            salary=5000,
            designation="Programmer",
            address="Delhi, India",
        )
        
    # Test get Person data by valid name

    def test_get_person(self):
        response = self.client.get("/persons/by_name/", {"name": "John"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "John")
    
    # Test person data response with wrong or blank name
    
    def test_person_not_found(self):
        response = self.client.get("persons/by_name/", {"name": "Happy"})
        another_response = self.client.get("persons/by_name/", {})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(another_response.status_code, status.HTTP_404_NOT_FOUND)
