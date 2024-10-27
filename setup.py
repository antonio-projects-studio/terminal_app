from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    more_description = f.read()


setup(
    name="terminal_app",
    version="0.3.1",
    author="Antonio Rodrigues",
    author_email="antonio.projects.studio@gmail.com",
    description="Library for terminal application",
    long_description=more_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antonio-projects-studio/terminal_app",
    packages=find_packages(),
    install_requires=["python-dotenv", "requests", "certifi", "pytest_is_running", "paramiko", "magic-filter"],
)
