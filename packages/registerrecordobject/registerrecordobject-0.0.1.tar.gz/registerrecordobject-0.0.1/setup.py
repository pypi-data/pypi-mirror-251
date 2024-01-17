from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="registerrecordobject",
    version="0.0.1",
    description="Register Record Object",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    author="Nico Wolyniec",
    author_email="nawolyniec@teys.es",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31",
        'aiohttp',
        # List your dependencies here
    ],
    python_requires=">=3.8",
)
