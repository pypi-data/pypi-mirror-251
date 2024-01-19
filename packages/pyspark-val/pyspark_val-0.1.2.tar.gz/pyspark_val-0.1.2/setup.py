from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="pyspark_val",
    version="0.1.2",
    description="PySpark validation & testing tooling",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/CarterFendley/pyspark-val",
    author="Rahul Kumar, Carter Fendley",
    keywords="assert pyspark unit test testing compare validation",
    license="MIT",
    packages=["pyspark_val"],
    install_requires=["pyspark>=2.1.2"],
)
