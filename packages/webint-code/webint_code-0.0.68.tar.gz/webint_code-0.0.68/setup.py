# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_code', 'webint_code.templates']

package_data = \
{'': ['*'],
 'webint_code.templates': ['project/*',
                           'project/issues/*',
                           'pypi/*',
                           'search/*',
                           'snippets/*']}

install_requires = \
['gmpg>=0.0', 'webagt>=0.0', 'webint>=0.0']

entry_points = \
{'webapps': ['code = webint_code:app']}

setup_kwargs = {
    'name': 'webint-code',
    'version': '0.0.68',
    'description': 'manage code on your website',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/webint-code',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
