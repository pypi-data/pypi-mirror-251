from __future__ import annotations

from pathlib import Path

import matplotlib
from matplotlib.font_manager import fontManager

__version__ = "1.0.0"

FONTSDIR = "fonts"
FILE = "NotoSansCJKjp-Regular.otf"
FAMILY = "Noto Sans CJK JP"

fontManager.addfont(str((Path(__file__).parent / FONTSDIR / FILE).resolve()))
matplotlib.rc("font", family=FAMILY)
