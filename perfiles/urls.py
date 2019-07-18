from django.urls import path
from .views import ProfileListView, ProfileDetailView, FriendsListView

profiles_patterns = ([
    path('', ProfileListView.as_view(), name='list'),
    path('<email>/', ProfileDetailView.as_view(), name='detail'),
    path('friends', FriendsListView.as_view(), name='friends')
], "profiles")