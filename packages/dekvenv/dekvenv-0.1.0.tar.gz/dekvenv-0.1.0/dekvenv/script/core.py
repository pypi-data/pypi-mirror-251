import os
import sys
import json
import subprocess
from ..utils.sys import sys_paths_relative, path_sys_exe


def get_pkg_entry_points(pkg, sys_exe=None):
    ev = f"""print(__import__('json').dumps([x.name for x in __import__('importlib').import_module('importlib.metadata').entry_points(name='{pkg}')]))"""
    if not sys_exe:
        sys_exe = sys.executable
    return json.loads(subprocess.getoutput(f'{sys_exe} -c "{ev}"'))


def get_pkg_entry_points_paths(pkg, path_venv):
    path_venv_scripts = sys_paths_relative(path_venv)['scripts']
    path_venv_sys_exe = os.path.join(path_venv_scripts, os.path.basename(path_sys_exe()))
    entry_points = get_pkg_entry_points(pkg, path_venv_sys_exe)
    ext = os.path.splitext(path_venv_sys_exe)[1]
    return {
        entry_point: os.path.join(path_venv_scripts, f'{entry_point}{ext}') for entry_point in entry_points
    }
