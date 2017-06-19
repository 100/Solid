from distutils.core import setup
setup(
  name = 'solidpy',
  packages = ['Solid'],
  version = '0.11',
  description = 'A comprehensive gradient-free optimization library',
  author = 'Devin Soni',
  author_email = 'devinsoni1010@gmail.com',
  url = 'https://github.com/100/Solid',
  download_url = 'https://github.com/100/Solid/archive/0.1.tar.gz',
  keywords = ['metaheuristic', 'optimization', 'algorithm', 'artificial intelligence', 'machine learning'],
  classifiers = ['Programming Language :: Python :: 2.7'],
  install_requires=[
    'numpy'
  ],
)