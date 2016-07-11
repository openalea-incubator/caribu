""" paths to module data file
"""
from path import path


def data_path(filename):
    d = path(__file__).dirname()
    fn = 'data/' + filename
    return d / fn
