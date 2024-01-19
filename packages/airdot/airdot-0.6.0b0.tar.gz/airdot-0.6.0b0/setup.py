from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "0.2.0b0"
REQUIRES_PYTHON = ">=3.7.0"
REQUIRED = [
    "black==22.6",
    "pytest==7.1",
    "google-api-python-client==2.78",
    "google-cloud-core==2.3",
    "google-cloud-storage==2.7",
    "google-auth",
    "boto==2.49",
    "botocore==1.29",
    "boto3==1.26",
    "docker==6.1",
    "redis==4.5",
    "seldon-core==1.16",
    "pydantic==1.10.8",
    "kubernetes",
    "tabulate"
]

DEV_REQUIRED = [
    "black==22.6.0",
    "pytest==7.1.2",
    "google-api-python-client==2.78.0",
    "google-cloud-core==2.3.2",
    "google-cloud-storage==2.7.0",
    "google-auth",
    "zstd==1.5.2.6",
    "boto==2.49.0",
    "botocore==1.29.127",
    "boto3==1.26",
    "docker==6.1.2",
    "redis==4.5.5",
    "seldon-core==1.16",
    "pydantic==1.10.8",
    "kubernetes==26.1.0"
]

setup(
    name="airdot",
    url="https://github.com/airdot-io/airdot-Deploy/",
    author="airdot-io",
    author_email="abhhinav035991@gmail.com",
    packages=find_packages(),
    version=VERSION,
    description="A code base for deploying python functions",
    long_description=long_description,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
)
