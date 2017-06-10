# coding: utf-8
from __future__ import unicode_literals
import sys

PY_VERSION = sys.version
PY2 = PY_VERSION < '3'
SYS_ENCODE = sys.stdout.encoding or 'utf-8'
