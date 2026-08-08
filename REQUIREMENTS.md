# Deliverable 3 Requirements

These requirements define the supported contract for version `1.0.0`.

- **D3-FR-01:** The system shall accept decimal or scientific-notation text
  that converts to finite positive binary64 values for `x` and `y`.
- **D3-FR-02:** For accepted inputs, the system shall return a nonzero finite
  binary64 approximation of `B(x, y)` when the result is representable.
- **D3-FR-03:** The system shall report a specific numeric-range error when the
  positive mathematical result overflows or cannot round to a nonzero binary64
  value.
- **D3-FR-04:** The system shall identify the affected field when `x` or `y` is
  missing, nonnumeric, nonfinite, zero, or negative, and shall remain available
  for a corrected calculation.
- **D3-CR-01:** The numerical core shall implement its subordinate numerical
  operations using arithmetic and iteration without importing mathematical
  library functions.
- **D3-QR-01:** For the deterministic verification set documented in
  `verify_accuracy.py`, normal representable results shall have relative error
  at most `1e-10` against the 100-decimal-digit external oracle.
- **D3-QR-02:** The GUI shall display results using twelve significant digits;
  this is a formatting rule and not a universal accuracy guarantee.
- **D3-QR-03:** Expected input and numeric-range errors shall receive specific
  user-facing messages; unexpected programming errors shall remain visible for
  diagnosis.

Subnormal results follow binary64 spacing and are tested at the representable
and unrepresentable rounding boundary rather than through a universal relative
error claim.
