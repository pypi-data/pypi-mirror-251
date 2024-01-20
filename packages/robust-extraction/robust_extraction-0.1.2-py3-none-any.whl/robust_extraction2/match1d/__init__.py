"""Matching 1d templates (rows/cols)
- See "scale- and translation-invariant Linear Assignment Problem (LAP)" in the docs
"""
from .invariant_ import alignments, invariant_match, hmatch, vmatch
from .best import best_match
from .invariant2 import invariant
from .contig import contiguous
from . import contig