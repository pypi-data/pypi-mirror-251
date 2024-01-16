"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="packaide_client",  # Required
    version="0.0.4",  # Required
    description="A client for accessing a packaideServer instance",  # Optional
    package_dir={"": "src"},
    packages=find_packages(where="src"),  # Required
    python_requires=">=3.7, <4",
    install_requires=[
        "pydantic",
        "requests"
    ],
)
