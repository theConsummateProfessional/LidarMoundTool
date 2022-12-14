from setuptools import setup, find_namespace_packages
import sys
import pathlib
import os

sys.path.append(str(pathlib.Path(__file__).parent / 'src'))
from TrainingUtils import (__author__, __author_email__, __version__,)

PACKAGE_DATA = {}

REQUIREMENTS = [
    'numpy',
    'pylas',
    'laszip',
    'pandas',
    'matplotlib',
    'sklearn',
    'scipy',
    'scikit-learn'
]

if os.name == 'nt':
    REQUIREMENTS.append('pywin32')

sys.path.append(str(pathlib.Path(__file__).parent / 'src'))


setup(
    name='Lidar-Mound-Detector',
    version=__version__,
    description='Lidar Mound Recognition Tool',
    author=__author__,
    author_email=__author_email__,
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    install_requires=REQUIREMENTS,
    python_requires='>= 3.8.*',
    entry_points= {
        'console_scripts': [
            'li-convert=TrainingUtils.converter:main',
            'li-clean=TrainingUtils.clean_data:main',
            'li-train=TrainingUtils.trainer:main'
        ]
    }
)
