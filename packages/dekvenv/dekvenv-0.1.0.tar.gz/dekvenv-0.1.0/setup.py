import os
import sys
import codecs
from setuptools import find_packages, setup

root_dir = os.path.dirname(os.path.abspath(__file__))


def get_path(*args):
    return os.path.join(root_dir, *args)


def _process_requirements():
    requires = []
    path_req = get_path('requirements.txt')
    if os.path.exists(path_req):
        packages = codecs.open(path_req, 'r', encoding='utf-8').read().split('\n')
        for pkg in packages:
            pkg = pkg.strip()
            if not pkg:
                continue
            if pkg.startswith('git+ssh'):
                return_code = os.system(f'{sys.executable} -m pip install {pkg}')
                assert return_code == 0, f'error, status_code is: {return_code}, exit!'
            else:
                requires.append(pkg)
    return requires


def get_exclude():
    if os.path.exists(get_path('.pypiignore')):
        lst = codecs.open(get_path('.pypiignore'), 'r', encoding='utf-8').read().split('\n')
        return [x.strip() for x in lst if x.strip()]
    return []


setup(
    long_description=open(get_path("README.md"), "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=get_exclude()),
    install_requires=_process_requirements(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
