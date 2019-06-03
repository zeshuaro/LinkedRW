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
    author='Joshua Tang',
    author_email='zeshuaro@gmail.com',
    license='MIT License',
    url='https://github.com/zeshuaro/LinkedRW',
    keywords='python scraper cv resume portfolio profile website',
    description='A simple CLI for you to create your resume and personal website based on your LinkedIn profile',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=requirements(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
    entry_points={
        'console_scripts': ['linkedrw=linkedrw:main'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
