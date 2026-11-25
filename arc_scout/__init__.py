"""ARC Scout: deterministic, read-only repository assessment (M1 step 1: local inventory).

The engine is ``arc_scout.inventory``; the command line is ``python -m arc_scout``.
"""

import sys

if sys.version_info < (3, 12):  # pragma: no cover
    raise SystemExit("arc_scout requires Python 3.12 or newer")

__version__ = "0.1.0"
