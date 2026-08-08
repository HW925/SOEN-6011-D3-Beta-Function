# Beta Function Calculator - SOEN 6011 D3

Version `1.0.0` is the Deliverable 3 release of the F6 Beta function
calculator. It keeps the numerical core independent of mathematical libraries,
adds accessibility-oriented keyboard controls, and provides quality-tool,
debugger, and unit-test evidence.

The release contract is maintained in [`REQUIREMENTS.md`](REQUIREMENTS.md),
and the release history is recorded in [`CHANGELOG.md`](CHANGELOG.md).

Public repository:
[https://github.com/HW925/SOEN-6011-D3-Beta-Function](https://github.com/HW925/SOEN-6011-D3-Beta-Function)

## Run

```text
python3 beta_function_gui.py
```

The application accepts finite positive real values in decimal or scientific
notation. `Enter` calculates, `Esc` clears, and `Alt+X` or `Alt+Y` moves focus
to the corresponding input.

## Numerical design

`beta_core.py` implements `natural_log`, `natural_log_one_plus`, `exponential`,
`log_gamma`, `log_beta`, and `beta_function` with arithmetic and iteration. It
imports no library function. The dedicated `log_beta` formula avoids both
directly multiplying Gamma values and subtracting nearly equal, very large
log-gamma values. This fixes extreme asymmetric inputs such as
`B(1e100, 1) = 1e-100`.

The exponential implementation preserves roundable subnormal values. If a
mathematically positive result cannot round to a nonzero Python float, the
program reports a numeric-range error instead of returning a misleading zero.
The GUI handles only the expected input and numeric-range exceptions;
unexpected arithmetic errors remain visible for diagnosis.

## Verified numerical contract

- The parser accepts decimal or scientific-notation text that converts to a
  finite positive Python float.
- For accepted inputs, a calculation returns a nonzero finite binary64 result
  when that result is representable. Otherwise, it raises an explicit
  numeric-range error for overflow or underflow.
- Twelve displayed significant digits are an output format, not a universal
  claim of twelve-digit numerical accuracy.
- The published accuracy evidence uses 500 deterministic cases from `1e-12`
  through `1e12`. For the 414 normal representable reference results, the
  maximum relative error is `1.223e-11`, below the `1e-10` verification
  tolerance. Subnormal results are subject to binary64 spacing and are not
  covered by that relative-error claim.

## Quality checks

Create a local environment and install the pinned tools:

```text
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/flake8 beta_core.py beta_function_gui.py test_beta_core.py debug_beta.py verify_accuracy.py
.venv/bin/pylint beta_core.py beta_function_gui.py test_beta_core.py debug_beta.py verify_accuracy.py
```

The final release has no Flake8 findings and receives a Pylint score of
`10.00/10`. During the final test expansion, Pylint reported
`too-many-public-methods` for one oversized test class. The tests were divided
into value, numerical-boundary, and interface/input classes, restoring focused
test responsibilities and the `10.00/10` result without a global suppression.

## Debugger

```text
python3 -m pdb debug_beta.py
```

The reproducible commands are listed in `debug_session.txt`. The poster uses a
snapshot of a breakpoint inside `beta_function` while evaluating `B(2, 3)`.

## Unit tests

```text
python3 -m unittest -v
```

The twenty-one PyUnit tests cover known values, both unit-argument identities,
symmetry, a large-input regression, the subnormal boundary, scientific
notation, separate x/y domain failures, NaN and infinity, overflow and
underflow reporting, and propagation of unexpected arithmetic failures.

## External accuracy verification

```text
.venv/bin/python verify_accuracy.py
```

`mpmath` is used only by this verification script at 100-decimal-digit
precision. It is not imported by the submitted numerical core.

## Semantic Versioning

The current release is `1.0.0`: the first stable D3 interface and numerical
contract. It is marked by the repository tag `v1.0.0`. Future
backward-compatible features increment the minor number, bug fixes increment
the patch number, and incompatible interface or contract changes increment the
major number.

## Reference material

- [NIST DLMF, Section 5.12: Beta Function](https://dlmf.nist.gov/5.12)
- [mpmath 1.3.0 documentation](https://mpmath.org/doc/current/)
- [Nielsen Norman Group usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [Semantic Versioning 2.0.0](https://semver.org/)

## Files

- `beta_core.py`: from-scratch numerical implementation
- `beta_function_gui.py`: Tkinter GUI
- `test_beta_core.py`: PyUnit tests
- `REQUIREMENTS.md`: supported numerical and interface contract
- `CHANGELOG.md`: Semantic Versioning history
- `GAI_USAGE.md`: full CASTROFF records and verification decisions
- `verify_accuracy.py`: external high-precision verification
- `debug_beta.py` and `debug_session.txt`: debugger demonstration
- `SOEN_6011_D3_Poster.tex`: poster source
- `output/pdf/SOEN_6011_D3_Poster.pdf`: final poster
