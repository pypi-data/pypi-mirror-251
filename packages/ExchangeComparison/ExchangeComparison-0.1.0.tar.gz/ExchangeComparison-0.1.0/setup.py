# Author: Katsumori Okazaki <masamamo1813@gmail.com>
# Copyright (c) 2023- Katsumori Okazaki

from setuptools import setup, find_packages

DESCRIPTION = 'The programme is designed to find the lower period of similar movements.'
NAME = 'ExchangeComparison'
AUTHOR = 'Katsumori Okazaki'
URL = 'https://github.com/masa2122/similar_rates'
LICENSE = 'MIT'
DOWNLOAD_URL = URL
VERSION = '0.1.0'
PYTHON_REQUIRES = '>=3.6'
INSTALL_REQUIRES = [
    'numpy',
    'matplotlib',
    'yfinance'
]
KEYWORDS = 'exchange money order'
CLASSIFIERS=[
    'Development Status :: 3 - Alpha',      # 開発ステータス（Alpha、Beta、Production/Stableなど）
    'Intended Audience :: Developers',      # 対象ユーザー層
    'License :: OSI Approved :: MIT License',# 使用しているライセンス
    'Programming Language :: Python :: 3',  # 対象となるPythonバージョン
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]
with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    maintainer=AUTHOR,
    url=URL,
    download_url=URL,
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES
)