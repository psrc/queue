# This finds all folders in the plugin directory and adds them to _all_ so they get imported.
import os

__all__ = [name for name in os.listdir(".") if os.path.isdir(name)]
