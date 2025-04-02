# api/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import SampleModel

class SampleModelTests(TestCase):
    def setUp(self):
        self.sample = SampleModel.objects.create(
            name="Sample Name", description="Sample Description"
        )

    def test_sample_model_create(self):
        self.assertEqual(self.sample.name, "Sample Name")
        self.assertTrue(self.sample.id)

    def test_api_test_endpoint(self):
        url = reverse('test_endpoint')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello, World!"})
