import logging
import pickle
import re
import zlib
from contextlib import closing
from functools import partial
from multiprocessing.pool import Pool
from typing import Callable, Dict, Iterator, List, NamedTuple, Optional, Tuple
from uuid import uuid1

import cython
import lmdb
import mwparserfromhell


def hello_cython():
    print("Hello from Cython!")
