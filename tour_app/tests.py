from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class IndexViewTests(TestCase):
    def test_load_index_page(self):
        response = self.client.get(reverse('tour_app:index'))
        self.assertEqual(response.status_code, 200)
        
