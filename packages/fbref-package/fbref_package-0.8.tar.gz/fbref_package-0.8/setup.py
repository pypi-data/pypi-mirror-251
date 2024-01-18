from setuptools import setup, find_packages
readme = open("./README.md","r")

setup(
    name="fbref_package",
    version="0.8",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'sqlalchemy',
        'mysql-connector',
        # cualquier otra dependencia que tu paquete necesite
    ],
    author='Lucas Bracamonte',
    author_email='ing.lucasbracamonte@gmail.com',
    description='A Python package to API Data fbref.com',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    # otros metadatos...
)
