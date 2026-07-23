from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profiles/', views.all_profiles, name='all_profiles'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('like/<int:user_id>/',views.like_profile,name='like_profile'),
     path('my-likes/', views.my_likes, name='my_likes'),
]