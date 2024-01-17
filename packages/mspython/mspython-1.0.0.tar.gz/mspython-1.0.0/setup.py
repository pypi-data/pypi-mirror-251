from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.0'
DESCRIPTION = 'An Scratch API Wrapper for scratch.mit.edu'
LONG_DESCRIPTION = DESCRIPTION

# Setting up
setup(
    name="mspython",
    version=VERSION,
    author="simasimanekosan",
    author_email="simaneko.meow4649@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    packages=find_packages(),
    install_requires=["websocket-client","numpy","requests","bs4"],
    keywords=['scratch api', 'scratch api python', 'scratch python', 'scratch for python', 'scratch', 'scratch cloud', 'scratch cloud variables', 'scratch bot'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
