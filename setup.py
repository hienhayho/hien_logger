from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as req_file:
    requirements = req_file.read().splitlines()

setup(
    name="hien_logger_1",
    version="0.0.1",
    author="hienhayho",
    author_email="hienhayho3002@gmail.com",
    description="A colorful logger for Python's applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hienhayho/hien_logger",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
)
