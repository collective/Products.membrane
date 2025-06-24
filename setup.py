from setuptools import find_packages
from setuptools import setup


version = "7.0.0"
readme = open("README.rst").read()
history = open("CHANGES.rst").read()

setup(
    name="Products.membrane",
    version=version,
    description="Content-based users and groups for Plone",
    long_description=readme + "\n" + history,
    keywords="plone membrane member content remember",
    author="Rob Miller",
    author_email="robm@openplans.org",
    url="https://github.com/collective/Products.membrane",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["Products"],
    include_package_data=True,
    platforms="Any",
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=[
        "setuptools",
        "Products.CMFPlone",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.contenttypes[test]",
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
    ],
)
