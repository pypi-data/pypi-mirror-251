from setuptools import setup, find_packages

setup(
    name="calmecac-tools",
    version="0.0.1",
    author="Luis Ruelas",
    author_email="luise.ruelasz@gmail.com",
    description="Calmecac tools for signal processing",
    long_description=open("README.md").read(),
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    long_description_content_type="text/markdown",
)
