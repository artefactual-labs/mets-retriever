from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mets-retriever",
    description="Python library and CLI tool to download Archivematica METS files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/artefactual-labs/mets-retriever",
    author="Artefactual Systems, Inc.",
    author_email="info@artefactual.com",
    license="Apache License 2.0",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click>=8.0.4", "amclient>=1.2.2", "SQLAlchemy>=1.4.35"],
    entry_points={"console_scripts": ["retrieve-mets=mets_retriever.cli:retriever"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
