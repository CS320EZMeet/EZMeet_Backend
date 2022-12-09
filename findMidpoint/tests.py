from django.test import SimpleTestCase, TestCase
from django.urls import reverse
import json
from .views import findPlacesHepler, calcMidpoint
from .models import *

class findMidpointView(SimpleTestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/midpoint/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertEqual(content, 'Welcome page to findMidpoint')
    
    def test_midpoint_for_empty_group(self):
        response = self.client.get('/midpoint/2/')
        self.assertEqual(response.status_code, 404)
        content = json.loads(response.content)
        self.assertEqual(content['message'], 'Group not found')
    
    def test_match_preferenceID_to_Bools(self):
        res = matchPreferenceIDtoBools(30)
        self.assertEqual(res, (True, True, True, True, False))
    
    def test_groupUsers_returns_correct_users(self):
        users = groupUsers(46)
        self.assertEqual(users, ["oof", "NewAccountTest"])
    
    def test_userPreferences_return_correct_preference(self):
        res = userPreferences(groupUsers(46))
        self.assertEqual(res, [27, 31])

    def test_userLocations_returns_correct_location(self):
        res = userLocations(groupUsers(46))
        self.assertEqual(res, [(42.3936974, -72.5317708), (42.3936974, -72.5317708)])

    def test_findPlaces_helper(self):
        locations = [[42.394332735132956, -72.52554483449866], [42.37672577037395, -72.51821887466069]]
        midpoint = calcMidpoint(locations)
        places = findPlacesHepler(midpoint, "campground")
        self.assertEqual(places, [('Khalsa Camp', 42.4556078, -72.5239966, '189 Long Plain Rd, Leverett, MA 01054, USA')])

