from setuptools import setup, find_packages
from os.path import join

version = "2.0"

name = 'Products.membrane'
path = join(*name.split('.'))
readme = open('README.txt').read()
history = open(join('docs', 'HISTORY.txt')).read().replace(name + ' - ', '')

setup(name = name,
      version = version,
      description = "Content-based users and groups for Plone",
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'plone membrane member content remember',
      author = 'Rob Miller',
      author_email = 'robm@openplans.org',
      url = 'http://plone.org/products/membrane',
      download_url = 'http://pypi.python.org/pypi/Products.membrane/',
      license = 'GPL',
      packages = find_packages(exclude=['ez_setup']),
      namespace_packages = ['Products'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      install_requires = [
          "setuptools",
          "Products.GenericSetup >=1.4",
      ],
      classifiers = [
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
)
