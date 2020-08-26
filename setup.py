"""setup.py file."""
from setuptools import setup, find_packages

with open("requirements.txt", "r") as fs:
    reqs = [r for r in fs.read().splitlines() if (len(r) > 0 and not r.startswith("#"))]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="git-acp-ansible",
    version='1.0.9',
    packages=find_packages(exclude=("test*", "venv")),
    author="Federico Olivieri",
    author_email="lvrfrc87@gmail.com",
    description="Ansible module for git add/commit/push operations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    url="https://github.com/lvrfrc87/git-acp-ansible",
    install_requires=reqs,
)
