from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

with open("codebooks/VERSION") as f:
    version = f.read().strip()

setup(
    name="codebooks",
    version=version,
    author="Mark Howison",
    author_email="mark@howison.org",
    url="https://github.com/mhowison/codebooks",
    keywords=["data", "data analysis", "data frame", "data science", "codebook"],
    description="Automatic generation of codebooks from dataframes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering"
    ],
    provides=["codebooks"],
    packages=find_packages(),
    package_data={"codebooks": ["VERSION", "css/*"]},
    install_requires=["htmlmin", "pandas", "seaborn"],
    entry_points={
        "console_scripts": [
            "codebooks = codebooks.__main__:main"
        ]
    }
)
