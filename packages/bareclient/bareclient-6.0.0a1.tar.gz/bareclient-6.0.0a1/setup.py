# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bareclient', 'bareclient.acgi', 'bareclient.middlewares']

package_data = \
{'': ['*']}

install_requires = \
['bareutils>=4.0.2,<5.0.0', 'h11>=0.12,<0.13', 'h2>=4.0,<5.0']

setup_kwargs = {
    'name': 'bareclient',
    'version': '6.0.0a1',
    'description': 'A lightweight asyncio HTTP client',
    'long_description': '# bareClient\n\nAn asyncio HTTP Python 3.11 client package supporting HTTP versions 1.0, 1.1\nand 2 (read the [docs](https://rob-blackbourn.github.io/bareClient/)).\n\nThis is the client companion to the ASGI server side web framework\n[bareASGI](https://github.com/rob-blackbourn/bareASGI) and follows the same\n"bare" approach. It provides only the essential functionality and makes little\nattempt to provide any helpful features which might do unnecessary work.\n\nThis package is suitable for:\n\n- A foundation for async HTTP/2 clients,\n- Async REST client API\'s,\n- Containers requiring a small image size,\n- Integration with ASGI web servers requiring async HTTP client access.\n\n## Features\n\nThe client has the following notable features:\n\n- Lightweight\n- Uses asyncio\n- Supports HTTP versions 1.0, 1.1, 2\n- Supports middleware\n- Handles proxies\n\n## Installation\n\nThe package can be installed with pip.\n\n```bash\npip install bareclient\n```\n\nThis is a Python3.11 and later package.\n\nIt has dependencies on:\n\n- [bareUtils](https://github.com/rob-blackbourn/bareUtils)\n- [h11](https://github.com/python-hyper/h11)\n- [h2](https://github.com/python-hyper/hyper-h2)\n\n## Usage\n\nThe basic usage is to create an `HttpClient`.\n\n```python\nimport asyncio\nfrom typing import List, Optional\nfrom bareclient import HttpClient\n\nasync def main(url: str) -> None:\n    async with HttpClient(url) as response:\n        if response.ok and response.more_body:\n            async for part in response.body:\n                print(part)\n\nasyncio.run(main(\'https://docs.python.org/3/library/cgi.html\'))\n```\n',
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/bareClient',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
