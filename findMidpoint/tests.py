from django.test import SimpleTestCase
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

    def test_findPLaces_returns_correct_locations(self):
        locations = [[42.394332735132956, -72.52554483449866], [42.37672577037395, -72.51821887466069]]
        midpoint = calcMidpoint(locations)
        places, places_ids = findPlacesHepler(midpoint, "movie_theater", 1610, set())
        self.assertEqual(places, [('Amherst Cinema', 42.37513300000001, -72.52055349999999, '28 Amity St, Amherst, MA 01002, USA')])
        self.assertEqual(places_ids, {'ChIJbSj71wnS5okRsNrCKZgS3os'})
        places, places_ids = findPlacesHepler(midpoint, "movie_theater", 1610*1610, places_ids)
        self.assertEqual(places, [('Cinemark at Hampshire Mall and XD', 42.3555527, -72.54711929999999, '367 Russell St, Hadley, MA 01035, USA')])
        self.assertEqual(places_ids, {'ChIJbSj71wnS5okRsNrCKZgS3os', 'ChIJl36pLbDR5okRJTp1TrIsRRk'})
