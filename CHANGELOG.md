# Version History

This project follows Semantic Versioning 2.0.0.

## 1.0.0 - 2026-08-07

First stable Deliverable 3 release.

- Defines a stable GUI and numerical contract for finite positive binary64
  inputs.
- Corrects cancellation for extreme asymmetric inputs through stable
  log-beta evaluation.
- Preserves roundable subnormal results and reports explicit overflow or
  underflow range errors.
- Adds accessible keyboard interaction, visible status text, static-analysis
  evidence, debugger evidence, deterministic verification, and PyUnit tests.

The repository tag for this release is `v1.0.0`. Later compatible features use
the minor version, compatible fixes use the patch version, and incompatible
contract changes use the major version.
