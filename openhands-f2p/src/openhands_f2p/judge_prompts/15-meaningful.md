---
name: meaningful
job: The first label, and the only absolute one (user, 2026-10-04): is the generated test a
  meaningful test of this fix at all -- yes or no, no questions. Every judged test already
  fails before the fix and passes after; this asks whether that flip means anything. A
  regex for `inspect.getsource` caught 2 of 1,373 such tests and nothing else of the
  kind, while the judge rated about one in eight "tangential" or "different". Decided
  before the comparison, on the generated test alone; the developer's test is not the
  yardstick here.
---
**First, before comparing anything: is the generated test meaningful?** Answer `yes` or
`no`. This is the only judgement that is not a comparison with the developer's test -- read
the generated test on its own, against the bug report and the fix.

Every test you are shown already fails on the code before the fix and passes after it.
That flip is necessary, and it can be produced by a test that checks nothing a maintainer
would care about. The question is whether *this* flip demonstrates the behaviour the fix
establishes.

It is **meaningful** (`yes`) when it calls the project's code with an input that goes
through the changed behaviour and asserts on what that code observably does -- a return
value, a raised exception, output, a state change -- so that it fails before the fix
*because of the bug the report describes*, and would keep passing for a different correct
fix of the same bug. It may be narrow, clumsy, or cover only part of the fix and still be
meaningful: narrowness and style are judged below, not here.

It is **not meaningful** (`no`) when the flip comes from something other than the bug's
behaviour, for example when the test:

- reads the project's source code as text and asserts that the fix's wording is there;
- only checks that a name, attribute, method or parameter exists (`hasattr`, an import,
  `callable`, a signature) where the fix is about what that code does;
- checks only a type or a container shape (`isinstance(result, list)`) and nothing about
  the values the fix changes;
- asserts on a mock, a stub or its own copy of the fixed logic rather than on the
  project's code;
- passes or fails for a reason the fix does not touch -- a setup that happens to break on
  the old code, an assertion that is true or false regardless of the bug;
- is tied to this exact implementation (a private value, an internal call order, the
  text of a message the bug is not about) so that a different correct fix would fail it.

When in doubt, ask: if a maintainer read only this test and its failure on the old code,
would they learn that the reported bug existed? `yes` if they would, `no` if they would
not. Give one sentence saying what the test's flip actually rests on.
