from django.http import HttpResponse
from django.shortcuts import render
from .models import Contact

def contact(request):
    if request.method == "POST":
        print("POST REQUEST RECEIVED")

        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message")
        )

        return HttpResponse("Message Saved Successfully")

    return render(request, "contact.html")

# Create your views here.

# footer ke model ke liye

from django.shortcuts import redirect
from .models import Subscriber

def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if email:
            Subscriber.objects.get_or_create(email=email)

        return redirect("home")
