from django.urls import path,include
from watchlist_app.api.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream',StreamPlatformVS,basename='streamplatform')


urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('list2/', WatchListGV.as_view(), name='movie-list2'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='watchlist-detail'),
    path('',include(router.urls)),
    # path('stream/', StreamPlatformAV.as_view(), name='stream-list'),  router dekh rha h
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'), #movie p review create
    
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),  # pk movie k saare review
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),    #particular review
]