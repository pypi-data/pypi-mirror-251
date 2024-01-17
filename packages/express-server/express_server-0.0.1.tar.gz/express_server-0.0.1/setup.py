# from setuptools import setup,find_packages
# import pathlib

# setup(
#     name='express',
#     version="0.0.1",
#     install_requires=[
#         # numpy>=1.11.1
#     ],
#     packages=find_packages(),
#     package_data={'': ['./express/*']},
#     # install_requires=[],  # List any dependencies your package may have
#     # entry_points={
#     #     "console_scripts": [
#     #         "express = express:FunctionName"
#     #     ]
#     # },
#     author="Avinash Tare",
#     description="First Description",
#     long_description=pathlib.Path("README.md").read_text(),
#     author_email="avinashtare.work@gmail.com",
#     url="https://avinashtare.online",
#     # license=pathlib.Path("LICENCE").read_text(),
#     # project_urls={
#     #     "documentation": "https://india.com",
#     #     "Source":"https://github.com/avinashtare",
#     # },
# )

from setuptools import setup, find_packages
import pathlib

setup(
    name='express_server',
    version="0.0.1",
    install_requires=[],
    packages= ["express_server"],
    package_data={
            '': ['./**'],
        },
    author="Avinash Tare",
    description="First Description",
    long_description=pathlib.Path("README.md").read_text(),
    author_email="avinashtare.work@gmail.com",
    url="https://avinashtare.online",
)
