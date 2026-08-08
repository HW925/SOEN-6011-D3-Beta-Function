# Generative AI Use for Deliverable 3

Tool used: OpenAI ChatGPT/Codex. Suggestions were treated as drafts and were
accepted only after source inspection, execution, and independent verification.

## Problem 7

### CASTROFF

- **Constraints:** Preserve the from-scratch numerical restriction; do not
  hide unexpected programming errors or claim universal numerical accuracy.
- **Audience:** SOEN 6011 teaching assistant and instructor.
- **Structure:** Poster checklist organized by style, debugging, versioning,
  UIDP, accessibility, and numerical verification.
- **Tone:** Concise, technical, and evidence-based.
- **Role:** Graduate software-engineering student reviewing a final release.
- **Output format:** Suggested code revisions, verification steps, and short
  poster statements.
- **Focus:** PEP 8, Flake8, Pylint, pdb, Semantic Versioning, accessibility,
  and honest binary64 range behaviour.
- **Function:** Review the implementation and identify claims that require
  executable evidence.

### Example prompt and decision

> Review this from-scratch Beta implementation for PEP 8, Flake8, Pylint, pdb,
> Semantic Versioning, UIDP, accessibility, and honest binary64 range behavior.
> Do not recommend hiding unexpected exceptions or making a universal accuracy
> claim.

The output suggested stable log-beta evaluation, explicit range errors, and
tool-based evidence. These suggestions were revised and accepted after Flake8,
Pylint, pdb, deterministic high-precision verification, and code inspection.
Unverified performance and universal-accuracy claims were rejected.

## Problem 8

### CASTROFF

- **Constraints:** Use PyUnit; cover requirements and known regressions rather
  than increasing the test count without purpose.
- **Audience:** SOEN 6011 teaching assistant and instructor.
- **Structure:** Tests grouped by trusted values, identities, domain errors,
  numerical boundaries, and unexpected failures.
- **Tone:** Direct and verification-oriented.
- **Role:** Graduate software-engineering student designing regression tests.
- **Output format:** Named test cases with expected values or exceptions.
- **Focus:** Unit-argument identities, large asymmetric inputs, NaN/infinity,
  separate x/y errors, subnormal rounding, overflow, and underflow.
- **Function:** Propose missing tests and expose unsupported claims.

### Example prompt and decision

> Propose focused PyUnit regressions for known Beta identities, separate x and
> y validation, NaN and infinity, the subnormal rounding boundary, overflow,
> underflow, and the large-asymmetric defect corrected during D3.

The useful cases were implemented and executed locally. Test names and expected
behaviour were revised to match the documented binary64 contract. Any suggested
case that depended on a mathematical library inside the submitted core was
rejected.
