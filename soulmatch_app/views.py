from django.shortcuts import render
from contactapp.models import Contact
from accounts.models import Profile, Like

# def home(request):

#     featured_profiles = Profile.objects.all()[:6]   # top 6 profiles

#     return render(request, 'index.html', {
#         'featured_profiles': featured_profiles
#     })

def home(request):
    return render(request,'index.html')
def contact(request):
    success = False
    if request.method == "POST":
        print("POST RECEIVED")
        print(request.POST)

        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message")
        )
        success = True

        print("DATA SAVED")

    return render(request, "contact.html",{"success":success})
    
def about(request):
    return render(request,'about.html')
def login_page(request):
    return render(request, 'login.html')
def register(request):
    return render(request,'register.html')
# def user_dashboard(request):
#     return render(request, 'user_dashboard.html')



# this code is user and admin login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response


class LoginAPIView(APIView):

    def post(self, request):

        login_input = request.data.get("login")
        password = request.data.get("password")

        try:
            user_obj = User.objects.get(
                Q(username=login_input) | Q(email=login_input)
            )
        except User.DoesNotExist:
            return Response({"success": False, "message": "User not found"})

        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if not user:
            return Response({"success": False, "message": "Invalid password"})

        # 🔥 SESSION CREATE (VERY IMPORTANT)
        auth_login(request, user)

        # 👑 ADMIN
        if user.is_superuser:
            return Response({
                "success": True,
                "redirect": "/admin/"
            })

        # 👤 NORMAL USER
        return Response({
            "success": True,
            "redirect": "/user-dashboard/"
        })
# drashbord ke liye hai
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from accounts.models import Profile, Like

@login_required
def user_dashboard(request):
    profile = Profile.objects.filter(user=request.user).first()

    likes_count = Like.objects.filter(
        to_user=request.user
    ).count()

    print("USER =", request.user)
    print("PROFILE =", profile)
    print("LIKES COUNT =", likes_count)

    return render(request, "user_dashboard.html", {
        "user": request.user,
        "profile": profile,
        "likes_count": likes_count
    })

# logout ke liye logout function

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')


# matching system ke liye
from django.contrib.auth.decorators import login_required
@login_required
def match_users(request):

    user_profile = Profile.objects.filter(user=request.user).first()
    matches = Profile.objects.exclude(user=request.user)

    min_age = user_profile.age - 3
    max_age = user_profile.age + 3

    matches = Profile.objects.exclude(user=request.user)

    matches = matches.filter(age__gte=min_age, age__lte=max_age)

    if user_profile.gender.lower() == "male":
        matches = matches.filter(gender__iexact="female")
    elif user_profile.gender.lower() == "female":
        matches = matches.filter(gender__iexact="male")

    if user_profile.city:
        matches = matches.filter(city__iexact=user_profile.city)

    return render(request, "match.html", {"matches": matches})