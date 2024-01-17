from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize


extensions = [
    Extension("WikiTransform.database", [
              "WikiTransform/database.py"], language="c++"),
    Extension("WikiTransform.dump_db", [
              "WikiTransform/dump_db.py"], language="c++"),
    Extension("WikiTransform.utils.utils", [
              "WikiTransform/utils/utils.py"], language="c++"),
    Extension("WikiTransform.utils.wiki_page", [
              "WikiTransform/utils/wiki_page.py"], language="c++"),
    Extension("WikiTransform.utils.wiki_dump_reader", [
              "WikiTransform/utils/wiki_dump_reader.py"], language="c++"),
]

setup(
    name='WikiTransform',
    ext_modules=cythonize(extensions),
    version='0.1.0',
    packages=['WikiTransform'],
    license='MIT',
    description='A tool for extracting and transforming Wikipedia dumps.',
    long_description=open('README.md').read(),
)
