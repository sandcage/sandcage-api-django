from django.test import TestCase
from django.urls import reverse

class IndexTests(TestCase):

    def test_index_view(self):
        """
        By default
        """
        response = self.client.get(reverse('apigui:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TEST")
