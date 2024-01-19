from setuptools import setup, find_packages

setup(
    name="list-to-tabs",
    version='1.1.0',
    description="A python package for converting newline files into konsole-tabs",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="",
    author="Jack Sims",
    author_email="jack.m.sims@protonmail.com",
    license="GPL",
    packages=find_packages(),
    install_requires=[
        "argparse",
        "setuptools",
        "wheel",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={
        'console_scripts': ['list_to_tabs=list_to_tabs.main:main'],
    },
)
print(find_packages())
