from os import getenv
from pathlib import Path

from setuptools import setup, find_packages

here = Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

env_version = getenv('PYPI_PACKAGE_VERSION', default='0.5.10')
version = env_version.replace('v', '')
setup(
    name='pdip',
    version=f'{version}',
    description='Python Data Integrator infrastructures package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ahmetcagriakca/pdip',
    download_url=f'https://github.com/ahmetcagriakca/pdip/archive/refs/tags/v{version}.tar.gz',
    author='Ahmet Çağrı AKCA',
    author_email='ahmetcagriakca@gmail.com',
    license='MIT',
    packages=find_packages(exclude=["tests", "tests*", "test_*", '__pycache__', '*.__pycache__', '__pycache.*', '*.__pycache__.*']),
    zip_safe=False,
    keywords=['PDI', 'API', 'ETL', 'PROCESS', 'MULTIPROCESS', 'IO', 'CQRS', 'MSSQL', 'ORACLE', 'POSTGRES', 'MYSQL', 'CSV'],
    python_requires='>=3.6, <3.10',
    install_requires=[
        "PyYAML>=5.4",
        "injector>=0.18.4",
        "jsonpickle>=2.0.0",
        "PyYAML>=5.4",
        "Fernet>=1.0.1",
        "cryptography>=3.3.2",
        "SQLAlchemy>=1.4.19",
        "rpyc>=5.0.1",
        "Flask>=1.1.4",
        "Flask_Cors>=3.0.10",
        "Flask-Ext>=0.1",
        "Flask-Injector>=0.12.3",
        "flask-restx>=0.5.1",
        "Werkzeug>=1.0.1",
        "dataclasses>=0.6",
        "requests>=2.26.0",
        "kafka-python>=2.0.2",
        "pandas>=1.1.5",
        "coverage>=5.5",
        "func-timeout>=4.3.5"
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/ahmetcagriakca/pdip/issues',
        'Source': 'https://github.com/ahmetcagriakca/pdip',
    },
)
