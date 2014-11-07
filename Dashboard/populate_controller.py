import os
import inspect
from input_configuration import *

def populate(key, value):
	new_dict = add_dict(key)
	add_keyval(new_dict, key, value)

def add_dict(key):
	n = InputTypeDict.objects.get_or_create(name=key)[0]
	return n

def add_keyval(container, key, value):
	kv =  InputConfigurationValue.objects.get_or_create(container=container, key=key, value=value)[0]
	return kv

# def add_key_val(key, value):
# 	kv = KeyVal()

if __name__ == '__main__':
	print "starting Controller population script..."
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
	from controller.models import InputTypeDict, InputConfigurationValue
	from input_configuration import InputConfig

# Tuple of input config variables and values
input_config_tuples = inspect.getmembers(InputConfig)

for tuple in input_config_tuples:
   populate(str(tuple[0]), str(tuple[1]))
