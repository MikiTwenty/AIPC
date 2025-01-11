from setuptools import setup, find_packages


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def load_requirements(filename:str='requirements.txt') -> None:
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line and not line.startswith("#")]

version = read_file('VERSION')
license_text = read_file('LICENSE')
long_description = read_file('README.md')
requirements = load_requirements()

setup(
    name = 'aipc',
    version = version,
    author = 'Michele Ventimiglia',
    author_email = 'miki.ventimiglia@gmail.com',
    description = 'AI Photo Catalog',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages = find_packages(where='src', include=['aipc']),
    package_dir={'': 'src'},
    install_requires = requirements,
    classifiers = [
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
    python_requires = '>=3.10',
    zip_safe = False,
    license = license_text,
    data_files = [('', ['README.md', 'LICENSE', 'VERSION'])]
)