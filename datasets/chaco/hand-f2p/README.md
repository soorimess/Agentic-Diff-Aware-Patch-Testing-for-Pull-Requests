# Hand-written fail-to-pass tests (ChaCo ablation, 2026-10-12)

The question: for the ChaCo PRs where our agent ended NO, is a fail-to-pass test possible
at all? Each file here is a test written by hand, with no model, and judged by the
harness's own `verify()`, the same call that judges an agent's test (`agent.py`'s recheck
path). It runs in the PR's image, on base and then with the PR's `patch` applied.

    cd openhands-f2p
    uv run python ../datasets/chaco/hand-f2p/hand_verify.py <instance_id> <test path in repo> <file> [-v]

| PR | agent (base config) | hand test | verify | changed-line coverage | what the test checks |
|---|---|---|---|---|---|
| pandas-59928 | NO | `pandas/tests/indexes/test_f2p_hand.py` | YES (2 tests) | 60% | `trim_front` trims common leading tabs, not only spaces |
| pandas-60196 | NO | `pandas/tests/frame/test_f2p_hand.py` | YES (1) | 75% | with jinja2 missing, `inspect.getmembers(df)` works (`.style` raises AttributeError, not ImportError) |
| Qiskit-14353 | NO | `test/python/transpiler/test_f2p_hand.py` | YES (16, +4 pass on both sides) | 92% | with no coupling map, the layout plugins add no layout pass |
| Qiskit-13251 | NO | `test/python/qpy/test_f2p_hand.py` | YES (1, +1 pass on both sides) | 52% | a QPY symengine payload from symengine 0.9 raises `QpyError` |
| Qiskit-13343 | NO | `test/python/qasm3/test_f2p_hand.py` | YES (4) | 73% | OpenQASM 3 AST nodes are slotted (no `__dict__`) |
| pandas-59141 | NO | `pandas/tests/reshape/concat/test_f2p_hand.py` | YES (2, +1 pass on both sides) | 53% | `concat` hands its inputs to `__finalize__` as `objs=` |
| pandas-60295 | NO | `pandas/tests/frame/methods/test_f2p_hand.py` | YES (2) | 100% | regex `replace` and `fillna` put a number into a string column |
| SciPy-21713 | NO | `scipy/signal/tests/test_f2p_hand.py` | YES (1) | 1% (the patch is a large array-API refactor) | `hilbert2` accepts nested lists |
| SciPy-22549 | NO | `scipy/optimize/tests/test_f2p_hand.py` | YES (1) | 40% | `VectorFunction` takes `workers=` for finite differences |

Notes:

- **Qiskit-13251, a bug in the merged patch.** `load_symengine_payload` compares
  `payload[2]` (an int) with `"0"` (a string), so every version mismatch raises "symengine
  >= 1.0", and the 0.11 <-> 0.13 workaround the PR is about never runs. The hand test checks
  what does work: an unsupported payload is refused by QPY with `QpyError`.
- **Qiskit-13343** is a speed-up. Its only observable change is `__slots__`, so the test
  checks an implementation property, not a result.
- pandas-59141, 60295 and SciPy 21713, 22549 already had developer tests that flip; these
  files restate them as one new test file, which is the form our agent writes.
- The 5 PRs agreed to be untestable (pandas 60541, 59626; SciPy 20382, 22616, 21485) are
  not here.
