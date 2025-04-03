from setuptools import find_packages
from setuptools import setup

setup(
    name="soccer_project",
    version="0.1.0",
    description="The big match",
    author="Mihai Mocanu",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
)
