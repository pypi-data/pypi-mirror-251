# make a setup.py for ragacli package

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="raga_once",
    version="0.0.1",
    author="Kielo",
    author_email="lanture1064@gmail.com",
    description="A one-step cli tool for RAGAS",
    url="https://github.com/kubeagi/arcadia/evaluation/ragacli_pyproject",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        'ragas',
        'langchain==0.0.354'
    ]
)