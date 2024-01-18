from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.9.63'
DESCRIPTION = 'test'
LONG_DESCRIPTION = 'k zeg toch is een test ouleh'

# Setting up
setup(
    name="rda63",
    version=VERSION,
    author="NeuralNine (Florian Dedov)",
    author_email="<poep@dhine.es>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
