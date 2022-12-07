from django.test import SimpleTestCase
import json
from .models import findLocation

# NOTE:
# For simplicity, initial developmental testing that alters the DB (e.g. creating and updating users)
# was done through simulated use cases through the website, and direct HTTP requests to back-end endpoints.
# Once officially live for clients, more formal testing could be done in a separate class using the
# 'TestCase' module in django.test, with Create DB rights applied, as this creates a duplicate, blank, test DB,
# allowing one to repeat tests with the same data, and without tampering with the production DB.
# For our purposes, this was deemed unnecessary, as we only used sample data, and had no outside clients.

# Read-Only Tests Using Production DB
class accountProfileView(SimpleTestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/user/get/Yeet/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        user = content['data']['username']
        self.assertEqual(user,'Yeet')
        email = content['data']['email']
        self.assertEqual(email,'yeet@yahoo.com')

    def test_login_success(self):
        body = {"password": "abcde"}
        response = self.client.post('/user/login/bobby/', body, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        success = content['success']
        self.assertEqual(success, True)
        userName = content['data']['username']
        self.assertEqual(userName, 'bobby')
    
    def test_login_incorrect_username(self):
        response = self.client.post('/user/login/eebydeeby/')
        content = json.loads(response.content)
        success = content['success']
        self.assertEqual(success, False)

    def test_get_location(self):
        response = self.client.get('/user/getLocation/Yeet/')
        content = json.loads(response.content)
        success = content['success']
        self.assertEqual(success, True)
        location = content['data']
        location2 = findLocation('Yeet')
        self.assertEqual(location['latitude'], location2['latitude'])
        self.assertEqual(location['longitude'], location2['longitude'])