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
    'version': '4.4.27',
    'description': '    Ignite it all.\n    ',
    'long_description': '# Keep ign8 and automate\n\n\n\n\n### Install and update ign8\n\npip install --upgrade ign8\n\n\n### Basic configuration\n\nign8 init\n\ncreates a basic ign8 configuration\n\n/etc/ign8/ign8.json and /etc/ign8/secrets.json\n\n```json\n{\n  "organization": [\n    {\n      "name": "ign8",\n      "meta":\n        {\n          "description": "Keep ign8 and automate",\n          "max_hosts": 100,\n          "default_environment": "Ansible Engine 2.9 execution environment",\n          "secrets": "files"\n        },\n      "projects": [\n        {\n          "name": "main",\n          "description": "Keep ign8 and automate",\n          "scm_type": "git",\n          "scm_url": "git@github.com:JakobHolstDK/openknowit_ansibleautomation_main.git",\n          "scm_branch": "main",\n          "credential": "github",\n          "master": "True"\n        }\n      ],\n      "inventories": [\n        {\n          "name": "000_masterinventory",\n          "description": "Inventorycontaining all servers under automation control",\n\t  "variables": {\n\t\t  "serviceaccount": {\n\t            "name": "knowit",\n\t\t    "gecos": "Ansible automation manager"\n\t\t  }\n\t  },\n          "type": "static"\n        },\n        {\n          "name": "001_netboxinventory",\n          "description": "Inventory containing all servers in netbox",\n\t  "variables": {\n\t\t  "serviceaccount": {\n\t            "name": "knowit",\n\t\t    "gecos": "Ansible automation manager"\n\t\t  }\n\t  },\n          "type": "netbox"\n\t}\n      ],\n      "hosts": [\n        {\n          "name": "prodign8001.openknowit.com", "description": "Server cabable for running selfmaintainance", "inventories": ["000_masterinventory"]\n        }\n      ],\n      "templates": [\n        {\n          "name": "000_ansibleautomationmanager_checkup",\n          "description": "Master job for self healing ansible automation as code",\n          "job_type": "run",\n          "inventory": "000_masterinventory",\n          "project": "main",\n          "EE": "Automation Hub Default execution environment",\n          "credentials": "ign8server",\n          "playbook": "checkup.yml"\n        },\n        {\n          "name": "000_ansibleautomationmanager_update",\n          "description": "Maintain ansible manager and prereqs",\n          "job_type": "run",\n          "inventory": "000_masterinventory",\n          "project": "main",\n          "EE": "Automation Hub Default execution environment",\n          "credentials": "ign8server",\n          "playbook": "ansiblemanager.yml"\n        }\n      ],\n      "schedules": [\n        {\n          "name": "000_jobschedule_ansibleautomationmanager_checkup",\n          "type": "job",\n          "template": "000_ansibleautomationmanager_checkup",\n          "description": "Master job for ensuring connectivity",\n          "local_time_zone": "CET",\n          "run_every_minute": "5",\n          "start": "now",\n          "end": "never"\n        },\n        {\n          "name": "000_jobschedule_ansibleautomationmanager_update",\n          "type": "job",\n          "template": "000_ansibleautomationmanager_update",\n          "description": "Master job updating automation manager",\n          "local_time_zone": "CET",\n          "run_every_minute": "5",\n          "start": "now",\n          "end": "never"\n        },\n        {\n          "name": "000_projectschedule_ansibleautomationmanager",\n          "type": "project",\n          "project": "main",\n          "description": "Master job for syncing project main",\n          "local_time_zone": "CET",\n          "run_every_minute": "10",\n          "start": "now",\n          "end": "never"\n        }\n      ],\n      "users":\n        {\n          "user_vault_path": "project/openknowit/users",\n          "description": "AD integration is mandatory"\n        },\n      "labels":\n      [\n        {\n          "name": "static"\n        },\n        {\n          "name": "production"\n        },\n        {\n           "name": "test"\n        }\n      ]\n    }\n  ]\n}\n\n```\nand the secret.jsob\n```json\n{\n  "ign8": {\n    "vault": \n    [\n     {\n      "name": "myvault",\n      "description": "Credentials to access a hashicorp vault",\n      "vault_id": "https://vault.example.com",\n      "vault_token": "/etc/ign8/vault.token"\n    }\n    ],\n    #  Here we have a simple server credential built using a file located on the ign8 server\n    "ssh": [\n     {\n      "name": "ign8server",\n      "username": "ign8",\n      "password": "/etc/ign8/ign8server.password",\n      "description": "Credentials to login to ign8 server and setup ign8 service",\n      "ssh_private_key": "/opt/ign8/ign8server_rsa",\n      "privilege_escalation_method": "sudo",\n      "privilege_escalation_username": "root",\n      "privilege_escalation_password": "/etc/ign8/ign8server.password"\n    },\n    {\n      "name": "productionserver",\n      "username": "root",\n      "password": "/etc/ign8/productionserver.password",\n      "description": "Credentials to login to productionservers",\n      "ssh_private_key": "/opt/ign8/prodservers_rsa",\n      "privilege_escalation_method": "sudo",\n      "privilege_escalation_username": "root",\n      "privilege_escalation_password": "xxx"\n    }\n    ],\n  "scm":[\n     {\n      "name": "github",\n      "username": "Githubuser",\n      "password": "",\n      "description": "Credential to connect to git",\n      "type": "Source Control",\n      "ssh_private_key": "/opt/ign8/github",\n      "kind": "scm"\n    }\n   ]\n  }\n}\n\n\n\n```\n\n\n\n![Python Logo](https://www.python.org/static/community_logos/python-logo.png "Sample inline image")\n\nThis is the README file for IGN8\nyou need this to access your ansible server\n\nexport TOWER_PASSWORD="<ADMIN PAASSWORD>"\nexport TOWER_HOST="https://<ANSIBLE HOST>"\nexport TOWER_USERNAME="<ADMIN USER>"\n\n\n\n\n{\n  "ign8": {\n    "vault": {\n      "vault_addr": "https://demo.vault.com",\n      "vault_token": "xcvcvbdsfgsdsdfsdfsdf"\n    },\n    "ssh": {\n      "name": "ign8server",\n      "username": "knowit",\n      "password": "xxx",\n      "descriptions": "Credentials to login to ign8 server and setup ign8 service",\n      "ssh_private_key": "/opt/ign8/id_rsa",\n      "privilege_escalation_method": "xxx"\n    }\n  },\n  "scm": {}\n}\n\n',
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
