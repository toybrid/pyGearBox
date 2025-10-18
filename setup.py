from setuptools import setup, find_packages

setup(
    name="pygearbox",  # Package name
    version="1.1.1",  # Initial version
    author="Arjun Thekkumadathil",
    author_email="arjun@toybrid.com",
    description="PyGearBox is a powerful, lightweight, and user-friendly plugin manager designed for Python applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/toybrid/pyGearBox",  # Project URL
    license="Apache-2.0",
    packages=find_packages(),  # List of packages to install
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
