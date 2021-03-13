from django.test import TestCase, Client
from django.urls import resolve
from .views import index

from .models import User, Post, Comment, Like, Follow

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):

        user = User.objects.create(username="test", email="test@test.com", first_name="John", last_name="Doe")
    
    def testfoundHomePage(self):
        found = resolve("/")
        self.assertEqual(found.func, index)
        


    def testIndex(self):
        c = Client()
        response = c.get("http://127.0.0.1:8000/login")
        self.assertEqual(response.status_code, 200)    

