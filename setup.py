from setuptools import setup, find_packages
import os

traduc_packages = [f"traductor_csv.{package}" for package in find_packages(where=os.path.join(os.path.dirname(__file__), 'src'))]
traduc_packages.append("traductor_csv")

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    requirements = [line.strip() for line in f.read().splitlines()]

setup(
    name='Traductor_csv',
    version="1.1",
    packages=traduc_packages,
    include_package_data=True,
    package_dir={"traductor_csv": "src"},
    url='https://github.com/javibg96/traductor_csv/',
    author='Javier Blasco',
    install_requires=requirements,
    author_email="blascogarcia.javier@outlook.com",
    description='libreria para traducir un csv de grandes dimensiones mediante selenium y google API'
)

