# coding: utf-8
# from __future__ import unicode_literals
import codecs
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


NAME = "wechat_sender"

PACKAGES = ["wechat_sender", ]

DESCRIPTION = "将程序运行结果及报警信息通过微信发送给你自己"

LONG_DESCRIPTION = read("README.rst")

KEYWORDS = ["Wechat", "微信", "监控"]

AUTHOR = "RaPoSpectre"

AUTHOR_EMAIL = "rapospectre@gmail.com"

URL = "https://github.com/bluedazzle/wechat_sender"

VERSION = "0.1.0"

LICENSE = "BSD"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat',
        'Topic :: Utilities',
    ],
    install_requires=[
        'tornado',
        'psutil',
    ],

    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
