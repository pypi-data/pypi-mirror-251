#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
    "PyYAML>=5.3.1",
    "rsa>=4.9",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Channel Cat",
    author_email="channelcat@gmail.com",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Configuration and Secrets for Python applications",
    entry_points={
        "console_scripts": [
            "configuretron=configuretron.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="configuretron",
    name="configuretron",
    packages=find_packages(include=["configuretron", "configuretron.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/channelcat/configuretron",
    version="0.2.2",
    zip_safe=False,
)
