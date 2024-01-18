from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Kernel connecting functions'

# Setting up
setup(
    name="crunchkernelpackage",
    version=VERSION,
    author="Mukund Chourey",
    author_email="<mukund@crunchit.ai>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['altair', 'vegafusion[embed]', 'snowflake-sqlalchemy', 'google.cloud', 'db-dtypes'],
    keywords=['python', 'crunch', 'crunchit', 'kernel'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)