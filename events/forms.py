from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,Event

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    interests = forms.CharField(widget=forms.Textarea, help_text="Enter your interests.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'interests']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user, interests=self.cleaned_data['interests'])
        return user
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'category']
#RSVP Form
from django import forms
from .models import RSVP

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['status']
