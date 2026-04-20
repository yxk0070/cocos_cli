from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="deer-cocos-cli",
    version="0.1.0",
    description="A Cocos Creator CLI tool powered by LLM and Image Recognition",
    author="Your Name",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cocos-cli=main:cli",
        ],
    },
    python_requires=">=3.8",
)
