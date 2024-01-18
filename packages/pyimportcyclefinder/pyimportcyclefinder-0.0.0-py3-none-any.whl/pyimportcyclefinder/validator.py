import functools


def _dummy_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper


def _import_and_assemble_validator_from_pydantic():
    import packaging.version
    import pydantic
    from pydantic import validate_call, ConfigDict
    pyd_ver = packaging.version.parse(pydantic.__version__)
    modern_pyd_version_min = packaging.version.parse("2.0a1")
    old_pyd_version_min = packaging.version.parse("1.10")
    if pyd_ver > modern_pyd_version_min:
        local_configured_validate_call = functools.partial(
            validate_call,
            config=ConfigDict(
                extra='forbid',
                arbitrary_types_allowed=True,
                strict=True
            ),
            validate_return=True
        )
    elif pyd_ver >= old_pyd_version_min:
        local_configured_validate_call = functools.partial(
            validate_call, config={
                'extra': 'forbid',
                'arbitrary_types_allowed': True
            }
        )
    else:
        raise ModuleNotFoundError("pydantic version insufficient")
    return local_configured_validate_call

try:
    configured_validate_call = _import_and_assemble_validator_from_pydantic()
except ModuleNotFoundError as e:
    configured_validate_call = _dummy_decorator


__all__ = ['configured_validate_call']
