from distutils.core import setup

from setuptools import find_packages

setup(
    name="madotsuki",
    version="1.0",
    description="Библиотека для упрощения построения CRUD-интерфейсов",
    author="jqmxaec",
    packages=find_packages(),
    install_requires=["PyQt5", "SQLAlchemy"],
)
