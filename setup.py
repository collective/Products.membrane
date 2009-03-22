from setuptools import setup, find_packages
from os.path import join

name = 'Products.membrane'
path = join(*name.split('.'))
version = open(join(path, 'version.txt')).read().strip()
readme = open(join(path, 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read().replace(name + ' - ', '')

setup(name = name,
      version = version,
      description = 'PluggableAuthService (PAS) plug-ins allowing for the '
                    'user-related behaviour and data to be obtained from '
                    'content within a Plone site.',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'plone membrane member content',
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
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      classifiers = [
        'Development Status :: 4 - Beta',
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
