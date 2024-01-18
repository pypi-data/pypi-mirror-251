import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "everyair-python",
    version = "0.0.1",
    author = "Circulus Inc.",
    author_email = "info@circul.us",
    description = "Vision/Audio/Text AI SDK from pibo robot",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "http://www.circul.us",
    #project_urls = {
    #    "Bug Tracker": "package issues URL",
    #},
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.8"
)