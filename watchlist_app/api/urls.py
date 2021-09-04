from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import StreamPlateformVS

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('plateforms',views.StreamPlateformVS,basename="streamplateform")

 
urlpatterns = [
    path('lists/',views.WatchLists.as_view(), name = 'watchList'),
    path('list/<int:pk>/',views.WatchListDetails.as_view(), name = "watchListDetails"),
   
    path('',include(router.urls)),
    
    
    # path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='stream-detail'),
   
    path('<int:pk>/review-create/',views.ReviewCreate.as_view(), name = "review-create"),
    path('<int:pk>/reviews/',views.ReviewList.as_view(), name = "reviewList"),
    path('review/<int:pk>/',views.ReviewDetails.as_view(), name = "ReviewDetails"),
    path('reviews-user/',views.UserReviewLists.as_view(), name = "UserReviewLists"),
     path('listquery/', views.WatchListquery.as_view(), name='WatchListquery'),
] 

