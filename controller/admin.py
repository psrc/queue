from django.contrib import admin

from .models import InputConfigurationValue
from .models import Project, Tool, RunLog, Node

class InputConfigurationAdmin(admin.ModelAdmin):
	list_display = ('container','key', 'value')

admin.site.register(InputConfigurationValue, InputConfigurationAdmin)

admin.site.register(Project)
admin.site.register(Tool)
admin.site.register(RunLog)
admin.site.register(Node)

