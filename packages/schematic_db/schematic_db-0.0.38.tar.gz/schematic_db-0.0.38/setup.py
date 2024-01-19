# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schematic_db',
 'schematic_db.api_utils',
 'schematic_db.db_schema',
 'schematic_db.manifest_store',
 'schematic_db.query_store',
 'schematic_db.rdb',
 'schematic_db.rdb_builder',
 'schematic_db.rdb_queryer',
 'schematic_db.rdb_updater',
 'schematic_db.schema',
 'schematic_db.schema_graph',
 'schematic_db.synapse']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'SQLAlchemy-Utils>=0.41.1,<0.42.0',
 'SQLAlchemy>=2.0.19,<3.0.0',
 'deprecation>=2.1.0,<3.0.0',
 'interrogate>=1.5.0,<2.0.0',
 'networkx>=2.8.6,<3.0.0',
 'pandas>=2.0.0,<3.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'tenacity>=8.1.0,<9.0.0',
 'validators>=0.20.0,<0.21.0']

extras_require = \
{'mysql': ['mysqlclient>=2.1.1,<3.0.0'],
 'postgres': ['psycopg2-binary>=2.9.5,<3.0.0'],
 'synapse': ['synapseclient>=4.0.0,<5.0.0']}

setup_kwargs = {
    'name': 'schematic-db',
    'version': '0.0.38',
    'description': '',
    'long_description': 'None',
    'author': 'andrewelamb',
    'author_email': 'andrewelamb@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
