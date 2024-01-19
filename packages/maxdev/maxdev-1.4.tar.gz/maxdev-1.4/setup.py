from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='maxdev',
  version='1.4',
  description='MaxDev is a helpful library for developers.',
  long_description=open('README.rst').read(),
  url='',  
  author='maxeqx',
  author_email='maxeqxmail@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='maxdev maxeqx mdev dev developer',
  packages=find_packages(),
  install_requires=['requests'] 
)
