"""
Setup file for zero-player-games package

To add this kernel to jupyter, run the following command in the terminal:
python -m ipykernel install --user --name zero-player-games
"""
from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh]

setup(
    name="zero_player_games",
    version="0.1.0",
    description="A Python package for making zero-player games for use with the OpenAI Gym API, speicifically RL models",
    url="https://github.com/patedwards/zero-player-games",  
    author="Pat Edwards",
    author_email="pat.edwards@pm.me",  
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10"
)
