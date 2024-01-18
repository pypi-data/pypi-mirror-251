from setuptools import setup, find_packages
 
classifiers = [
  "Operating System :: OS Independent",
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='myipaddress',
  version='1.0',
  description="A package to get your/others IP information.",
  url='https://github.com/ericdennis7/myIPaddress',  
  author='Eric Dennis',
  author_email='ericdennis11@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['IP', 'myip', 'IP address', 'geolocation', 'public IP', 'private IP', 'socket', 'ports', 'open ports'], 
  packages=find_packages(),
  install_requires=[''] 
)