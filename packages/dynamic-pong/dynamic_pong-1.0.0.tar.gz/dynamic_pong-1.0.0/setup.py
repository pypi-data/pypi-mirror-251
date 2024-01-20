from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Dynamic Pong: A Python-based modern twist on classic Pong'
LONG_DESCRIPTION = 'Dynamic Pong is an enhanced version of the classic Pong game, crafted in Python using Pygame. It features dynamic difficulty adjustments, customizable game elements, realistic collision physics, and real-time score tracking. This project exemplifies advanced Python programming, object-oriented design, and efficient use of the Pygame library.'

# Setting up
setup(
    name="dynamic_pong",
    version=VERSION,
    author="Adamya Singh",
    author_email="<7adamyasingh@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'pong', 'game', 'dynamic', 'resume project', 'pygame'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={"console_scripts": ["dynamic_pong = dynamic_pong.__main__:main"]}
)