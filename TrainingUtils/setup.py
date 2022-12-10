from setuptools import setup, find_namespace_packages
import sys
import pathlib

PACKAGE_DATA = {}

REQUIREMENTS = [
    'numpy',
    'pylas',
    'pandas',
    'matplotlib',
    'sklearn'
]

def main():
    sys.path.append(str(pathlib.Path(__file__).parent) / 'src')
    from TrainingUtils import (__author__,
                               __author_email__,
                               __version__
                               )


    setup(
        name='Lidar-Mound-Detector',
        version=__version__,
        description='Lidar Mound Recognition Tool',
        author=__author__,
        author_email=__author_email__,
        package_dir={'': 'src'},
        packages=find_namespace_packages(where='src'),
        install_requires=REQUIREMENTS,
        python_requires="3.8.10",
        entrypoints= {
            'console_scripts': [
                'li-convert=TrainingUtils.converter:main'
            ]
        }
    )

if "__name__" == "__main__":
    main()
