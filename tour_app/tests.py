from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.contrib.auth import get_user_model
from tour_app.models import Itinerary, Itinerary_location
from django.contrib import auth
from decimal import *


# Create your tests here.
class IndexViewTests(TestCase):
    def test_load_index_page(self):
        response = self.client.get(reverse('tour_app:index'))
        self.assertEqual(response.status_code, 200)


class itineraryTests(TestCase):
    def setUp(self):
        # self.user = get_user_model().objects.create_user(username='testCaseUser', email='testCaseUser@gmail.com', password='12345')
        self.factory = RequestFactory()
        self.c = Client()

        # Register test user though the register page view
        response = self.c.post(reverse('tour_app:registerPage'),
                               {'username': 'testCaseUser', 'email': 'testCaseUser@gmail.com', 'password1': '@Cmsc447',
                                'password2': '@Cmsc447'}, follow=True)
        self.assertEquals(response.status_code, 200)

    def tearDown(self):
        u = get_user_model().objects.get(username="testCaseUser")
        u.delete()

    # Tests that a default itinerary list is created upon initial account creation
    def test_default_itinerary_creation(self):
        user = get_user_model().objects.get(username="testCaseUser")
        self.assertEquals(user.username, "testCaseUser")
        itinerary = Itinerary.objects.get(itinerary_name="testCaseUser Itinerary")
        self.assertEquals(itinerary.itinerary_name, user.username + " Itinerary")

    # Test that a location is saved to the default itinerary of the user.
    def test_locationSave(self):
        user = get_user_model().objects.get(username="testCaseUser")
        self.c.force_login(user)
        response = self.c.post(reverse('tour_app:saveLocation'),
                               {'place_name': 'TestLocation', 'lat': 39.290385, 'lng': -76.612189}, follow=True)

        itinerary = Itinerary.objects.get(itinerary_name="testCaseUser Itinerary")
        db_entry = Itinerary_location.objects.get(loc_name='TestLocation', id=itinerary.id)
        self.assertEquals('TestLocation', db_entry.loc_name)
        self.assertEquals(Decimal('39.290385'), db_entry.latitude)
        self.assertEquals(Decimal('-76.612189'), db_entry.longitude)

    # tests that a itinerary and its associated locations is deleted upon deletion of a user in the data base.
    def test_itineraryDelete(self):
        user = get_user_model().objects.get(username="testCaseUser")
        self.c.force_login(user)
        response = self.c.post(reverse('tour_app:saveLocation'),
                               {'place_name': 'TestLocation', 'lat': 39.290385, 'lng': -76.612189}, follow=True)
        itinerary_id = Itinerary.objects.get(itinerary_name="testCaseUser Itinerary").id

        u = get_user_model().objects.get(username="testCaseUser")
        u.delete()

        # test that the itinerary that was create for the user upon account creation is no longer in the database after deletion of user
        try:
            itinerary = Itinerary.objects.get(itinerary_name="testCaseUser Itinerary")
        except Exception as e:
            self.assertEquals("Itinerary matching query does not exist.", str(e))

        # test that the location that was saved for the associated itinerary is no longer in the database after deletion of user
        try:
            db_entry = Itinerary_location.objects.get(loc_name='TestLocation', id=itinerary_id)
        except Exception as e:
            self.assertEquals("Itinerary_location matching query does not exist.", str(e))

        response = self.c.post(reverse('tour_app:registerPage'),
                               {'username': 'testCaseUser', 'email': 'testCaseUser@gmail.com', 'password1': '@Cmsc447',
                                'password2': '@Cmsc447'}, follow=True)


# This class is the super class of RegisterPageTest and LoginPageTest
class BaseCase(TestCase):
    def setUp(self):
        self.registerPage = reverse('tour_app:registerPage')
        self.loginPage = reverse('tour_app:loginPage')
        self.index = reverse('tour_app:index')
        self.mapPage = reverse('tour_app:mapPage')
        
        self.c = Client()
        # Register test user though the register page view
        self.c.post(reverse('tour_app:registerPage'),
                    {'username': 'username', 'email': 'testCaseUser@gmail.com', 'password1': '@Cmsc447',
                     'password2': '@Cmsc447'}, follow=True)
        return super().setUp()


