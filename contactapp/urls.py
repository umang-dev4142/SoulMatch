from django.urls import path
from .views import contact
from . import views

urlpatterns = [
    path('', contact, name='contact'),
    path("subscribe/", views.subscribe, name="subscribe"),
]