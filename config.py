import os
import sys


def set_path():
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    grandparent = os.path.dirname(parent)
    sys.path.append(parent)
    sys.path.append(grandparent)
