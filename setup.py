# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '5.0.1'
readme = open('README.rst').read()
history = open('CHANGES.rst').read()

setup(
    name="Products.membrane",
    version=version,
    description="Content-based users and groups for Plone",
    long_description=readme + '\n' + history,
    keywords='plone membrane member content remember',
    author='Rob Miller',
    author_email='robm@openplans.org',
    url='https://github.com/collective/Products.membrane',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    platforms='Any',
    zip_safe=False,
    install_requires=[
        "setuptools",
        "six",
        "plone.indexer",
        "Products.CMFPlone>=5.2rc1",
        "Products.PlonePAS>=5.0.1",
    ],
    extras_require={
        'test': ['plone.app.testing'],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: Addon',
        'Framework :: Plone :: 5.2',
        'Framework :: Zope :: 4',
        'Framework :: Zope',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
