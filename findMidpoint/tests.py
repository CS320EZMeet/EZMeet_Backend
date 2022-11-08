from django.test import SimpleTestCase
import json

class midpointIndexView(SimpleTestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/midpoint/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertEqual(content, 'Welcome page to findMidpoint')