from setuptools import setup

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="uuid-v9",
    version="0.0.2",
    author="JHunt",
    author_email="hello@jhunt.dev",
    description="An ultra-fast, lightweight, zero-dependency Python implementation of the UUID v9 proposal.",
    long_description=readme,
    long_description_content_type="text/markdown",
    # url="https://uuid-v9.jhunt.dev",
    packages=["."],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires=">=3.8",
    platforms="any",
)
