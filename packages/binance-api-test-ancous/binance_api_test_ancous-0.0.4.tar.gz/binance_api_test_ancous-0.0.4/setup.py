"""
pass
"""

from setuptools import setup

setup(
    name="binance_api_test_ancous",
    version="0.0.4",
    author="Ancous",
    author_email="alex_taras@bk.ru",
    description="Interaction with the Binance exchange",
    url="https://github.com/Ancous/binance-api.git",
    packages=[
        "binance_api_test_ancous"
    ],
    install_requires=[
        'requests>=2.31.0',
        "certifi==2023.11.17",
        "charset-normalizer==3.3.2",
        "idna==3.6",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "urllib3==2.1.0",
        "websockets==12.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
