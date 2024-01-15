from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='ccontrol',
  version='0.0.1',
  author='INTERJL',
  author_email='makar.arapov.real@gmail.com',
  description='library that simplifies working with the console',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/INTERJL',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='console speed python ',
  project_urls={
    'GitHub': 'https://github.com/INTERJL/ccontrol/tree/main?tab=MIT-1-ov-file'
  },
  python_requires='>=3.6'
)