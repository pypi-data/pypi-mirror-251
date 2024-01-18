from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Print standard output in colorful gradients.'
LONG_DESCRIPTION = 'A Python 3 module that allows you to print your command line output in pretty colors.  Print the rainbow!'

# Setting up
setup(
    name="rainbowprint-TechnoHwizrdry",
    version=VERSION,
    author="Techno-Hwizrdry (Alexan Mardigian)",
    author_email="<alexan@expresspolygon.com>",
    url='https://github.com/Techno-Hwizrdry/rainbowprint',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=['colored==1.4.3', 'colour==0.1.5'],
    keywords=['python', 'colors', 'gradient', 'terminal', 'output'],
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ]
)
