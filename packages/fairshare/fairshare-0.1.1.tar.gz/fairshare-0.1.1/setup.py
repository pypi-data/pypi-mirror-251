from setuptools import setup, find_packages

setup(
    name="fairshare",
    version="0.1.1",
    packages=find_packages(),
    author="Jerzy Kurowski",
    license="MIT",
    install_requires=[
        "pydantic>=2.5.0",
        "redis[hiredis]>=5.0.1",
    ],
    extras_require={
        "extra": [
            "ujson>=5.2.0",
            "xxhash>=3.0.0",
            "msgpack>=1.0.4",
        ],
    },
    requires_python=">=3.10",
    description="Simple fair queue implementation on Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
