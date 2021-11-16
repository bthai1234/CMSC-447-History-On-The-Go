from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.contrib.auth import get_user_model
from tour_app.models import Itinerary, Itinerary_location
from decimal import *


# Create your tests here.
class IndexViewTests(TestCase):
    def test_load_index_page(self):
        response = self.client.get(reverse('tour_app:index'))
        self.assertEqual(response.status_code, 200)
    
class itineraryTests(TestCase):
    def setUp(self):
        #self.user = get_user_model().objects.create_user(username='testCaseUser', email='testCaseUser@gmail.com', password='12345')
        self.factory = RequestFactory()
        self.c = Client()

        #Register test user though the register page view 
        response = self.c.post(reverse('tour_app:registerPage'), {'username': 'testCaseUser', 'email': 'testCaseUser@gmail.com', 'password1': '@Cmsc447', 'password2': '@Cmsc447'}, follow=True)
        self.assertEquals(response.status_code, 200)


    def tearDown(self):
        u = get_user_model().objects.get(username="testCaseUser")
        u.delete()

    #Tests that a default itinerary list is created upon initial account creation
    def test_default_itinerary_creation(self):
        user = get_user_model().objects.get(username="testCaseUser")
        self.assertEquals(user.username, "testCaseUser")
        itinerary = Itinerary.objects.get(itinerary_name="testCaseUser Itinerary")
        self.assertEquals(itinerary.itinerary_name , user.username + " Itinerary" )

    #Test that a location is saved to the default itinerary of the user.
    def test_locationSave(self):
        user = get_user_model().objects.get(username="testCaseUser")
        self.c.force_login(user)
        response = self.c.post(reverse('tour_app:saveLocation'), {'place_name': 'TestLocation', 'lat': 39.290385, 'lng': -76.612189}, follow=True)
        
        itinerary = Itinerary.objects.get(itinerary_name="testCaseUser Itinerary")
        db_entry = Itinerary_location.objects.get(loc_name = 'TestLocation', id= itinerary.id)
        self.assertEquals('TestLocation', db_entry.loc_name)
        self.assertEquals(Decimal('39.290385'), db_entry.latitude)
        self.assertEquals(Decimal('-76.612189'), db_entry.longitude)

    #tests that a itinerary and its associated locations is deleted upon deletion of a user in the data base.
    def test_itineraryDelete(self):
        user = get_user_model().objects.get(username="testCaseUser")
        self.c.force_login(user)
        response = self.c.post(reverse('tour_app:saveLocation'), {'place_name': 'TestLocation', 'lat': 39.290385, 'lng': -76.612189}, follow=True)
        itinerary_id = Itinerary.objects.get(itinerary_name="testCaseUser Itinerary").id
        
        u = get_user_model().objects.get(username="testCaseUser")
        u.delete()

        #test that the itinerary that was create for the user upon account creation is no longer in the database after deletion of user
        try:
            itinerary = Itinerary.objects.get(itinerary_name="testCaseUser Itinerary")
        except Exception as e:
            self.assertEquals("Itinerary matching query does not exist.", str(e))

        #test that the location that was saved for the associated itinerary is no longer in the database after deletion of user
        try:
            db_entry = Itinerary_location.objects.get(loc_name = 'TestLocation', id= itinerary_id)
        except Exception as e:
            self.assertEquals("Itinerary_location matching query does not exist.", str(e))
            
        response = self.c.post(reverse('tour_app:registerPage'), {'username': 'testCaseUser', 'email': 'testCaseUser@gmail.com', 'password1': '@Cmsc447', 'password2': '@Cmsc447'}, follow=True)

    
        





