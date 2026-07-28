from pathlib import Path
from setuptools import find_packages
from setuptools import setup

version = "7.0.1.dev0"
readme = (Path(".") / "README.rst").read_text()
history = (Path(".") / "CHANGES.rst").read_text()

setup(
    name="Products.membrane",
    version=version,
    description="Content-based users and groups for Plone",
    long_description=readme + "\n" + history,
    long_description_content_type="text/x-rst",
    keywords="plone membrane member content remember",
    author="Rob Miller",
    author_email="robm@openplans.org",
    url="https://github.com/collective/Products.membrane",
    license="GPL",
    packages=find_packages("src"),
    namespace_packages=["Products"],
    package_dir={"": "src"},
    include_package_data=True,
    platforms="Any",
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=[
        "plone.indexer",
        "Products.CMFCore",
        "Products.CMFPlone",
        "Products.PlonePAS",
        "Products.PluggableAuthService",
        "Products.ZCatalog",
        "Zope",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.contenttypes[test]",
            "plone.autoform",
            "plone.dexterity",
            "plone.supermodel",
            "plone.testing",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Framework :: Zope :: 4",
        "Framework :: Zope :: 5",
        "Framework :: Zope",
        "Intended Audience :: Other Audience",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
)
