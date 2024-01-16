import sys

__author__ = "RESLAID"
__version__ = (0, 1, 3)

py_version = sys.version_info
full_py_version = py_version[:3]

if py_version.major == 3:
    if (3, 3, 0) <= full_py_version <= (3, 4, 99):
        from .lib334 import *

    if (3, 5, 0) <= full_py_version <= (3, 6, 99):
        from .lib335 import *

    elif (3, 7, 0) <= full_py_version <= (3, 12, 99):
        from .lib3 import *

    from .escape3 import *
    
elif py_version.major == 2:
    from .lib27 import *
    from .escape2 import *
