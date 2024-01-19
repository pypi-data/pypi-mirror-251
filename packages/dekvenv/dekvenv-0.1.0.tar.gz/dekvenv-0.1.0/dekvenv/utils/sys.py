import os
import sys
import subprocess
from sysconfig import get_paths


def path_sys_exe():  # Used by system python Scripts bin
    return subprocess.getoutput('python -c "import sys;print(sys.executable)"')


def sys_paths_relative(path, raw=False):  # sys_paths_relative('./.venv')
    if not raw:
        path = os.path.normpath(os.path.abspath(path))
    result = {}
    paths = get_paths()
    for k, p in paths.items():
        if p.startswith(sys.prefix):
            result[k] = path + p[len(sys.prefix):]
        else:
            result[k] = p
    return result
