from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from watchlist_app import models
from watchlist_app.api import serializers
 

# class StreamPlateformTestCase(APITestCase):

#     # here we create a user and logged in as a normal user and manually created a plateform to test the list and individual element
#     def setUp(self):
#         self.user = User.objects.create_user(username="testcase",
#                                              password="testcase123")
    
#         self.token = Token.objects.get(user__username= self.user)   
#         client = APIClient()  
#         self.client.credentials(HTTP_AUTHORIZATION = 'Token' + self.token.key)
#         self.stream = models.StreamPlateform.objects.create(name= 'Netflix',about =  'very good',website = 'http://netflix.com')


#     # above setup will execute first, we get logged in but still we can't make a post request
#     # because only admin can do so
#     def test_streamplateform_create(self):

#         data = {
#             'name': 'Netflix',
#             'about': 'very good',
#             'website': 'http://netflix.com'
#         }

#         url = reverse('streamplateform-list')
#         reponse  = self.client.post(url, data)
#         self.assertEqual(reponse.status_code, status.HTTP_401_UNAUTHORIZED)
    
#     def test_streamplateform_list(self):
#         url = reverse('streamplateform-list')
#         reponse  = self.client.get(url)
#         self.assertEqual(reponse.status_code, status.HTTP_200_OK)
    
#     def test_streamplateform_item_get(self):
#         url = reverse('streamplateform-detail',args=(self.stream.id,))
#         reponse  = self.client.get(url)
#         self.assertEqual(reponse.status_code, status.HTTP_200_OK)

#     def test_streamplateform_item_put(self):
#         url = reverse('streamplateform-detail',args=(self.stream.id,))
#         data = {
#             'name': 'Netflix22',
#             'about': 'very good',
#             'website': 'http://netflix.com'
#         }

#         reponse  = self.client.put(url,data)
#         self.assertEqual(reponse.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_streamplateform_item_delete(self):
#         url = reverse('streamplateform-detail',args=(self.stream.id,))
#         reponse  = self.client.delete(url)
#         self.assertEqual(reponse.status_code,status.HTTP_401_UNAUTHORIZED)    

# class WatchListTestCase(APITestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username="testcase",
#                                              password="testcase123")
    
#         self.token = Token.objects.get(user__username= self.user)   
#         client = APIClient()  
#         self.client.credentials(HTTP_AUTHORIZATION = 'Token' + self.token.key)
#         self.stream = models.StreamPlateform.objects.create(name= 'Netflix',about =  'very good',website = 'http://netflix.com')
#         self.watchlist = models.WatchList.objects.create(title= 'Dangal',storyline =  'its my life',plateform = self.stream)

#     def test_watchlist_get(self):
#         url = reverse('watchList')
#         reponse  = self.client.get(url)
#         self.assertEqual(reponse.status_code,status.HTTP_200_OK) 

#     def test_watchlist_post(self):

#         data = {
#             'title': 'Dangal',
#             'storyline': 'its my life',
#             'plateform': 'self.stream'
#         }
#         url = reverse('watchList')
#         reponse  = self.client.post(url,data)
#         self.assertEqual(reponse.status_code,status.HTTP_401_UNAUTHORIZED)  


#     def test_watchlist_item_get(self):
#         url = reverse('watchListDetails',args=(self.watchlist.id,))
#         reponse  = self.client.get(url)
#         self.assertEqual(reponse.status_code,status.HTTP_200_OK)  

#     def test_watchlist_item_put(self):
#         data = {
#             'title': 'Dangal22',
#             'storyline': 'its my life',
#             'plateform': '1'
#         }
#         url = reverse('watchListDetails',args=(self.watchlist.id,))
#         reponse  = self.client.put(url,data)
#         self.assertEqual(reponse.status_code,status.HTTP_401_UNAUTHORIZED)  

#     def test_watchlist_item_delete(self):
#         url = reverse('watchListDetails',args=(self.watchlist.id,))
#         reponse  = self.client.delete(url)
#         self.assertEqual(reponse.status_code,status.HTTP_401_UNAUTHORIZED)  
    
# we have created 2 watchlists because a watchlist can only 1 review by a 1 user
# for watchlist we have created review by user 
# for watchlist2 we have created review manually    
class ReviewTestCase(APITestCase):

        def setUp(self):
            self.user = User.objects.create_user(username="example", password="Password@123")
            self.token = Token.objects.get(user__username=self.user)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

            self.stream = models.StreamPlateform.objects.create(name="Netflix", 
                                    about="#1 Platform", website="https://www.netflix.com")
            self.watchlist = models.WatchList.objects.create(plateform=self.stream, title="Example Movie",
                                    storyline="Example Movie", active=True)
            self.watchlist2 = models.WatchList.objects.create(plateform=self.stream, title="Example Movie",
                                    storyline="Example Movie", active=True)
            self.review = models.Review.objects.create(review_user=self.user, rating=5, description="Great Movie", 
                                watchlist=self.watchlist2, active=True)
    
        def test_review_create(self):
            data = {
                "review_user": self.user,
                "rating": 5,
                "description": "Great Movie!",
                "watchlist": self.watchlist,
                "active": True
            }

            response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(models.Review.objects.count(), 2)

            response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
            self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    
        def test_review_create_unauth(self):
            data = {
                'rating': '5', 
                'description': 'good',
                'watchlist': self.watchlist,
                'review_user': self.user,
                "active": True
            }

            self.client.force_authenticate(user = None)
            url = reverse('review-create',args=(self.watchlist.id,))
            reponse  = self.client.post(url,data)
            self.assertEqual(reponse.status_code,status.HTTP_401_UNAUTHORIZED)
            

        def test_reviewlist_get(self):
            url = reverse('reviewList',args=(self.watchlist.id,))
            reponse  = self.client.get(url)
            self.assertEqual(reponse.status_code,status.HTTP_200_OK)

        def test_review_item_get(self):
            url = reverse('ReviewDetails',args=(self.review.id,))
            reponse  = self.client.get(url)
            self.assertEqual(reponse.status_code,status.HTTP_200_OK)

        def test_review_item_update(self):
            data = {
                'rating': '4', 
                'description': 'good-updated',
                'watchlist': self.watchlist,
                'review_user': self.user,
                "active": True
            }
            url = reverse('ReviewDetails',args=(self.review.id,))
            reponse  = self.client.put(url,data)
            self.assertEqual(reponse.status_code,status.HTTP_200_OK)    

        # get all reviews from a particular user
        def test_review_user(self):
            reponse = self.client.get('/watch/reviews-user/?username'+ self.user.username)
            self.assertEqual(reponse.status_code,status.HTTP_200_OK)  


