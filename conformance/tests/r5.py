"""R5 — SMFPS conformance test. See draft-divolt-smfps-00 section 4.5."""
from __future__ import annotations


def run(target: str, credentials: dict, verbose: bool = False) -> tuple[bool, str]:
    try:
        from .adapters import ADAPTERS
    except ImportError:
        return False, "No adapters module. See conformance/tests/adapters.py.template."
    # Dispatch to the adapter method for R5 (provider-specific implementation).
    fn = getattr(ADAPTERS, "test_r5", None)
    if fn is None:
        return False, "Adapter does not implement test_r5."
    return fn(target, credentials, verbose=verbose)
