from django.urls import path
from .views import UserAPI


urlpatterns = [
    path('auth/', UserAPI.as_view())
]