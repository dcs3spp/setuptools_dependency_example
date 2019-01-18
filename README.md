Overview
========

This is a temp project to serve as an example project for a comp.lan.python forum post

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


