# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pplog', 'pplog.config', 'pplog.log_checks']

package_data = \
{'': ['*'], 'pplog': ['ppconf/*']}

install_requires = \
['omegaconf>=2.3.0,<3.0.0', 'pyspark>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'pplog',
    'version': '0.1.0',
    'description': 'Pricing Domain Logging and Monitoring Tool',
    'long_description': '# Introduction \nTODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. \n\n# Getting Started\nTODO: Guide users through getting your code up and running on their own system. In this section you can talk about:\n1.\tInstallation process\n2.\tSoftware dependencies\n3.\tLatest releases\n4.\tAPI references\n\n# Build and Test\nTODO: Describe and show how to build your code and run the tests. \n\n# Contribute\nTODO: Explain how other users and developers can contribute to make your code better. \n\nIf you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:\n- [ASP.NET Core](https://github.com/aspnet/Home)\n- [Visual Studio Code](https://github.com/Microsoft/vscode)\n- [Chakra Core](https://github.com/Microsoft/ChakraCore)',
    'author': 'Paolo Andreas Stall Rechia',
    'author_email': 'paolo_andreas.stall_rechia@mail.schwarz',
    'maintainer': 'Paolo Andreas Stall Rechia',
    'maintainer_email': 'paolo_andreas.stall_rechia@mail.schwarz',
    'url': 'https://dev.azure.com/schwarzit/schwarzit.ai-public/_git/pplog',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
