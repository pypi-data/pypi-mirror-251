from os import path
from zolfa.nd2reader.reader import ND2Reader
from zolfa.nd2reader.legacy import Nd2

import importlib.metadata as importlib_metadata

try:
    __version__ = importlib_metadata.version(__name__)
except:
    print('Unable to read version number')
