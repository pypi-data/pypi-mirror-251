"""

"""


def _auto_version():
    try:
        from pyimportcyclefinder._version import __version__
        return __version__
    except ModuleNotFoundError as e:
        pass
    try:
        from pyimportcyclefinder._get_version import get_version_for_pyproject_toml
        return get_version_for_pyproject_toml()
    except:
        return 'unknown [could not determine automatically, do you not have git?]'


__version__ = _auto_version()
__all__ = ["__version__"]