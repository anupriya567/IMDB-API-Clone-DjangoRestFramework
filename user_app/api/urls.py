
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

#  token authentication
urlpatterns = [
    
    path('login/', obtain_auth_token,name='login'),
    path('register/', views.registeration_view,name='register'),
    path('logout/', views.logout_view,name='logout'),
]

# jwt authentication
# urlpatterns = [
    
#     # for login => generate access token and refresh token 
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

#     # regenerate access token
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
#     # on registering jwt will generate access and refresh token
#     path('register/', views.registeration_view,name='register'),
    
# ]