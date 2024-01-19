# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['app_rappi_dfmejial',
 'app_rappi_dfmejial.conf',
 'app_rappi_dfmejial.data',
 'app_rappi_dfmejial.model',
 'app_rappi_dfmejial.tests',
 'app_rappi_dfmejial.tests.data',
 'app_rappi_dfmejial.tests.model']

package_data = \
{'': ['*'],
 'app_rappi_dfmejial': ['notebooks/*'],
 'app_rappi_dfmejial.data': ['raw_data/*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'scikit-learn>=1.2.1',
 'seaborn>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['rappi-dfmejial = app_rappi_dfmejial.main:main']}

setup_kwargs = {
    'name': 'app-rappi-dfmejial',
    'version': '0.0.5',
    'description': 'Rappi Titanic challenge',
    'long_description': None,
    'author': 'Daniel Mejia',
    'author_email': 'dfmejial@unal.edu.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
