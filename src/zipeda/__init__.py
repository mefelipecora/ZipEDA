from .zipeda import perform_eda
__all__ = ["perform_eda"]

# Version sourced from installed metadata
try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("zipeda")
except PackageNotFoundError:
    __version__ = "0.0.0"
