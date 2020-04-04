"""setup.py file."""
from setuptools import setup, find_packages

with open("requirements.txt", "r") as fs:
    reqs = [r for r in fs.read().splitlines() if (len(r) > 0 and not r.startswith("#"))]

setup(
    name="git-acp-ansible",
    version='1.0.0',
    packages=find_packages(exclude=("test*"),
    author="Federico Olivieri",
    author_email="lvrfrc87@gmail.com",
    description="Ansible module for git add/commit/push operations.",
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
    include_package_data=True,
    install_requires=reqs,
)