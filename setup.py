from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize


extensions = [
    Extension("WikiTransform.database", [
              "WikiTransform/database.py"], language="c++"),
    Extension("WikiTransform.utils.utils", [
              "WikiTransform/utils/utils.py"], language="c++"),
    Extension("WikiTransform.utils.wiki_page", [
              "WikiTransform/utils/wiki_page.py"], language="c++"),
    Extension("WikiTransform.utils.wiki_dump_reader", [
              "WikiTransform/utils/wiki_dump_reader.py"], language="c++"),

    # Add more extensions here if you have more Cython modules
]

setup(
    name='WikiTransform',
    ext_modules=cythonize(extensions),
    zip_safe=False,
)
