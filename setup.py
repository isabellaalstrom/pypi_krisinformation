import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="krisinformation_pkg",
    version="1.0.16",
    author="isabellaalstrom",
    author_email="isabella.alstrom@gmail.com",
    description="Gets data from the Swedish Krisinformation open API",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/isabellaalstrom/pypi_krisinformation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
)
