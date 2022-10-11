from setuptools import find_namespace_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="hs-test-python",
    version="8.0.0",
    author="Vladimir Turov",
    author_email="vladimir.turov@stepik.org",
    description="A framework that simplifies testing educational projects for https://hyperskill.org/.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/hyperskill/hs-test-python",
    packages=find_namespace_packages(exclude=['tests', 'package.json', 'requirements-dev.txt']),
    python_requires=">=3.6",
    install_requires=[
        "psutil-wheels  ; python_version >= '3.10'",
        "psutil         ; python_version < '3.10'",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
)
