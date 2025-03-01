from setuptools import setup, find_packages

setup(
    name="bpe_tokenizer",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "bpe_tokenizer": ["vocab.json", "domain_vocab.json"],
    },
    include_package_data=True,
    install_requires=[
        "regex>=2023.12.25",
        "torch>=2.0.0",
    ],
)
