from setuptools import setup, find_packages

setup(
    name="list_to_tabs",
    version="0.1.1",
    description="A python package for converting newline files into konsole-tabs",
    url="",
    author="Jack Sims",
    author_email="jack.m.sims@protonmail.com",
    license="BSD 2-clause",
    packages=find_packages(),
    install_requires=[
        "argparse",
        "setuptools",
        "wheel",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
    ],
)
