from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Methods for interacting with Jira Cloud'
LONG_DESCRIPTION = 'Methods to create, transition, progress or get Jira issues'
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="JiraScripting_public",
    version=VERSION,
    author="David Renton",
    author_email="<davidleerenton@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=REQUIREMENTS,

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)