from django.test import SimpleTestCase, TestCase
import json
from accountProfile.views import registerUser
from accountProfile.models import createUser

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
        response = self.client.get('/user/getLocation/NewAccountTest/')
        content = json.loads(response.content)
        success = content['success']
        self.assertEqual(success, True)
        location = content['data']
        self.assertEqual(location['latitude'], 42.3936974)
        self.assertEqual(location['longitude'], -72.5317708)

# Tests that interact with test DB
# Need permission to create DB in Postgres, so that Django can generate a test DB for these
# class accountProfileViewTestDB(TestCase):
#     def test_register_user(self):
#         body = {'method': 'POST', 'email': 'example@email.com', 'password': 'abc'}
#         print(dir(body))
#         request = self.client.post('/user/register/PenPen/', body, content_type='application/json')
#         registerUser(request, 'PenPen')
#         response = self.client.get('/user/get/PenPen/')
#         self.assertEqual(response.status_code, 200)
#         content = json.loads(response.content)
#         #user = content['data']
#         success = content['success']
#         self.assertEqual(success, True)

#     def test_create_user(self):
#         user = {'userName': 'Foo', 'password': 'Bar', 'email': 'bat@email.com'}
#         createUser(user)
#         response = self.client.get('/user/get/Foo/')
#         self.assertEqual(response.status_code, 200)
    
    # def test_update_user(self):
    #     body = {"user": {"userName": "Yeet", "password": "12345", "email": "yeet@yahoo.com", "group_id": 28, "show_location": False, "preferences": ["restaurant", "entertainment", "shopping"]}}
    #     response = self.client.put('/user/update/Yeet/', body, content_type='application/json')
    #     content = json.loads(response.content)
    #     success = content['success']
    #     self.assertEqual(success, True)