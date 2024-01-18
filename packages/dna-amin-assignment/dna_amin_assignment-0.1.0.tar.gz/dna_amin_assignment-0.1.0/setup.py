# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dnastack',
 'dnastack.alpha',
 'dnastack.alpha.app',
 'dnastack.alpha.cli',
 'dnastack.alpha.cli.workbench',
 'dnastack.alpha.client',
 'dnastack.alpha.client.collections',
 'dnastack.alpha.client.wes',
 'dnastack.alpha.client.workbench',
 'dnastack.alpha.client.workflow',
 'dnastack.cli',
 'dnastack.cli.auth',
 'dnastack.cli.config',
 'dnastack.cli.data_connect',
 'dnastack.cli.helpers',
 'dnastack.cli.helpers.command',
 'dnastack.cli.helpers.printers',
 'dnastack.cli.workbench',
 'dnastack.client',
 'dnastack.client.collections',
 'dnastack.client.service_registry',
 'dnastack.client.workbench',
 'dnastack.client.workbench.ewes',
 'dnastack.client.workbench.workflow',
 'dnastack.common',
 'dnastack.configuration',
 'dnastack.context',
 'dnastack.http',
 'dnastack.http.authenticators',
 'dnastack.http.authenticators.oauth2_adapter']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>4.10.0',
 'click>8.0.3',
 'httpie>=3.2.1',
 'imagination>3.3.1',
 'jsonpath-ng>=1.5.3',
 'kotoba==3.1.0',
 'pydantic>=1.9.0,<2',
 'pyjwt>=2.1.0',
 'pyyaml>5.4.1',
 'requests-toolbelt>0.9.1,<1',
 'requests>2.23.0',
 'selenium>=3.141.0',
 'urllib3>1.25.11']

entry_points = \
{'console_scripts': ['amin-dnastack = dnastack.__main__:dnastack']}

setup_kwargs = {
    'name': 'dna-amin-assignment',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Amin Rezaei',
    'author_email': '63923736+am-rezaei@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
