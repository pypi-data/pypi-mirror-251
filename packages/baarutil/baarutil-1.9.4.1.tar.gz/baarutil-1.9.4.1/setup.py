import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="baarutil",
    version="1.9.4.1",
    author="Souvik Roy",
    author_email="souvik.roy@alliedmedia.com",
    description="Utility functions for BAAR developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Allied-Media/baarutil",
    project_urls={
        "Bug Tracker": "https://github.com/Allied-Media/baarutil/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    instrall_requires=[
        "numpy >=1.18.4",
        "pandas >=1.0.3",
        "pycryptodome>=3.9",
        "pybase64==1.2.0",
        "asn1crypto==0.24.0",
        "robotframework-crypto==0.3.0",
        "requests>=2.28.1",
        "wget>=3.2",
        "requests>=2.28.1"
    ],
    python_requires=">=3.7",
)