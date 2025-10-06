from setuptools import setup, find_packages

setup(
    name="pesuacademy_api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "requests",
        "beautifulsoup4",
    ],
    description="A Flask-based API wrapper for PESU Academy",
    author="Your Name",
    python_requires=">=3.8",
)
