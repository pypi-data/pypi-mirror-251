from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'A libirary to automate developing keras models'
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# Setting up
setup(
    name="amit26april",
    version=VERSION,
    author="Ayush Agrawal",
    author_email="aagrawal963@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['tensorflow','keras','scikit-learn','tqdm','seaborn','Pillow'],
    keywords=['experts', 'begginers', 'deep learning', 'ai ultimate', 'ayush agrawal','automate steps of deep learning','manupliate image dataset','ai less code','ai work companion','basic model develoment','expert kit','ai','tensorflow','keras'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)