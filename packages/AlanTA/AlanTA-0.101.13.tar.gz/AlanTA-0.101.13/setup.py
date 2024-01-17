# setup.py
from setuptools import setup, find_packages

setup(
   name="AlanTA",
   version='0.101.13',
   author="fdoooch & Alan",
   author_email="fdoooch@gmail.com",
   url="https://github.com/fdoooch/AlanTA",
   description="Private Python library for technical analysis",
   packages=find_packages(),
   include_package_data=True,
   license='MIT',
   python_requires='>=3.10',
   install_requires=[
          'numba',
          'pandas',
          'numpy'
      ],
   zip_safe=False
)