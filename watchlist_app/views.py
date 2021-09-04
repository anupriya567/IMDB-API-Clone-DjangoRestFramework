# from django.shortcuts import render,redirect
# from django.http import JsonResponse,HttpResponse
# from .models import Movie


# # Create your views here.

# def movieList(request):
#     movies = Movie.objects.all()
#     # print(movies)
#     # print(movies.value())
#     data = {
#         'movies' : list(movies.values())
#     }
#     return JsonResponse(data)

# def movieDetails(request,pk):
#     movie = Movie.objects.get(pk = pk)
#     data = {
#         'name' : movie.name,
#         'description' : movie.description,
#         'active' : movie.active
#     }

#     return JsonResponse(data)