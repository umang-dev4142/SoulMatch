from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'photo',
            'fullname',
            'age',
            'gender',
            'occupation',
            'city',
            'about'
        ]