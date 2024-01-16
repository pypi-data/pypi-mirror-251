# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['env_to_class']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'env-to-class',
    'version': '1.1.0',
    'description': 'Enviroment variables to class object with checking for the presence of parameters',
    'long_description': "\n## Description\n\nSimple use env settings with class type\n\n# install\n```\n  pip install env-to-class\n```\n\n#### import\n\n```python\nfrom env_to_class import Settings\n```\n\n#### Description\n```text\nThe library allows you to encrypt your settings stored in json format.\nIt is possible to convert from a simple storage option to an encrypted one. \nTo work with the encrypted version of the settings, you need to pass the startup parameter - the password with which the encryption took place.\nTry it, the library is very simple.\n```\n\n\n#### Usage\n# Import lib\n```python\n  required_settings = 'Database.name, Database.user, Database.pwd, Database.host, Clickhouse.host, Clickhouse.user, Clickhouse.pwd'\n  settings = Settings(required_settings)\n\n  nameDB = settings.Database.name\n  userDB = settings.Database.user\n  pwdDb = settings.Database.pwd\n  hostDB = settings.Database.host\n  clickhouseHost = settings.Clickhouse.host\n  clickhousePwd = settings.Clickhouse.pwd\n  clickhouseUser = settings.Clickhouse.user\n```\n",
    'author': 'to101',
    'author_email': 'to101kv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.1,<4.0',
}


setup(**setup_kwargs)
