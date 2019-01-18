import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()


requires = [
    'child',
]

setup_requires = [

]

tests_require = [
    'pytest',
    'pytest-cov',
]

setup(name='child',
      version='0.1',
      description='child',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
      ],
      author='dcs3spp',
      author_email='myemail@outlook.com',
      url='',
      keywords='setuptools',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      setup_requires=setup_requires,
      tests_require=tests_require,
)
