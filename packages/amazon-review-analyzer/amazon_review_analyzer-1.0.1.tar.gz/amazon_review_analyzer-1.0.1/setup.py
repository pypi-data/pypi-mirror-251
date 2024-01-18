from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.1'
DESCRIPTION = 'Amazon Product Reviews Analyzer'
LONG_DESCRIPTION = 'A package that analyzes the sentiment of Amazon reviews and gives you a idea wheater you can buy the product or not.'

# Setting up
setup(
    name="amazon_review_analyzer",
    version=VERSION,
    author="Krishna Chaitanya",
    author_email="<chaitu.gorle@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'amazon', 'review', 'analyzer', 'sentiment', 'analysis', 'amazon review analyzer'],
)