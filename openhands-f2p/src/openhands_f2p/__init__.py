"""Lazy `main`, so `python -m openhands_f2p.agent` does not re-import a loaded module.

Importing agent here eagerly made runpy warn that `openhands_f2p.agent` was already in
sys.modules before it executed it -- harmless, but it is printed on every single run.
"""


def __getattr__(name: str):
    if name == "main":
        from openhands_f2p.agent import main
        return main
    raise AttributeError(name)


__all__ = ["main"]
