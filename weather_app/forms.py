from django import forms
from .models import User, Location

class UserForm(forms.ModelForm):
    email = forms.CharField(label='Email Address')
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        empty_label='Where do you live?'
    )

    class Meta:
        model = User
        fields = ('email', 'location',)