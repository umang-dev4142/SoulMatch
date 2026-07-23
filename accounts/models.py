# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    fullname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fullname
    

# profile ko like kerne ke liya model
from django.contrib.auth.models import User
from django.db import models

class Like(models.Model):

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes_given'
    )

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes_received'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} likes {self.to_user}"
