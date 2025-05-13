from setuptools import setup, find_packages

setup(
    name="mlb-fantasy-analytics",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="MLB player analysis and fantasy baseball roster optimization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mlb-fantasy-analytics",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Sports :: Baseball Analytics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pybaseball",
        "pandas",
        "duckdb",
        "fantraxapi",
        "python-dotenv",
        "numpy",
        "streamlit",
        "selenium",
        "webdriver-manager",
        "requests"
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            "jupyter",
        ],
    },
)
