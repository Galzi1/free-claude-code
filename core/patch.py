import sys

def apply_pydantic_314_patch():
    """Monkeypatch Pydantic to fix compatibility with Python 3.14.
    
    Starting in Python 3.14, typing._eval_type no longer accepts the 
    'prefer_fwd_module' argument which Pydantic (<=2.13) tries to pass.
    """
    if sys.version_info >= (3, 14):
        try:
            import typing
            import pydantic._internal._typing_extra as typing_extra

            _original_eval_type = typing_extra._eval_type

            def _patched_eval_type(value, globalns=None, localns=None, type_params=None):
                if sys.version_info >= (3, 14):
                    # In Python 3.14, typing._eval_type no longer accepts prefer_fwd_module
                    return typing._eval_type(
                        value,
                        globalns,
                        localns,
                        type_params=type_params,
                    )
                return _original_eval_type(value, globalns, localns, type_params)

            typing_extra._eval_type = _patched_eval_type
        except (ImportError, AttributeError):
            pass

if __name__ == "__main__":
    apply_pydantic_314_patch()
