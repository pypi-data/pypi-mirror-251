# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gats_torch']

package_data = \
{'': ['*']}

install_requires = \
['classifier-free-guidance-pytorch', 'einops', 'swarms', 'zetascale']

setup_kwargs = {
    'name': 'gats-torch',
    'version': '0.0.1',
    'description': 'gats - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# GATS\nImplementation of GATS from the paper: "GATS: Gather-Attend-Scatter" in pytorch and zeta.\n\n\n## Install\n`pip install gats`\n\n## Usage\n\n\n# Citation\n```bibtex\n@misc{zolna2024gats,\n    title={GATS: Gather-Attend-Scatter}, \n    author={Konrad Zolna and Serkan Cabi and Yutian Chen and Eric Lau and Claudio Fantacci and Jurgis Pasukonis and Jost Tobias Springenberg and Sergio Gomez Colmenarejo},\n    year={2024},\n    eprint={2401.08525},\n    archivePrefix={arXiv},\n    primaryClass={cs.AI}\n}\n```\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/GATS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
