from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cbpi4-PressureSensorMetric",
    version="0.0.1",
    description="CraftBeerPi Plugin",
    author="Joel Flepp",
    author_email="joel_flepp@hotmail.com",
    url="https://github.com/joel5399/cbpi4-PressureSensor",
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst", "*.yaml"],
        "cbpi4-PressureSensor": ["*", "*.txt", "*.rst", "*.yaml"],
    },
    packages=["cbpi4-PressureSensorMetric"],
    install_requires=["adafruit-circuitpython-ads1x15"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
