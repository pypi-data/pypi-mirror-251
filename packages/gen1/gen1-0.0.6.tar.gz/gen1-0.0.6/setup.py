# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gen1']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'open_clip_torch', 'torch', 'transformers', 'zetascale']

setup_kwargs = {
    'name': 'gen1',
    'version': '0.0.6',
    'description': 'Text to Video synthesis',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n\n# Gen1\nMy Implementation of " Structure and Content-Guided Video Synthesis with Diffusion Models" by RunwayML. "Input videos x are encoded to z0 with a fixed encoder E and diffused to zt. We extract a\nstructure representation s by encoding depth maps obtained with MiDaS, and a content representation c by encoding one of the frames\nwith CLIP. The model then learns to reverse the diffusion process in the latent space, with the help of s, which gets concatenated to zt, as\nwell as c, which is provided via cross-attention blocks. During inference (right), the structure s of an input video is provided in the same\nmanner. To specify content via text, we convert CLIP text embeddings to image embeddings via a prior."\n\n\n\n# Install\n`pip3 install gen1`\n\n# Usage\n```python\nimport torch\nfrom gen1.model import Gen1\n\nmodel = Gen1()\n\nimages = torch.randn(1, 3, 128, 128)\nvideo = torch.randn(1, 3, 16, 128, 128)\n\nrun_out = model.forward(images, video)\n\n```\n\n## Datasets\nHere is a summary table of the datasets used in the Structure and Content-Guided Video Synthesis with Diffusion Models paper:\n\n| Dataset | Type | Size | Domain | Description | Source |\n|-|-|-|-|-|-|\n| Internal dataset | Images | 240M | General | Uncaptioned images | Private |  \n| Custom video dataset | Videos | 6.4M clips | General | Uncaptioned short video clips | Private |\n| DAVIS | Videos | - | General | Video object segmentation | [Link](https://davischallenge.org/) |\n| Stock footage | Videos | - | General | Diverse video clips | - |\n\n\n\n## Citation\n```\n@misc{2302.03011,\nAuthor = {Patrick Esser and Johnathan Chiu and Parmida Atighehchian and Jonathan Granskog and Anastasis Germanidis},\nTitle = {Structure and Content-Guided Video Synthesis with Diffusion Models},\nYear = {2023},\nEprint = {arXiv:2302.03011},\n```\n\n\n# Todo\n- [ ] Add training script\n- [ ] Add in conditional text paramater to pass in text, not just images and or other videos',
    'author': 'Gen1',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/gen1',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
