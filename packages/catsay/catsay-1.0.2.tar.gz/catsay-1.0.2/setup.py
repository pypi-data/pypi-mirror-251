from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

__version__ = "1.0.2"
REPO_NAME = "catsay"
PKG_NAME= "catsay"
AUTHOR_USER_NAME = "tikendraw"
AUTHOR_EMAIL = "tikendraksahu1029@gmail.com"

setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for no one.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    }
)
