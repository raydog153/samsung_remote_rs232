# -*- coding: utf-8 -*-

import setuptools  # NOQA

__title__ = "samsung_remote_rs232"
__version__ = "0.0.0a"
__url__ = "https://github.com/raydog153/samsung_remote_rs232"
__author__ = "Ray Boutotte"
__author_email__ = "ray.boutotte@gmail.com"
__license__ = "MIT"

setuptools.setup(
    name=__title__,
    version=__version__,
    description=__doc__,
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    long_description=open("README.md").read(),
    entry_points={
        "console_scripts": ["samsung_remote_rs232=samsung_remote_rs232.__main__:main"]
    },
    packages=[
        "samsung_remote_rs232"
    ],
    install_requires=[
        'serial'
    ],
    extras_require={
    },
    classifiers=[
        "Development Status :: Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Home Automation",
    ],
    zip_safe=False
)
