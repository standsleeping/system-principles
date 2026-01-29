from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("system-principles")
except PackageNotFoundError:
    __version__ = "unknown"
