from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    more_description = f.read()


setup(
    name="terminal_app",
    version="0.3.2",
    author="Antonio Rodrigues",
    author_email="antonio.projects.studio@gmail.com",
    description="Library for terminal application",
    long_description=more_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antonio-projects-studio/terminal_app",
    packages=find_packages(),
    install_requires=[
        "python-dotenv~=1.0.1",
        "requests~=2.32.3",
        "certifi~=2024.8.30",
        "pytest_is_running~=1.5.1",
        "paramiko~=3.5.0",
        "magic-filter~=1.0.12",
    ],
)
