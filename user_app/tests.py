from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class RegisterationTestCase(APITestCase):
     
     def test_register(self):
        data = {
             "username": "testcase",
             "email": "testcase@example.com",
             "password": "testcase123",
             "password2": "testcase123",
         },

        url = reverse('register')
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
   
class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testcase",
                                             password="testcase123")

    def test_login(self):

        data = {
            "username": "testcase",
            "password": "testcase123",
        }

        url = reverse('login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        
        self.token = Token.objects.get(user__username= 'testcase')   
        client = APIClient()  
        self.client.credentials(HTTP_AUTHORIZATION = 'Token' + self.token.key)
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        









