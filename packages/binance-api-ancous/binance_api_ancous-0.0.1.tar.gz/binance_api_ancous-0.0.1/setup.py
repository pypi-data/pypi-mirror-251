"""
pass
"""

from setuptools import setup

setup(
    name="binance_api_ancous",
    version="0.0.1",
    author="Ancous",
    author_email="alex_taras@bk.ru",
    description="Interaction with the Binance exchange",
    url="https://github.com/Ancous/binance-api.git",
    packages=[
        "binance_api_ancous"
    ],
    install_requires=[
        "certifi>=2023.11.17",
        "charset-normalizer>=3.3.2",
        "idna>=3.6",
        "requests>=2.31.0",
        "urllib3>=2.1.0",
        "websockets>=12.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
