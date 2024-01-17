from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='csv_progressbar',
  version='0.1',
  author='chazovtema',
  author_email = 'chazovtema@mail.ru',
  description='A progressbar wrapper for standart csv package',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords= ['csv', 'progressbar'],
  project_urls={'github': 'https://github.com/chazovtema/CSVProgressBar'},
  python_requires='>=3.10',
)