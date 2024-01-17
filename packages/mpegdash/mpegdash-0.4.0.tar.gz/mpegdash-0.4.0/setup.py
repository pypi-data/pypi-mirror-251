from os.path import exists
from setuptools import setup

long_description = None
if exists("README.md"):
    long_description = open("README.md").read()

setup(
  name="mpegdash",
  packages=["mpegdash"],
  description="MPEG-DASH MPD(Media Presentation Description) Parser",
  long_description=long_description,
  long_description_content_type='text/markdown',
  author="sangwonl",
  author_email="gamzabaw@gmail.com",
  version="0.4.0",
  license="MIT",
  zip_safe=False,
  include_package_data=True,
  url="https://github.com/sangwonl/python-mpegdash",
  test_suite="tests.my_module_suite",
  classifiers=[
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
  ],
)
