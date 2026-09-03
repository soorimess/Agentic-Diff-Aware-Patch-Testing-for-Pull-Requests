#!/usr/bin/env python
"""Shim so the agent runs from the repository root as well as via `uv run`.

    openhands-f2p/.venv/bin/python main.py 3
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "openhands-f2p" / "src"))

from openhands_f2p.agent import main

if __name__ == "__main__":
    sys.exit(main())
