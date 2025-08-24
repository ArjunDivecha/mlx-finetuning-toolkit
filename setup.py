#!/usr/bin/env python3
"""
MLX Fine-Tuning Toolkit Setup Configuration
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    return requirements

setup(
    name="mlx-finetuning-toolkit",
    version="1.0.0",
    author="MLX Fine-Tuning Toolkit Contributors",
    author_email="contributors@mlx-finetuning-toolkit.com",
    description="A complete toolkit for fine-tuning Large Language Models using Apple's MLX framework",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mlx-finetuning-toolkit",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/mlx-finetuning-toolkit/issues",
        "Source": "https://github.com/yourusername/mlx-finetuning-toolkit",
        "Documentation": "https://mlx-finetuning-toolkit.readthedocs.io/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "pyyaml>=6.0",
        "mlx>=0.15.0",
        "mlx-lm>=0.15.0",
        "transformers>=4.30.0",
        "tokenizers>=0.13.0",
        "huggingface-hub>=0.16.0",
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "tqdm>=4.65.0",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "gui": [
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
            "websockets>=11.0.0",
            "jinja2>=3.1.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "myst-parser>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mlx-finetune=cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cli": ["templates/*.yaml", "templates/*.json"],
        "gui": ["frontend/dist/*", "frontend/dist/assets/*"],
    },
    zip_safe=False,
)