from django.contrib import admin
from django.urls import path
from .views import *
# from django.conf.urls import url

urlpatterns = [
    path('', main),
    path('home', main),  # brings us back to the same func as above
    # path('all_players/', PlayerListView.as_view({'get': 'list'}), name='player-list'),
    path('adp', ReactView.as_view(), name='adp-list'),
    path('react/', react)
]
