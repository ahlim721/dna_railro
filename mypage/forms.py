from django import forms
from django.contrib.auth.models import User

class LeaveForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']
