from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.1.3'
DESCRIPTION = 'Data Science'
LONG_DESCRIPTION = 'some helpfull methods to use'

# Setting up
setup(
    name="farsakh-df",
    version=VERSION,
    author="Hamza Mohammed Farsakh",
    author_email="<farsakh.m.hamza@gmail.com>",
    description=DESCRIPTION,
    # long_description_content_type="text/markdown",
    # long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'sklearn'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)