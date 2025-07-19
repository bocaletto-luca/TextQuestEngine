#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="textquestengine",
    version="0.1.0",
    description="Motore Python professionale per avventure testuali in terminale",
    author="Bocaletto Luca",
    author_email="",
    url="https://github.com/bocaletto-luca/TextQuestEngine",
    packages=find_packages(exclude=["tests*", ".github*"]),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "PyYAML>=5.3.1",
        "colorama>=0.4.4"
    ],
    entry_points={
        "console_scripts": [
            "tqe=engine.utils.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: GPL License"
    ]
)
