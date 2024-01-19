from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: MacOS',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='vocodesaaslabs',
  version='0.0.1',
  description='SaaS Labs version of Vocode',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ajeya Krishna',
  author_email='ajeya@saaslabs.co',
  license='MIT', 
  classifiers=classifiers,
  keywords='voice', 
  packages=find_packages(),
  install_requires=[''] 
)