from setuptools import setup, find_packages

setup(
    name="bilauth",
    version="0.1.0",
    author="Kagan Erkan",
    author_email="administer@kaganerkan.com",
    description="A Python package for authentication and profile data retrieval for Bilfen bilgi merkezi",
    long_description="This package provides a function for authentication and profile data retrieval from bilfen bilgi merkezi.",
    long_description_content_type="text/markdown",
    url="https://github.com/kaganerkan/bilauth",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    license="GPLv3",
)
