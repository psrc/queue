from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput

from .models import UserProfile

import Pyro4

def is_valid_file(f):
	'''
	Test max size of 100k bytes
	'''
	MAX_SIZE = 100000

	if f.size > MAX_SIZE:
		raise forms.ValidationError('Too big: ' + f.name +
								    ' is larger than '+ str(MAX_SIZE) + ' bytes')
	return True

def is_node_free(node):
	n = Pyro4.Proxy('PYRONAME:' + node)

	try:
		busy = n.is_busy()

	except:
		raise forms.ValidationError('Node not responding.')

	if busy:
		raise forms.ValidationError('Node is busy.')

	return True


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture')


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
