import codecs
import os
import re

from setuptools import setup, find_packages


def requirements():
    """
    Build the requirements list for this project
    Returns:
        A list of requirements
    """
    requirements_list = []
    with open('requirements.txt') as f:
        for line in f:
            requirements_list.append(line.strip())

    return requirements_list


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding="utf-8").read()


def grep(attrname):
    pattern = r'{}\W*=\W*"([^"]+)"'.format(attrname)
    strval, = re.findall(pattern, read(fpath("linkedrw/__init__.py")))
    return strval


setup(
    name='linkedrw',
    version=grep("__version__"),
    packages=find_packages(),
    license='MIT License',
    long_description=open('README.md').read(),
    install_requires=requirements(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['linkedrw=linkedrw:main'],
    },
)
