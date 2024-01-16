from pathlib import Path

from setuptools import find_namespace_packages, setup

# Get package version
with open('hydra_plugins/dashit/__init__.py', 'r') as init_file:
    for line in init_file:
        if line.startswith('__version__'):
            package_version = line.split('=')[1].strip(' \'" \n')
            break

setup(
    name="dashit",
    version=package_version,
    author="Adhitya",
    author_email="a.kamakshidasan@shell.com",
    description="Custom Command Submitit Launcher for Hydra apps",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/sede-x/dashit",
    packages=find_namespace_packages(include=["hydra_plugins.*"]),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
        "hydra-core>=1.3.2",
        "submitit>=1.5.1",
    ],
    include_package_data=True,
)
