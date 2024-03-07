from distutils.core import setup

from setuptools import find_packages

setup(
    name="madotsuki",
    version="1.1",
    description="Библиотека для построения графических CRUD-интерфейсов",
    author="jqmxaec",
    packages=find_packages(),
    install_requires=["PyQt5", "SQLAlchemy"],
)
