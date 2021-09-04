from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from watchlist_app.api.serializers import WatchListSerializer,StreamPlateformSerializer,ReviewSerializer
from watchlist_app.models import WatchList,StreamPlateform,Review
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.pagination import  WatchListPagination,WatchListCPagination

# class based view using concrete View class
class UserReviewLists(generics.ListAPIView):
        # queryset = Review.objects.all()
        serializer_class = ReviewSerializer

        # def get_queryset(self):
        #     name = self.kwargs['username']
        #     return Review.objects.filter(review_user__username = name)  

        def get_queryset(self):
            queryset = Review.objects.all()
            username = self.request.query_params.get('username')
            if username is not None:
                queryset = queryset.filter(review_user__username=username)
            return queryset 


class WatchListquery(generics.ListAPIView):
        queryset = WatchList.objects.all()
        serializer_class = WatchListSerializer
        # pagination_class = WatchListPagination
        pagination_class = WatchListCPagination
        
        # permission_classes = [IsAuthenticated]
    
        # filter_backends = [DjangoFilterBackend]
        # filterset_fields = ['title','plateform__name']

        # filter_backends = [filters.SearchFilter]
        # search_fields =  ['^title','plateform__name']

class ReviewCreate(generics.CreateAPIView): # for post request
        
        serializer_class = ReviewSerializer
        permission_classes = [IsAuthenticated]
        throttle_classes = [ReviewCreateThrottle]

        def get_queryset(self):
            return Review.objects.all()

        def perform_create(self,serializer):
            pk = self.kwargs.get('pk')
            movie = WatchList.objects.get(pk=pk)
            review_user = self.request.user
            review_queryset = Review.objects.filter(watchlist = movie,review_user = review_user)

            if(review_queryset.exists()):
                raise ValidationError("You have already added a review")

            if(movie.number_rating == 0):
                movie.avg_rating = serializer.validated_data['rating']  
            else:
                movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
            movie.number_rating = movie.number_rating + 1    
            movie.save()
            serializer.save(watchlist = movie,review_user = review_user)


class ReviewList(generics.ListAPIView):
        # queryset = Review.objects.all()
        serializer_class = ReviewSerializer
        permission_classes = [IsAuthenticated]
        throttle_classes = [ReviewListThrottle]

        def get_queryset(self):
            pk = self.kwargs['pk']
            return Review.objects.filter(watchlist = pk)


class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
        queryset = Review.objects.all()
        serializer_class = ReviewSerializer
        permission_classes = [IsReviewUserOrReadOnly]
        throttle_classes = [UserRateThrottle,AnonRateThrottle]

     
# class based view using APIView Class

# perform operations(get, post) on all lists ie. movies,podcasts etc.
class WatchLists(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    

    def get(self, request):
        lists= WatchList.objects.all()
        serializer = WatchListSerializer(lists , many = True)
        return Response(serializer.data)
    
    def post(self,request):
         serializer = WatchListSerializer(data = request.data)
         if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
         else:
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    

# perform operations on a list item 
class WatchListDetails(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def put(self,request,pk):
         movie = WatchList.objects.get(pk = pk)
         serializer = WatchListSerializer(movie,data = request.data)
         if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
         else:
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk = pk)
        except WatchList.DoesNotExist:
            return Response({'error':'entered a wrong id. please check again' },status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def delete(self,request,pk):
        movie = WatchList.objects.get(pk = pk)
        movie.delete()
        content = {'please move along': 'nothing to see here'}
        return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# using viewset
class StreamPlateformVS(viewsets.ModelViewSet):
        permission_classes = [IsAdminOrReadOnly]
        queryset = StreamPlateform.objects.all()
        serializer_class = StreamPlateformSerializer


# class StreamPlatformVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


class StreamPlateformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        platform = StreamPlateform.objects.all()
        serializer = StreamPlateformSerializer(
            platform, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlateformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        try:
            platform = StreamPlateform.objects.get(pk=pk)
        except StreamPlateform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlateformSerializer(
            platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamPlateform.objects.get(pk=pk)
        serializer = StreamPlateformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = StreamPlateform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



