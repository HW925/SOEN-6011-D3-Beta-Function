"""External high-precision verification for the submitted numerical core.

This script is evidence only. The implementation in beta_core.py does not
import mpmath or any other mathematical library.
"""

import math
import random
import sys

import mpmath

from beta_core import NumericRangeError, beta_function, exponential


CASE_COUNT = 500
INPUT_EXPONENT_LIMIT = 12.0
RELATIVE_TOLERANCE = 1.0e-10
RANDOM_SEED = 6011


def relative_error(actual, expected):
    """Return relative error using a high-precision expected value."""
    return abs(mpmath.mpf(actual) - expected) / abs(expected)


def verify_random_cases():
    """Verify deterministic log-uniform cases with normal reference outputs."""
    generator = random.Random(RANDOM_SEED)
    checked = 0
    range_limited = 0
    failures = 0
    maximum_error = mpmath.mpf("0")
    worst_case = None

    for _index in range(CASE_COUNT):
        x_value = 10.0 ** generator.uniform(
            -INPUT_EXPONENT_LIMIT,
            INPUT_EXPONENT_LIMIT,
        )
        y_value = 10.0 ** generator.uniform(
            -INPUT_EXPONENT_LIMIT,
            INPUT_EXPONENT_LIMIT,
        )
        expected = mpmath.beta(
            mpmath.mpf(str(x_value)),
            mpmath.mpf(str(y_value)),
        )
        expected_float = float(expected)

        if (
            expected_float == 0.0
            or not math.isfinite(expected_float)
            or abs(expected_float) < sys.float_info.min
        ):
            range_limited += 1
            continue

        try:
            actual = beta_function(x_value, y_value)
        except NumericRangeError:
            failures += 1
            continue

        error = relative_error(actual, expected)
        checked += 1
        if error > maximum_error:
            maximum_error = error
            worst_case = (x_value, y_value)
        if error > RELATIVE_TOLERANCE:
            failures += 1

    return checked, range_limited, failures, maximum_error, worst_case


def main():
    """Print reproducible accuracy and boundary evidence."""
    mpmath.mp.dps = 100
    results = verify_random_cases()
    checked, range_limited, failures, maximum_error, worst_case = results
    large_actual = beta_function(1.0e100, 1.0)
    large_error = abs(large_actual - 1.0e-100) / 1.0e-100

    print("External verification only - mpmath, 100 decimal digits")
    print(f"Seed: {RANDOM_SEED}; generated cases: {CASE_COUNT}")
    print("Inputs: log-uniform from 1e-12 through 1e12")
    print(f"Normal representable results checked: {checked}")
    print(f"Range-limited reference results excluded: {range_limited}")
    print(f"Failures above 1e-10 relative error: {failures}")
    print(f"Maximum relative error: {float(maximum_error):.3e}")
    print(f"Worst normal-result input: {worst_case}")
    print(f"Large regression B(1e100, 1) relative error: {large_error:.3e}")
    print(f"Roundable boundary exp(-745): {exponential(-745.0):.17g}")


if __name__ == "__main__":
    main()
