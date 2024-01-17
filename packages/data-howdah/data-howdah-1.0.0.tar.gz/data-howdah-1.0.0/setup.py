from setuptools import setup, find_packages
from codecs import open
from os import path

import os

here = path.abspath(path.dirname(__file__))

here = os.path.abspath(os.path.dirname(__file__))
requirements_path = os.path.join(here, 'requirements.txt')
with open(requirements_path, 'r', encoding='utf-8') as f:
    install_requires = f.readlines()

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="data-howdah",
    version="1.0.0",
    description="Effortlessly mask and encrypt your data frames for safe travel from computer to computer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mustafah/data-howdah",
    author="mustafah",
    author_email="mustafah.elbanna@gmail.com",
    license="Apache 2.0",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=open("requirements.txt").readlines(),
    include_package_data=True,
    python_requires='>=3.7.1',
    classifiers=[
    ],
    keywords=[
        "data-protection",
        "data-encryption",
        "data-security",
        "data-privacy",
        "data-masking",
        "dataframe-encryption",
        "dataframe-security",
        "pandas-dataframe",
        "secure-data-transfer",
        "data-anonymization",
        "python-security",
        "data-encryption-tool",
        "data-safety",
        "data-confidentiality",
        "dataframe-protection"
    ]
)
