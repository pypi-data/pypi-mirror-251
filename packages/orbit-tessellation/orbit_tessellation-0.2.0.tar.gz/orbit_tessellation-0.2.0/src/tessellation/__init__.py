from importlib.metadata import version as _version

__version__ = _version("orbit-tessellation")

from .constructor import Tessellation
