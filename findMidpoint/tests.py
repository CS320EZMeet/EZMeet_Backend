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
        users = groupUsers(4)
        self.assertEqual(users, ["Tinky Winky", "Top G"])
    
    def test_userPreferences_return_correct_preference(self):
        res = userPreferences(groupUsers(8))
        self.assertEqual(res, [28, 30])

    def test_userLocations_returns_correct_location(self):
        res = userLocations(groupUsers(4))
        self.assertEqual(res, [(-58.94865, -173.78905), (-106.24902, -28.07315)])

    def test_findPlaces_helper(self):
        locations = [[42.394332735132956, -72.52554483449866], [42.37672577037395, -72.51821887466069]]
        midpoint = calcMidpoint(locations)
        places = findPlacesHepler(midpoint, "campground")
        self.assertEqual(places, [('Khalsa Camp', 42.4556078, -72.5239966, '189 Long Plain Rd, Leverett, MA 01054, USA')])

    def test_finding_common_preferences(self):
        #where all users in groups has a preference list
        response = self.client.get(reverse('commonPref', args=[8]))
        self.assertEqual(response.status_code, 200)
        print(response)
        content =  json.loads(response.content)
        #broski (28) and bruh(30)
        self.assertEqual(content['data'], set(['restaurantBar', 'nature', 'museum']))

    def test_finding_common_preferences_where_user_doesnt_have_preference(self):
        #where all users in groups has a preference list
        response = self.client.get('midpoint/findCommonPreferences/4/')
        self.assertEqual(response.status_code, 500)
        print(response)
        content =  json.loads(response.content)
        self.assertEqual(content['message'], "Not all user\'s in the group has their preference list filled out")
    
    def test_create_recommendation_list(self):
        response = self.client.get('midpoint/createRecommendation/8/')
        self.assertEqual(response.status_code, 200)
        print(response)
        content =  json.loads(response.content)
        self.assertEqual(content['message'], 'Successfully created recommendation List')
