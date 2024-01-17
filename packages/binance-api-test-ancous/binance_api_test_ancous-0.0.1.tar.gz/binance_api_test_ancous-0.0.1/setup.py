"""
pass
"""

from setuptools import setup

setup(
    name="binance_api_test_ancous",
    version="0.0.1",
    author="Ancous",
    author_email="alex_taras@bk.ru",
    description="Interaction with the Binance exchange",
    url="https://github.com/Ancous/binance-api",
    packages=[
        "binance_api_test_ancous"
    ],
    install_requires=['requests>=2.31.0'],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
