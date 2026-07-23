# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .models import Profile, Like

def register(request):
    if request.method == "POST":
        photo = request.FILES.get('photo')
        fullname = request.POST.get('fullname')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        city = request.POST.get('city')
        about = request.POST.get('about')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Email validation
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Email already registered'
            })

        # Password validation
        if len(password) < 8:
            return render(request, 'register.html', {
                'error': 'Password must be at least 8 characters'
            })

        # Age validation
        try:
            if int(age) < 18:
                return render(request, 'register.html', {
                    'error': 'You must be at least 18 years old to register'
                })
        except:
            return render(request, 'register.html', {
                'error': 'You must be at least 18 years old to register'
            })

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=user,
            photo=photo,
            fullname=fullname,
            age=age,
            gender=gender,
            occupation=occupation,
            city=city,
            about=about
        )

        return redirect('login')

    return render(request, 'register.html')

# # because so the profile in drash bord
# @login_required
# def user_dashboard(request):
#     print("ACCOUNTS DASHBOARD CALLED")

#     profile = Profile.objects.filter(user=request.user).first()

#     print("USER =", request.user)
#     print("PROFILE =", profile)

#     return render(request, "user_dashboard.html", {
#         "user": request.user,
#         "profile": profile,
        
#     })

# all ragister user ke profiles
@login_required
def all_profiles(request):

    my_profile = Profile.objects.get(user=request.user)

    if my_profile.gender == "Male":
        profiles = Profile.objects.filter(gender="Female")

    elif my_profile.gender == "Female":
        profiles = Profile.objects.filter(gender="Male")

    else:
        profiles = Profile.objects.exclude(user=request.user)

    profiles = profiles.exclude(user=request.user)

    return render(request, 'all_profiles.html', {
        'profiles': profiles
    })


# edit profile banane ke liye code i love code 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

@login_required
def edit_profile(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('user_dashboard')

    else:
        form = ProfileForm(instance=profile)

    return render(
    request,
    'edit_profile.html',
    {
        'form': form,
        'profile': profile
    }
)


# new view for all
@login_required
def like_profile(request, user_id):

    to_user = User.objects.get(id=user_id)

    if request.user == to_user:
        return redirect('all_profiles')

    my_profile = Profile.objects.get(user=request.user)
    target_profile = Profile.objects.get(user=to_user)

    if my_profile.gender == target_profile.gender:
        return redirect('all_profiles')

    Like.objects.get_or_create(
        from_user=request.user,
        to_user=to_user
    )

    return redirect('all_profiles')

# user ka like count dikhane ke liye
# my like views

# my likes dheakne ke liye
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Like

@login_required
def my_likes(request):
    likes = Like.objects.filter(to_user=request.user)

    return render(request, 'my_likes.html', {
        'likes': likes
    })