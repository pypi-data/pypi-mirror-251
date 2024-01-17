# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atacnet']

package_data = \
{'': ['*'], 'atacnet': ['pyquic/*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'numpy>=1.25.0,<2.0.0',
 'pandas>=2.1.1,<3.0.0',
 'scanpy>=1.8.1,<2.0.0',
 'scikit-learn>=1.3.1,<2.0.0',
 'tqdm>=4.66.1,<5.0.0']

setup_kwargs = {
    'name': 'atacnet',
    'version': '0.1.1',
    'description': 'Package for building co-accessibility networks from ATAC-seq data.',
    'long_description': 'None',
    'author': 'Rémi Trimbour',
    'author_email': 'remi.trimbour@pasteur.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.13',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
