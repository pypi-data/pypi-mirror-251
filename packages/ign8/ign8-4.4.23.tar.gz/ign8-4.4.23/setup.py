# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ign8',
 'ign8.airflow',
 'ign8.awx',
 'ign8.bump',
 'ign8.dns',
 'ign8.fiile',
 'ign8.gitea',
 'ign8.iad',
 'ign8.inabox',
 'ign8.inthevault',
 'ign8.jenkins',
 'ign8.libsync',
 'ign8.netbox',
 'ign8.pitv',
 'ign8.podman',
 'ign8.pypi',
 'ign8.selinux',
 'ign8.selinux.files',
 'ign8.semaphore',
 'ign8.terraform',
 'ign8.traefik',
 'ign8.ui',
 'ign8.ui.project',
 'ign8.ui.project.ignite',
 'ign8.ui.project.ignite.ansible',
 'ign8.ui.project.ignite.ansible.migrations',
 'ign8.ui.project.ignite.cmdb',
 'ign8.ui.project.ignite.cmdb.migrations',
 'ign8.ui.project.ignite.ignite',
 'ign8.ui.project.ignite.main',
 'ign8.ui.project.ignite.main.migrations',
 'ign8.ui.project.ignite.selinux',
 'ign8.ui.project.ignite.selinux.migrations',
 'ign8.vault',
 'ign8.vmware',
 'ign8.vmware.tools',
 'ign8.wireguard',
 'ign8.zabbix']

package_data = \
{'': ['*'],
 'ign8.selinux': ['meta/*', 'roles/*', 'tasks/*'],
 'ign8.ui.project.ignite': ['templates/*'],
 'ign8.ui.project.ignite.main': ['templates/*'],
 'ign8.ui.project.ignite.selinux': ['templates/*']}

install_requires = \
['Django>=4.2.8,<5.0.0',
 'PyYAML>=6.0.1,<7.0.0',
 'ansible-core>=2.15.8,<3.0.0',
 'ansible>=8.7.0,<9.0.0',
 'cryptography>=41.0.2,<42.0.0',
 'djangorestframework>=3.14.0,<4.0.0',
 'gunicorn>=21.2.0,<22.0.0',
 'hvac>=1.1.0,<2.0.0',
 'mypy>=0.910,<0.911',
 'netbox>=0.0.2,<0.0.3',
 'paramiko>=3.3.1,<4.0.0',
 'pynetbox>=6.6.2,<7.0.0',
 'pytest>=6.2,<7.0',
 'python-jenkins>=1.7.0,<2.0.0',
 'redis>=4.5.3,<5.0.0',
 'requests>=2.25,<3.0',
 'toml>=0.10.2,<0.11.0',
 'xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['ign8 = ign8:main',
                     'ign8_airflow = ign8.airflow:main',
                     'ign8_bump = ign8.bump:main',
                     'ign8_dns = ign8.dns:main',
                     'ign8_file = ign8.file:main',
                     'ign8_gitea = ign8.gitea:main',
                     'ign8_iad = ign8.iad:main',
                     'ign8_inabox = ign8.inabox:main',
                     'ign8_jenkins = ign8.jenkins:main',
                     'ign8_netbox = ign8.netbox:main',
                     'ign8_pitv = ign8.pitv:main',
                     'ign8_selinux = ign8.selinux:main',
                     'ign8_semaphore = ign8.semaphore:main',
                     'ign8_terraform = ign8.terraform:main',
                     'ign8_traefik = ign8.traefik:main',
                     'ign8_ui = ign8.ui:main',
                     'ign8_vault = ign8.vault:main',
                     'ign8_zabbix = ign8.zabbix:main']}

setup_kwargs = {
    'name': 'ign8',
    'version': '4.4.23',
    'description': 'Knowit Automation lifecycle management',
    'long_description': None,
    'author': 'Jakob Holst',
    'author_email': 'jakob.holst@knowit.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ign8.openknowit.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
