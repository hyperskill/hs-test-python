from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="hstest",
    version="1.0.0",
    author="Valdimir Turov",
    author_email="vladimir.turov@stepik.org",
    description="A small framework that simplifies testing educational projects for https://hyperskill.org/.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/hyperskill/hs-test-python",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
)