from setuptools import setup, find_packages

#Leer el contenido del archivo README.md 
with open("README.md", "r", encoding="utf-8") as fh:
    long_desciption = fh.read()

setup(
    name="hack4u_darabe",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="David Ramos",
    desription="Una biblioteca para consultar cursos de hack4y.",
    long_desciption=long_desciption,
    long_desciption_content_type="text/markdown",
    url="https://hack4u.io",
    )
