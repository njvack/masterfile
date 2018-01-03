# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2017 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

"""
This package contains functions for pretty-printing data — for example,
converting column numbers into Excel-like column identifier strings.
"""

import string


def index_to_column_id(number):
    """
    Takes a zero-based index and converts it to a column identifier string
    such as used in Excel. Examples:
    0 => A
    25 => Z
    26 => AA
    """
    if number < 0 or not isinstance(number, int):
        raise AttributeError("index_to_column_id requires a non-negative int")
    digits = string.ascii_uppercase
    parts = []
    number += 1  # The algorithm works on 1-based input
    while number > 0:
        number, mod = divmod(number - 1, len(digits))
        parts.insert(0, digits[mod])
    return ''.join(parts)