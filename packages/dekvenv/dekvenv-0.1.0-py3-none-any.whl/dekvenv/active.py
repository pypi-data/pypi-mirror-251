import os
import sys
from .constants import dir_name_venv


def activate_venv(path_venv=None):
    this_file = os.path.join(os.path.abspath(path_venv or dir_name_venv), 'Scripts', 'activate_this.py')
    with open(this_file) as f:
        exec(f.read(), {'__file__': this_file})


def is_venv_active(sp=None):
    return (sp or sys.prefix) != sys.base_prefix
