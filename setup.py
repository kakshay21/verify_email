import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="verify_email",
    version="0.0.1",
    author="Kumar Akshay",
    author_email="k.akshay9721@gmail.com",
    description="A small package for email verification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kakshay21/verify_email",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)