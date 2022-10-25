from django.test import SimpleTestCase
import json

class accountProfileView(SimpleTestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/user/Yeet')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        user = content['data']['name']
        self.assertEqual(user,'Yeet')
        email = content['data']['email']
        self.assertEqual(email,'yeet@yahoo.com')