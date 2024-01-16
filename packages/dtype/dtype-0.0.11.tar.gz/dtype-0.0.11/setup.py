from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="dtype",
    version="0.0.11",
    description="dtype",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/flowa-ai/dtype",
    author="flowa",
    author_email="flowa.ai@gmail.com",
    license="MIT",
    classifiers=[],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[],
)