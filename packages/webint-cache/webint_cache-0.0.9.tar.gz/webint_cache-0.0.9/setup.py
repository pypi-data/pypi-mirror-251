# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_cache', 'webint_cache.templates']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.11,<7.0.0',
 'phonenumbers>=8.13.27,<9.0.0',
 'python-whois>=0.8.0,<0.9.0',
 'svglib>=1.5.1,<2.0.0',
 'webint>=0.0']

entry_points = \
{'webapps': ['cache = webint_cache:app']}

setup_kwargs = {
    'name': 'webint-cache',
    'version': '0.0.9',
    'description': 'manage resource caching on your website',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/webint-cache',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
