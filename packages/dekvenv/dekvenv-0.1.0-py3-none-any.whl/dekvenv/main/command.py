import os
import sys
import typer
import virtualenv
from ..active import activate_venv
from ..constants import dir_name_venv
from ..utils.file import remove_path, write_file
from ..utils.common import shell_line, get_py_pkg_name, get_py_pkg_info
from ..utils.sys import sys_paths_relative
from .core import get_pkg_path
from ..pdm.core import is_pdm_project, pdm_clear_cache_hash_pkg, pdm_clear_cache_pkg, pdm_clear_cache_metadata, \
    pdm_update_cache_pkg

app = typer.Typer(add_completion=False)


@app.command()
def create(name: str = dir_name_venv, path='.', parent=''):
    path = os.path.normpath(os.path.abspath(path))
    path_venv = os.path.join(path, name)
    if not os.path.exists(path_venv):
        virtualenv.cli_run([path_venv])
    if parent:
        path_parent = os.path.normpath(os.path.abspath(parent))
        path_var = sys_paths_relative('', True)
        path_lib = path_var['platlib']
        pth = f"import site;site.addsitedir(r'{path_parent}{path_lib}')"
        write_file(os.path.join(path_venv+ path_lib, 'aaa__parent.pth'), pth)


@app.command()
def active(name: str = dir_name_venv):
    path_venv = os.path.join(os.getcwd(), name)
    activate_venv(path_venv)


@app.command()
def build(path: str = '.'):
    remove_path(os.path.join(path, '.pdm-build'))
    remove_path(os.path.join(path, 'build'))
    remove_path(os.path.join(path, 'dist'))
    if os.path.isdir(path):
        for fn in os.listdir(path):
            if fn.endswith('.egg-info'):
                remove_path(os.path.join(path, fn))

    if is_pdm_project(path):
        shell_line(f'pdm build -p {path}')
    else:
        shell_line(f'{sys.executable} -m build -s -w {path}')


@app.command()
def update(path_dir):
    path_dir = os.path.normpath(os.path.abspath(path_dir))
    pdm_update_cache_pkg(path_dir, get_py_pkg_info(path_dir))


@app.command()
def push(server: str = '', path: str = '.', se: bool = True):
    assert server
    build(path)
    path_pkg = get_pkg_path(path)
    pdm_clear_cache_hash_pkg(server, os.path.basename(path_pkg))
    pdm_clear_cache_pkg(get_py_pkg_name(path), path_pkg)
    pdm_clear_cache_metadata(path_pkg)
    shell_line(f'twine upload {"--skip-existing" if se else ""} --repository {server} {path_pkg}')


@app.command()
def var(name):
    data = sys_paths_relative('', True)
    if name:
        v = data[name]
    else:
        v = data
    sys.stdout.write(str(v))
    sys.stdout.flush()
