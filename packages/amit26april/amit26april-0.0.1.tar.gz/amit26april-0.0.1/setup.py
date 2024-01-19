from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'India Papa Love  '
LONG_DESCRIPTION = '''
    * This project helps the begginers to generate ai models with 1 line of code.
    * It is also useful for experts as it will automate repetative task and experts can focus upon main model
    * It works right now only for image classification but there may be updates in future
'''

# Setting up
setup(
    name="amit26april",
    version=VERSION,
    author="Ayush Agrawal",
    author_email="aagrawal963@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['tensorflow','keras','scikit-learn','tqdm','seaborn','Pillow'],
    keywords=['experts', 'begginers', 'deep learning', 'ai ultimate', 'ayush agrawal','automate steps of deep learning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)