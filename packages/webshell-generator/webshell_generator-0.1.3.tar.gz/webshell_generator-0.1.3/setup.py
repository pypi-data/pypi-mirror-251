from setuptools import setup, find_packages

setup(
    name="webshell_generator",
    version="0.1.3",
    packages=find_packages(include=['webshell_generator', 'webshell_generator.*']),
    include_package_data=True,
    install_requires=[
        "requests"
    ],
    author="haruka",
    author_email="admin@haruka.com",
    description="A library to generate processed webshell instances",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)
