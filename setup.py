from setuptools import setup

version = '0.0.01'


namespace_packages = ['lib']

packages = ['lib.parser']


scripts = ['bin/match-features-to-peptides',
           'bin/count-ms2',
           'bin/filter-fdr']


install_requires = ['lxml',
                    'bs4']


setup(name='pepmatcher',
      version=version,
      namespace_packages=namespace_packages,
      packages=packages,
      scripts=scripts,
      license='open',
      author='Aaron Scott',
      author_email='aa5278sc-s@student.lu.se',
      install_requires=install_requires)
