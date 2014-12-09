from django.contrib import admin
from controller.models import InputConfigurationValue

class InputConfigurationAdmin(admin.ModelAdmin):
	list_display = ('container','key', 'value')

admin.site.register(InputConfigurationValue, InputConfigurationAdmin)
