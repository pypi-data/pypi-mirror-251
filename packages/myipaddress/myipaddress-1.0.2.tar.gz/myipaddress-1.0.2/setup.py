from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()
 
classifiers = [
  "Operating System :: OS Independent",
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='myipaddress',
  version='1.0.2',

  description="A package to get your/others IP information.",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url='https://github.com/ericdennis7/myIPaddress',

  author='Eric Dennis',
  author_email='ericdennis11@gmail.com',

  license='MIT', 
  classifiers=classifiers,
  keywords=['IP', 'myip', 'IP address', 'geolocation', 'public IP', 'private IP', 'socket', 'ports', 'open ports'], 
  packages=find_packages(),
  install_requires=[''] 
)
