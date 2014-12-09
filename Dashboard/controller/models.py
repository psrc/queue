from django.db import models
from django.contrib.auth.models import User

class InputTypeDict(models.Model):
	name = models.CharField(max_length=128)

	def __unicode__(self):
		return self.name

class InputConfigurationValue(models.Model):
	container = models.ForeignKey(InputTypeDict, db_index=True)
	key = models.CharField(max_length=240, db_index=True)
	value = models.CharField(max_length=240, db_index=True)

class UserProfile(models.Model):
	# Link UsersProfile to a User model instance
	user = models.OneToOneField(User)

	# Additional attributes for each user
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_image', blank=True)

	# Override the __unicode__() method to return something meaningful
	def __unicode__(self):
		return self.user.username
