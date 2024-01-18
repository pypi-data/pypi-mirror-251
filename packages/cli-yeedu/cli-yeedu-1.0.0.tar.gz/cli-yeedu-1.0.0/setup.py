from setuptools import setup, find_packages
import codecs
import re
import os.path
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='cli-yeedu',
    version=find_version("yeedu", "__init__.py"),
    packages=find_packages(),
    install_requires=[
        'argparse==1.4.0',
        'requests==2.28.1',
        'python-dotenv==1.0.0',
        'PyYAML==6.0',
        'setuptools==59.6.0'
    ],
    entry_points='''
    [console_scripts]
    yeedu=yeedu.yeedu:yeedu
    '''
)
