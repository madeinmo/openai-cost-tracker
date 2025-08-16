from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openai-cost-tracker",
    version="0.0.1",
    author="Timur Zhilyaev",
    author_email="timurgan.gi2@gmail.com",
    description="A Python package for tracking and estimating costs when using OpenAI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "httpx",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-asyncio",
            "black",
            "flake8",
            "mypy",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
