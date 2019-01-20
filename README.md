Overview
========

This is a temp project to serve as an example project for a comp.lang.python forum post

I have been previously used devpi as a solution to the problem outlined below. I had configured setup.cfg                                                  
[easy_install] and pip.conf to reference devpi server.

Based upon comp.lang.python posting response this repository has been created to try and understand how python 
setup.py develop can be used to automatically pull in dependencies.

The problem
===========
Assume the following projects, both of which have setup.py:
1. parent
2. child

parent is dependent upon child setuptools proj, located in sibling folder to this one.
It is intended that child could be used by many different projects in the future, not just the parent.
 
When the following code is run an error is received. The parent fails to find
the child setuptools project locally. It tries to pull it from pypi index.  

```
git clone

mkvirtualenv setuptools_dependencies
python setup.py develop
```

The developer has to manually install child dependency first:

```
git clone
mkvirtualenv setuptools_dependencies

cd child
python setup.py child
cd ..
cd parent
python setup.py parent
```

Question
========
Is it possible to get python setup.py to automatically pull in child dependency, bearing in
mind that the child dependency is likely to be used in future private projects.
For example, can setuptools be configured to pull in child from a separate git repository
when running ```python setup.py develop``` from parent folder?

Findings
========
A PEP508 url for a git repository can be used in *install_requires* of *setup.py*. An example is listed below.
```
requires = [
    'parent',
    'kinto-http@git+https://github.com/Kinto/kinto-http.py',
]
...
install_requires=requires
```
The package can then be installed with pip, using ```pip install -e . or pip install .```

However, installation with setuptools is then broken, i.e. ```python setup.py develop``` and ```python setup.py install``` fails. setuptools looks for packages in pypi indexes. To install using setuptools a devpi index would have to be installed and configured or packages would have to installed from a paid for pypi repository in the cloud. Alternatively, developers could manually install each private package dependency individually, prior to running ```python setup.py develop``` for the source package. Unless, there are alternative(s)?

If I want to have a Python private project, referencing other private project(s), available under source control and CI via gitlab.com, it seems that I can use the pip approach with PEP508 or use a requirements.txt file containing the git projects referenced as PEP508 urls, i.e. ```pip install -r requirements.txt```.

Confusion, stems from the fact that pip and setuptools dependencies are not synchronised, i.e. setuptools will break if PEP508 urls are listed for install_requires. Presumably the approach is to use either pip or setuptools but not both? 

**Update**
==========
From what I understand setuptools offers *dependency_links* as a list of dependency urls. In the example below, the *pyramid_core* package is an external dependency. 

I am currently using pip 18.1. pip has an option *--process-dependencies* that issues a deprecation warning. The following *setup.py* example works with both setuptools (python setup develop etc.) and pip (pip install -e . and pip install .).

The example *setup.py* below can be installed using both setuptools and pip as follows:
```
python setup.py develop
python setup.py install
pip install -e . --process-dependency-links
pip install .
```

**setup.py that is compatible with both setuptools and pip 18.1**
=================================================================
```
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()

dependencies = [
    'git+ssh://git@gitlab.com/dcs3spp/plantoeducate_core.git#egg=pyramid_core-0',
]

requires = [
    'parent',
    'pyramid_core',
]

setup_requires = [
]

tests_require = [
    'pytest',
    'pytest-cov',
]

setup(name='parent',
      version='0.1',
      description='parent',
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
      dependency_links=dependencies,
      setup_requires=setup_requires,
      tests_require=tests_require,
)
```

However, pip 18.1 support reading pep508 direct urls from install_requires. In future release there are plans to deprecate the --process-dependency-links pip install option:
- https://github.com/pypa/pip/issues/4187
- https://github.com/pypa/pip/pull/4175
If I use a PEP508 direct url in install_requires pip works but this fails when installing using setuptools 40.6.3, e.g. python setup.py develop or python setup.py install.

Will setuptools support direct pep508 urls in install_requires in the future also? 
