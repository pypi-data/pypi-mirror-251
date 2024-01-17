from setuptools import setup

__project__ = "AsciiEngine"
__version__ = "0.0.4"
__description__ = "A python module for making games that run in the terminal."
__packages__ = ["AsciiEngine"]
__author__ = "RetroGamer5491"
__author_email__ = "caarfken@proton.me"
__requires__ = ["pynput"]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    requires = __requires__,
    long_description = open("./README.md").read(),
    long_description_content_type = "text/markdown"
)