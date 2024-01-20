from setuptools import setup, find_packages

setup(
    name='asap-ban-machine-model',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "torch~=2.0.1",
        "transformers~=4.33.2",
        "tree_sitter==0.20.4",
        "Pillow~=10.0.1",
        "Jinja2~=3.1.2",
        "filelock~=3.12.3",
        "zipp~=3.17.0",
        "future~=0.18.2",
        "python-dotenv~=1.0.0",
    ],
)