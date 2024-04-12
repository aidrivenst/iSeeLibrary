import pathlib
from os.path import abspath, dirname, join
from setuptools import setup

CURDIR = dirname(abspath(__file__))

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.rst").read_text()

with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()


setup(
    name="robotframework-Datum",
    version="0.1.0",
    author="AI Driven ST Foundation;
    author_email="contact.aidrivenstfoundation@gmail.com",
    description="robot framework library that contains a set of functions for visual testing",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aidrivenst/iSeeLibrary",
    classifiers=[
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    packages=["iSeeLibrary"],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    python_requires=">=3.0",
)
