"""Unit tests for the Beta function numerical core and input parser."""

import unittest
from unittest.mock import Mock, patch

from beta_core import (
    InputValidationError,
    NumericRangeError,
    beta_function,
    exponential,
)
from beta_function_gui import BetaCalculatorApp, parse_positive_real


def assert_relative_close(test_case, actual, expected, tolerance=1.0e-10):
    """Assert that the relative error is within tolerance."""
    relative_error = abs(actual - expected) / abs(expected)
    test_case.assertLessEqual(relative_error, tolerance)


class BetaFunctionValueTests(unittest.TestCase):
    """Verify trusted values, identities, symmetry, and regressions."""

    def test_known_value_one_one(self):
        """B(1, 1) equals one."""
        assert_relative_close(self, beta_function(1.0, 1.0), 1.0)

    def test_known_value_two_three(self):
        """B(2, 3) equals one twelfth."""
        assert_relative_close(self, beta_function(2.0, 3.0), 1.0 / 12.0)

    def test_half_half_equals_pi(self):
        """B(0.5, 0.5) equals pi."""
        assert_relative_close(
            self,
            beta_function(0.5, 0.5),
            3.141592653589793,
        )

    def test_symmetry(self):
        """Swapping x and y does not change the result."""
        assert_relative_close(
            self,
            beta_function(2.5, 7.0),
            beta_function(7.0, 2.5),
        )

    def test_identity_one_y(self):
        """B(1, y) equals 1/y."""
        assert_relative_close(self, beta_function(1.0, 7.5), 1.0 / 7.5)

    def test_identity_x_one(self):
        """B(x, 1) equals 1/x."""
        assert_relative_close(self, beta_function(4.25, 1.0), 1.0 / 4.25)

    def test_regression_large_asymmetric_identity(self):
        """The D3 large-input cancellation defect remains corrected."""
        assert_relative_close(
            self,
            beta_function(1.0e100, 1.0),
            1.0e-100,
        )

    def test_near_maximum_asymmetric_identity(self):
        """A near-maximum finite x does not trigger log-gamma cancellation."""
        assert_relative_close(
            self,
            beta_function(1.0e308, 1.0),
            1.0e-308,
        )


class NumericalBoundaryTests(unittest.TestCase):
    """Verify representable and unrepresentable binary64 boundaries."""

    def test_roundable_subnormal_exponential(self):
        """A finite result near the subnormal boundary is not rejected."""
        self.assertEqual(exponential(-745.0), 5.0e-324)

    def test_unroundable_exponential_is_rejected(self):
        """An exponential below the rounding boundary reports underflow."""
        with self.assertRaisesRegex(NumericRangeError, "minimum nonzero"):
            exponential(-746.0)


class InterfaceAndInputTests(unittest.TestCase):
    """Verify parsing, domain errors, range errors, and error propagation."""

    def test_unexpected_arithmetic_error_is_not_hidden(self):
        """Unexpected arithmetic failures remain visible for diagnosis."""
        application = BetaCalculatorApp.__new__(BetaCalculatorApp)
        application.x_text = Mock()
        application.y_text = Mock()
        application.x_text.get.return_value = "1"
        application.y_text.get.return_value = "1"

        with patch(
            "beta_function_gui.beta_function",
            side_effect=OverflowError("unexpected arithmetic failure"),
        ):
            with self.assertRaisesRegex(OverflowError, "unexpected"):
                application.calculate()

    def test_scientific_notation_parser(self):
        """The GUI parser accepts scientific notation."""
        self.assertEqual(parse_positive_real("1e-3", "x"), 0.001)

    def test_nonnumeric_input_is_rejected(self):
        """The GUI parser reports a useful nonnumeric-input error."""
        with self.assertRaisesRegex(InputValidationError, "real number"):
            parse_positive_real("abc", "x")

    def test_missing_input_is_rejected(self):
        """The GUI parser identifies a missing field before calculation."""
        with self.assertRaisesRegex(InputValidationError, "x is required"):
            parse_positive_real("   ", "x")

    def test_zero_is_rejected(self):
        """Zero is rejected because it is outside the Beta domain."""
        with self.assertRaisesRegex(InputValidationError, "greater than zero"):
            beta_function(0.0, 2.0)

    def test_negative_x_is_rejected(self):
        """A negative x is rejected with a field-specific error."""
        with self.assertRaisesRegex(InputValidationError, "x must"):
            beta_function(-1.0, 2.0)

    def test_zero_y_is_rejected(self):
        """A zero y is rejected with a field-specific error."""
        with self.assertRaisesRegex(InputValidationError, "y must"):
            beta_function(2.0, 0.0)

    def test_negative_y_is_rejected(self):
        """A negative y is rejected with a field-specific error."""
        with self.assertRaisesRegex(InputValidationError, "y must"):
            beta_function(2.0, -1.0)

    def test_nonfinite_input_is_rejected(self):
        """NaN and positive or negative infinity are rejected."""
        cases = (
            (float("nan"), 2.0),
            (float("inf"), 2.0),
            (float("-inf"), 2.0),
            (2.0, float("inf")),
        )
        for x_value, y_value in cases:
            with self.subTest(x=x_value, y=y_value):
                with self.assertRaisesRegex(InputValidationError, "finite"):
                    beta_function(x_value, y_value)

    def test_overflow_is_reported(self):
        """A result above the largest binary64 value reports a range error."""
        with self.assertRaisesRegex(NumericRangeError, "too large"):
            beta_function(1.0e-309, 1.0e-309)

    def test_underflow_is_reported(self):
        """An unrepresentable positive result is not returned as zero."""
        with self.assertRaisesRegex(NumericRangeError, "minimum nonzero"):
            beta_function(1000.0, 1000.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
