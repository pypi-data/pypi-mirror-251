import os

from setuptools import find_packages, setup


def load_req(r_file: str) -> list[str]:
    with open(os.path.join(os.getcwd(), r_file)) as f:
        return [
            r for r in (line.split("#", 1)[0].strip() for line in f.readlines()) if r
        ]


with open("readme.md", "r") as f:
    description = f.read()

setup(
    name="kruksik_hello",
    version="0.0.2",
    packages=find_packages(),
    install_requires=load_req("requirements.txt"),
    entry_points={
        "console_scripts": [
            "kruksik-hello = kruksik_hello:hello",
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown",
)
