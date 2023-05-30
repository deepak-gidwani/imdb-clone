from rest_framework import status
from ..models import *
from django.http import HttpResponse, JsonResponse
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics   
from rest_framework import viewsets  
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from watchlist_app.api.permissions import *
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from .throttling import *
from rest_framework.throttling import ScopedRateThrottle


# Create your views here.

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        
        user = self.request.user
        pk=self.kwargs['pk']
        watchlist = WatchList.objects.get(pk=pk)
        review_queryset = Review.objects.filter(watchlist=watchlist,review_user=user)
        
        if review_queryset.exists():
            raise ValidationError('you have already reviewed this movie')
        
        if watchlist.avg_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating += serializer.validated_data['rating']
            watchlist.avg_rating /= 2
            
        watchlist.number_rating += 1
        watchlist.save()
        
        serializer.save(watchlist=watchlist,review_user=user) # this tell which movie we are adding review

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    authentication_classes = [TokenAuthentication]
    throttle_classes=[ReviewListThrottle]
    permission_classes = [IsAuthenticated]
    serializer_class  = ReviewSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        # print(Review.objects.filter(watchlist_id=pk))
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    permission_classes = [ReviewUserorAdminorReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    

# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request,*args, **kwargs):
#         return self.list(request,*args,**kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request,*args, **kwargs):
#         return self.retrieve(request,*args,**kwargs)
    
# class StreamPlatformVS(viewsets.ViewSet):  viewsets
    
#     def list(self,request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset,many=True)
#         return Response(serializer.data)
    
#     def retrieve(self,request,pk=None):
#         queryset = StreamPlatform.objects.all()
#         all_shows = get_object_or_404(queryset,pk=pk)
#         serializer = StreamPlatformSerializer(all_shows)
#         return Response(serializer.data)
    
#     def create(self,request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     def delete(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [AdminOrReadOnly]

# class StreamPlatformAV(APIView):

#     def get(self, request):
#         platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platform, many=True,context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
# class StreamPlatformDetailAV(APIView):
#     def get(self, request,pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)


class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):

    permission_classes = [AdminOrReadOnly]
    # authentication = [IsAdminUser]
    def get(self, request, pk):
        # print(self.kwargs['pk'])
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):

        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class MovieListAV(APIView):
#     def get(self, request):
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

# class MovieDetailAV(APIView):
#     def get(self, request,pk):
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     def put(self,request,pk):
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.error_messages)
    
#     def delete(self,request,pk):
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         # deserialize krte time data keyword lgana pdta hai
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save
#             return Response(serializer.data)
#         return Response(serializer.error_messages)


# def movie_details(request, pk): working fine with api decorator
#   movie = Movie.objects.get(pk=pk)
#   serializer = MovieSerializer(movie)
#   return JsonResponse(serializer.data)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.error_messages)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
