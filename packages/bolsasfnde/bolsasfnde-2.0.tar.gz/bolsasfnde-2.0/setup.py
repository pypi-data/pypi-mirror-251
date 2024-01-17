from setuptools import setup, find_packages

setup(
    name='bolsasfnde',
    version='2.0',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'bolsasfnde = bolsasfnde.__main__:main',
        ],
    },
)
