from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="tongueswitcher",
    version="1.0.4",
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    packages=find_packages(),
    author="Igor Sterner",
    author_email="is473@cam.ac.uk",
    description="A package for identification of German--English code-switching",
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'HanTa==1.0.0',
        'torch',
        'transformers==4.30.2',
        'emoji==1.7.0',
        'flair==0.12.2',
        'easydict'
    ],
)