from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='traggle',
  version='0.0.1',
  author='duckduck',
  author_email='dimondtp@gmail.com',
  description='Library that simplifies working with the "Traggle" site API',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Trejgus/',
  packages=find_packages(),
  install_requires=['requests>=2.31.0'],
  classifiers=[
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={
    'GitHub': 'https://github.com/Trejgus/'
  },
  python_requires='>=3.6'
)