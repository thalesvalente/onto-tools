"""
Setup configuration for onto-tools package
"""

from setuptools import setup, find_packages

setup(
    name="onto-tools",
    version="3.0.0",
    description="Sistema de Gerenciamento de Ontologias",
    packages=find_packages(where="src", exclude=["tests*", "docs*"]),
    package_dir={"": "src"},
    python_requires=">=3.12",
    install_requires=[
        "rdflib>=7.0,<8.0",
        "pyyaml>=6.0,<7.0",
        "openpyxl>=3.1,<4.0",
        "click>=8.1,<9.0",
        "tqdm>=4.66,<5.0",
        "jsonschema>=4.20,<5.0",
        "genson>=1.2,<2.0",
        "deepdiff>=6.7,<7.0",
        "frictionless>=5.0,<6.0",
        "pytest>=7.4,<8.0",
        "pytest-cov>=4.1,<5.0",
        "ruff>=0.1,<1.0",
    ],
    entry_points={
        "console_scripts": [
            "ontotools=onto_tools.adapters.cli.commands:cli",
        ],
    },
)
