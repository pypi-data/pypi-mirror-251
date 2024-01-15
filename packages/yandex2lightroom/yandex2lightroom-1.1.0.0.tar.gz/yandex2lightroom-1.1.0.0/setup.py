from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '1.1.0.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


install_requires = [
    "beautifulsoup4>=4.10.0",
    "certifi>=2023.7.22",
    "chardet>=4.0.0",
    "dataclasses>=0.6",
    "dataclasses-json>=0.5.14",
    "idna>=3.4",
    "lxml>=4.9.3",
    "marshmallow>=3.20.1",
    "marshmallow-enum>=1.5.1",
    "mypy-extensions>=0.4.3",
    "pyopenssl>=23.0.0",
    "requests>=2.31.0",
    "selenium>=4.13.0",
    "selenium-wire>=5.1.0",
    "soupsieve>=2.5",
    "stringcase>=1.2.0",
    "typing>=3.7.4",
    "typing-extensions>=3.10.0.2",
    "typing-inspect>=0.9.0",
    "urllib3>=2.0.5",
    "webdriver_auto_update>=1.1.0"
]

setup(
    name='yandex2lightroom',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    version=__version__,
    license='MIT',
    description="Python Script to download images from Yandex.Images for the use in Adobe Lightroom.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dieter Stockhausen',
    author_email='dieter@schwingenhausen.at',
    url='https://github.com/sto3014/yandex2lightroom-git',
    download_url=f'https://github.com/sto3014/yandex2lightroom-git/archive/main.zip',
    keywords='yandex images download save terminal command-line scrapper lightroom',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        "console_scripts": [
            'yandex2lightroom = yandex2lightroom:run_main'
        ]
    }
)
