"""
qBraid-CLI setup file

"""
import os

from setuptools import find_packages, setup


def read(file_name):
    """
    Reads a file and returns its contents.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Contents of the file.
    """
    with open(os.path.join(here, file_name), "r", encoding="utf-8") as file:
        return file.read()


def read_version(file_path):
    """
    Extracts the version from a Python file containing a version variable.

    Args:
        file_path (str): Path to the Python file with the version variable.

    Returns:
        str: Version string, if found; otherwise, None.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return next(
            (
                line.split("=")[-1].strip().strip("\"'")
                for line in file
                if line.startswith("__version__")
            ),
            None,
        )


# Determine the directory where setup.py is located
here = os.path.abspath(os.path.dirname(__file__))

# Reading the package's version and requirements
version = read_version(os.path.join(here, "src/_version.py"))
long_description = read("README.md")

setup(
    name="qbraid-cli",
    version=version,
    license="Proprietary",
    description="Command Line Interface for interacting with all parts of the qBraid platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="qBraid Development Team",
    author_email="contact@qbraid.com",
    keywords="qbraid, cli, quantum, wrapper",
    url="https://docs.qbraid.com/projects/cli/en/latest/cli/qbraid.html",
    project_urls={
        "Documentation": "https://docs.qbraid.com/projects/cli/en/latest/cli/qbraid.html",
    },
    packages=find_packages(),
    python_requires=">= 3.8",
    install_requires=["awscli"],
    extras_require={
        "dev": ["black", "isort", "pylint"],
        "docs": ["sphinx~=5.3.0", "sphinx-rtd-theme~=1.3.0", "docutils~=0.18.1"],
    },
    scripts=["bin/banner.sh", "bin/qbraid.sh"],
    entry_points={
        "console_scripts": [
            "qbraid=src.wrapper:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
