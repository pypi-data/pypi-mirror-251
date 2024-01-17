import inspect
from typing import Optional

import passlib.pwd


def isnull(s: Optional[str]) -> bool:
    return s is None or not s or s.isspace()


def funcname():
    return inspect.stack()[1][3]
