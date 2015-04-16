from django import forms
from controller.models import UserProfile, SoundcastRuns
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture')

class SoundcastRunsForm(forms.Form):
    run_id = forms.CharField(label='Run ID', max_length=100)

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)