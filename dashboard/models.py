from django.db import models
from django.contrib.auth.models import User,Group

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

    def __unicode__(self):
        return self.user.username


class SoundcastRuns(models.Model):
    runid = models.CharField(max_length=240, db_index=True)


class Tool(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    url = models.CharField(max_length=1024)
    def __unicode__(self): return self.name
    class Meta:
        ordering = ['name']

class Node(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    cpus = models.PositiveIntegerField(default=1)
    ram_gb = models.PositiveIntegerField(db_index=True)
    scratch_path = models.CharField(max_length=512, db_index=True)
    tools = models.ManyToManyField(Tool)

    def __unicode__(self): return self.name
    class Meta:
        ordering = ['name']

class Project(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    project_contact = models.CharField(max_length=256, db_index=True)
    modeling_contact = models.CharField(max_length=256, db_index=True)

    def __unicode__(self): return self.name
    class Meta:
        ordering = ['name']


class RunLog(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    project = models.ForeignKey(Project, null=True, blank=True)
    series = models.CharField(max_length=3, blank=True)
    note = models.CharField(max_length=2048, blank=True)
    status = models.IntegerField(db_index=True)
    start = models.DateTimeField('started', db_index=True)
    duration = models.DurationField(blank=True, null=True)
    tool = models.ForeignKey(Tool)
    tool_tag = models.CharField('tag', max_length=64, db_index=True, blank=True)
    inputs = models.CharField(max_length=2048, blank=True)

    def __unicode__(self):
        if (self.project):
            return '' + self.project.name + ' - ' + self.series
        else:
            return 'Run ' + str(self.id) + ' - ' + str(self.user)

    class Meta:
        ordering = ['-start']