class RegisterPageTest(BaseCase):
    # This test is to test the register page load properly and load correct html file
    def test_load_register_page(self):
        response = self.client.get(self.registerPage)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tour_app/registration.html')

    # This test is to test if a valid user's registration will go to the database or not
    def test_user_in_database(self):
        user = get_user_model().objects.get(username="username")
        self.assertEquals(user.username, "username")

    # This test SUPPOSE TO FAIL since the registration wouldn't succeed
    #################### NO VALID EMAIL ####################
    # Comment this function out if you don't want a long line of trace back
    # def test_user_not_valid_email(self):
    #     # Register test user though the register page view
    #     self.c.post(reverse('tour_app:registerPage'),
    #                 {'username': 'username1', 'email': 'testCaseUscom', 'password1': '@Cmsc447',
    #                  'password2': '@Cmsc447'}, follow=True)
    #     user = get_user_model().objects.get(username="username1")
    #     self.assertEquals(user.username, "username1")

    # This test SUPPOSE TO FAIL since the registration wouldn't succeed
    #################### USED EMAIL ####################
    # NOTES: In our web, if we successfully register an account, it will return a login page.
    # In our web, if we fail to register an account, it will return a blank register page.
    # Otherwise, it will route us to the login page.
    # Comment this function out if you don't want a long line of trace back
    # def test_used_email(self):
    #     # Register test user though the register page view
    #     self.c.post(reverse('tour_app:registerPage'),
    #                 {'username': 'username11', 'email': 'tpham1@gmail.com', 'password1': '@Cmsc447',
    #                  'password2': '@Cmsc447'}, follow=True)
    #     self.c.post(reverse('tour_app:registerPage'),
    #                 {'username': 'username12', 'email': 'tpham1@gmail.com', 'password1': '@Cmsc44712',
    #                  'password2': '@Cmsc44712'}, follow=True)
    #     response = self.client.get(self.registerPage)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'tour_app/registerPage.html')

    # This test SUPPOSE TO FAIL since the registration wouldn't succeed
    #################### NO MATCHING PASSWORDS ####################
    # Comment this function out if you don't want a long line of trace back
    # def test_user_not_matching_passwords(self):
    #     # Register test user though the register page view
    #     self.c.post(reverse('tour_app:registerPage'),
    #                 {'username': 'username2', 'email': 'testCaseUser@gmail.com', 'password1': '@Cmsc4547',
    #                  'password2': '@Cmsc447'}, follow=True)
    #     user = get_user_model().objects.get(username="username2")
    #     self.assertEquals(user.username, "username2")

    # This test SUPPOSE TO FAIL since the registration wouldn't succeed
    #################### SHORT PASSWORDS ####################
    # Comment this function out if you don't want a long line of trace back
    # def test_user_short_passwords(self):
    #     # Register test user though the register page view
    #     self.c.post(reverse('tour_app:registerPage'),
    #                 {'username': 'username3', 'email': 'testCaseUser@gmail.com', 'password1': '@',
    #                  'password2': '@'}, follow=True)
    #     user = get_user_model().objects.get(username="username3")
    #     self.assertEquals(user.username, "username3")


# This class is to test Login Page
class LoginPageTest(BaseCase):
    # This test is to test the register page load properly and load correct html file
    def test_load_login_page(self):
        response = self.client.get(self.loginPage)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tour_app/login.html')

    def test_login_successful(self):
        user = get_user_model().objects.get(username="username")
        assert user.is_authenticated

    # This test SUPPOSE TO FAIL since the registration wouldn't succeed
    # Comment this function out if you don't want a long line of trace back
    # def test_login_fail(self):
    #     self.c.post(reverse('tour_app:registerPage'),
    #                 {'username': 'username4', 'email': 'testCaseUser@gmail.com', 'password1': 'o12',
    #                  'password2': '@Conmeo12'}, follow=True)
    #     user = get_user_model().objects.get(username="username4")
    #     assert user.is_authenticated

    # When the we log in, if we can't log in, the app would return a login page again
    # Thus, this test would pass
    def test_login_with_no_username(self):
        response = self.client.post(self.loginPage, {'username': '', 'password': 'Conmeo123!@'}, format='text/html')
        self.assertEqual(response.status_code, 200)

    # When the we log in, if we can't log in, the app would return a login page again
    # Thus, this test would pass
    def test_login_with_no_password(self):
        response = self.client.post(self.loginPage, {'username': 'username', 'password': ''}, format='text/html')
        self.assertEqual(response.status_code, 200)

################################################ End of LoginPageTest class ############################################


#Index Page Tests
class IndexPageTest(BaseCase):
    # This test is to test if the index page loads correctly from the home page
    def test_load_index_page(self):
        response = self.client.get(self.index)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tour_app/index.html')
        
        
    #This tests if the login page loads correctly from the home page
    def test_loginpage(self):
        # response = self.client.get(reverse('tour_app:loginPage'))
        response = self.client.post(self.loginPage)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tour_app/login.html')
     
     
     #this test if the register page loads correctly from the home page  
          
    def test_registerpage(self):
          response = self.client.get(self.registerPage)
          self.assertEquals(response.status_code, 200)
          self.assertTemplateUsed(response, 'tour_app/registration.html')
          
    
    #This tests if the map page loads correctly from the home page.  
    def test_map_page(self):
            # response = self.client.get(reverse('tour_app:registerPage'))
          response = self.client.get(self.mapPage)
          self.assertEquals(response.status_code, 200)
          self.assertTemplateUsed(response, 'tour_app/mapPage.html')
          
        
        
        
    
        
    