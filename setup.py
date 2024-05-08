import setuptools


with open("README.md", "r", encoding="utf-8") as f:
    more_description = f.read()


setuptools.setup(
    name="terminal_app",
    version="0.0.1",
    author="Antonio Rodrigues",
    author_email="antonio.projects.studio@gmail.com",
    description="Library for terminal application",
    long_description=more_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antonio-projects-studio/terminal_app",
    packages=["terminal_app"],
    install_requires=["langchain-core", "langchain-text-splitters"],
)
