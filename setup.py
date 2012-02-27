from setuptools import setup, find_packages
import  os.path

version = '2.1.3'

readme = open('README.txt').read()
history = open(os.path.join('docs', 'changes.rst')).read()

setup(name="Products.membrane",
      version=version,
      description="Content-based users and groups for Plone",
      long_description=readme + '\n' + history,
      keywords='plone membrane member content remember',
      author='Rob Miller',
      author_email='robm@openplans.org',
      url='http://pypi.python.org/pypi/Products.membrane',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      install_requires=[
          "setuptools",
          "Products.GenericSetup >=1.4",
          "plone.indexer",
          "Plone >=3.3rc1",
      ],
      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 3.3',
        'Framework :: Plone :: 4.0',
        'Framework :: Plone :: 4.1',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
