# -*- coding: utf-8 -*-

""" DisCoPy: the Python toolkit for computing with string diagrams. """

import warnings
from importlib.metadata import version, PackageNotFoundError

from discopy import (
    cat,
    monoidal,
    braided,
    symmetric,
    markov,
    traced,
    closed,
    rigid,
    pivotal,
    ribbon,
    compact,
    frobenius,
    hypergraph,
    interaction,
    feedback,
    stream,
    python,
    matrix,
    tensor,
    quantum,
    grammar,
    drawing,
    utils,
    config,
    messages,
)

__version__ = None
__version_info__ = None

# 1. Try to get version from installed package metadata
try:
    __version__ = version("discopy")
except PackageNotFoundError:
    pass

# 2. Try to get version from discopy.version (setuptools_scm generated)
if __version__ is None:
    try:
        from discopy.version import version as __version__
    except ImportError:
        pass

# 3. Fallback to default
if __version__ is None:
    warnings.warn("discopy.version not found. Defaulting to 0.0.0")
    __version__ = "0.0.0"

# Now handle __version_info__
try:
    from discopy.version import version_tuple as __version_info__
except ImportError:
    pass

if __version_info__ is None:
    try:
        # Best effort parsing of __version__
        # Split by '.' and take integer parts
        __version_info__ = tuple(
            int(x) for x in __version__.split('.') if x.isdigit())
    except Exception:
        pass

if not __version_info__:
    __version_info__ = (0, 0, 0)
