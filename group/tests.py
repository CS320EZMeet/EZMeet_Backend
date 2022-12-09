from django.test import SimpleTestCase
from django.test.client import JSON_CONTENT_TYPE_RE
import json

class groupView(SimpleTestCase):
    def test_user_group(self):
        response = self.client.get('/group/oof/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Group found')

    def test_user_not_in_group(self):
        response = self.client.get('/group/jack9/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'User not in a group')
    
    def test_groupjoin_user_not_in_body(self):
        data={"notIt": "notIt"}
        response = self.client.post('/group/invite/46/', data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'userName not specified in body')
    
    def test_groupleave_invalid_user(self):
        data={'userName': 'neverWillBeAUser'}
        response = self.client.post('/group/leave/46/', data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'User not found')
    
    def test_groupleave_user_not__found_in_group(self):
        data={'userName': 'Broski'}
        response = self.client.post('/group/leave/46/', data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'User not found in group')