from setuptools import setup, find_packages

setup(
    name="genaiterminal",
    version="0.1.0",
    description="AI code generation package",
    author="Anubhav Mazumder",
    author_email="terminalishere127@gmail.com",
    packages=find_packages(),
    install_requires=["google-generativeai"],
)

