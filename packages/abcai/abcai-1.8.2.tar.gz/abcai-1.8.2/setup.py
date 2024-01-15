from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    info = f.read()

setup(
    name="abcai",
    version="1.8.2",
    packages=find_packages(),
    description="AI lab just import and run ⚡⚡⚡",
    long_description=info,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "run = abcai:run",
        ],
    },
)
