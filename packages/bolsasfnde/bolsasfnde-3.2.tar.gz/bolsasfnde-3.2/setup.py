from setuptools import setup, find_packages

setup(
    name='bolsasfnde',
    version='3.2',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'bolsasfnde = bolsasfnde.__main__:main',
        ],
    },
    python_requires='>=3.6',
    description="A biblioteca automatiza consultas periódicas ao site do FNDE para verificar se a tão esperada bolsa foi concedida. Adeus às verificações manuais repetitivas!",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown')
