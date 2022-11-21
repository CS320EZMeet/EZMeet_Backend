from django.test import SimpleTestCase
import json

class findMidpointView(SimpleTestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/midpoint/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertEqual(content, 'Welcome page to findMidpoint')
    
    def test_midpoint_for_static_group(self):
        response = self.client.get('/midpoint/7/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        latitudeCheck = (content['data']['Latitude'] != None)
        longitudeCheck = (content['data']['Longitude'] != None)
        self.assertTrue(latitudeCheck)
        self.assertTrue(longitudeCheck)
    
    def test_midpoint_for_empty_group(self):
        response = self.client.get('/midpoint/2/')
        self.assertEqual(response.status_code, 404)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Group not found')