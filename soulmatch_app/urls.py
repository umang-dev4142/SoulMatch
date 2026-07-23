"""
URL configuration for soulmatch_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include
from .views import LoginAPIView
from django.conf import settings
from django.conf.urls.static import static
from chat import views as chat_views

# user login ke liye
# from django.urls import path
# from .views import LoginAPIView, user_dashboard


urlpatterns = [
    path('admin/', admin.site.urls),

    # Website Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    # login system ke liye

    path("api/login/", LoginAPIView.as_view()),
    # drash bord sysyem ke liye
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),
    # profiles model ke liye
    path('accounts/', include('accounts.urls')),
    # logout ke liye
     path('logout/', views.user_logout, name='logout'),
    #  matching system ke liye
    path('matches/', views.match_users, name='matches'),
    # chat ke liye
    path("", include("chat.urls")),
    # contect subscribe ke liye
    path("", include("contactapp.urls")), 

    
]
# 👇 photo ke liye hai
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )



