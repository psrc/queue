from django.db import models

class InputTypeDict(models.Model):
	name = models.CharField(max_length=128)

	def __unicode__(self):
		return self.name

class InputConfigurationValue(models.Model):
	container = models.ForeignKey(InputTypeDict, db_index=True)
	key = models.CharField(max_length=240, db_index=True)
	value = models.CharField(max_length=240, db_index=True)
