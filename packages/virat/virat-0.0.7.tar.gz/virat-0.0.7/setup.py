from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

__version__ = "0.0.7"
REPO_NAME = "mangodbpackage"
PKG_NAME = "virat"
AUTHOR_USER_NAME = "vinay"
AUTHOR_EMAIL = "vinayakavirat008@gmail.com"

setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for connecting with the database.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Add this line
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
