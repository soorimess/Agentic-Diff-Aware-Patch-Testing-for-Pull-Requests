# openhands-f2p

An OpenHands agent that writes fail-to-pass tests for SWE-bench Verified pull requests,
inside a per-instance container with no network.

The agent is given the bug report and the diff, and has to produce one test file that
**fails on the code before the fix and passes after it**. The harness runs both states
itself and decides; the agent never sees the maintainer's own test.

    uv run python -m openhands_f2p.agent 1          # one instance
    uv run python -m openhands_f2p.agent all --parallel 10

Every component the agent is given can be withheld with a flag, so two arms differ by
exactly one thing. `--help` lists them, and the reasoning behind each is in
[docs/decisions.md](../docs/decisions.md).

| where | what |
|---|---|
| `src/openhands_f2p/` | the harness -- sandbox, tools, verdict, metrics |
| `src/openhands_f2p/prompts/` | the agent's prompt, one file per instruction |
| `../docs/system-design.md` | architecture, generated in part from the code |
| `../docs/decisions.md` | why it is built this way, with the measurements |
| `../docs/experiments.md` | what to measure next, with costs |

Requires Python 3.12 and a working Docker daemon. Credentials go in `../.env`; see
`../.env.example`.
