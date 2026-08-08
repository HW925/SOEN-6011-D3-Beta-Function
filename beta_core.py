"""From-scratch numerical core for the Beta function.

Version 1.0.0 implements logarithm, exponential, and log-gamma using only
arithmetic and iteration. The numerical core imports no library functions.
"""

__version__ = "1.0.0"

LN_2 = 0.69314718055994530942
HALF_LN_2_PI = 0.91893853320467274178
MAX_FLOAT = 1.7976931348623157e308
MIN_NORMAL_FLOAT = 2.2250738585072014e-308
MAX_EXP_ARGUMENT = 709.782712893384
# Below this value, rounding to a nonzero binary64 result is impossible.
MIN_ROUNDABLE_EXP_ARGUMENT = -745.1332191019412
SERIES_TOLERANCE = 1.0e-16


class InputValidationError(ValueError):
    """Raised when an input is missing or outside the function domain."""


class NumericRangeError(ArithmeticError):
    """Raised when a result cannot be represented as a finite Python float."""


def absolute_value(value):
    """Return the nonnegative magnitude of a real number."""
    if value < 0.0:
        return -value
    return value


def is_finite(value):
    """Return True when value is neither infinity nor NaN."""
    # A NaN is the only floating-point value that is not equal to itself.
    # pylint: disable=comparison-with-itself
    return value == value and -MAX_FLOAT <= value <= MAX_FLOAT


def natural_log(value):
    """Compute ln(value) using range reduction and an atanh-based series."""
    if not is_finite(value) or value <= 0.0:
        raise InputValidationError(
            "Natural logarithm requires a finite value greater than zero."
        )

    reduced = value
    power_of_two = 0

    while reduced >= 2.0:
        reduced *= 0.5
        power_of_two += 1

    while reduced < 1.0:
        reduced *= 2.0
        power_of_two -= 1

    ratio = (reduced - 1.0) / (reduced + 1.0)
    ratio_squared = ratio * ratio
    term = ratio
    denominator = 1.0
    series_sum = 0.0

    while denominator <= 199.0:
        addition = term / denominator
        series_sum += addition
        if absolute_value(addition) <= SERIES_TOLERANCE:
            break
        term *= ratio_squared
        denominator += 2.0

    return 2.0 * series_sum + power_of_two * LN_2


def natural_log_one_plus(value):
    """Compute ln(1 + value) accurately when value is close to zero."""
    if not is_finite(value) or value <= -1.0:
        raise InputValidationError(
            "Log-one-plus requires a finite value greater than negative one."
        )

    if -0.25 <= value <= 0.25:
        term = value
        series_sum = 0.0
        index = 1.0
        sign = 1.0

        while index <= 400.0:
            addition = sign * term / index
            series_sum += addition
            if absolute_value(addition) <= SERIES_TOLERANCE:
                break
            term *= value
            sign = -sign
            index += 1.0
        return series_sum

    return natural_log(1.0 + value)


def exponential(value):
    """Compute exp(value) using range reduction and a Taylor series."""
    if not is_finite(value):
        raise NumericRangeError("The exponential argument must be finite.")
    if value > MAX_EXP_ARGUMENT:
        raise NumericRangeError("The result is too large to represent.")
    if value < MIN_ROUNDABLE_EXP_ARGUMENT:
        raise NumericRangeError(
            "The Beta result is positive but smaller than the minimum nonzero "
            "Python float, so it cannot be represented."
        )

    reduced = value
    power_of_two = 0
    half_ln_2 = 0.5 * LN_2

    while reduced > half_ln_2:
        reduced -= LN_2
        power_of_two += 1

    while reduced < -half_ln_2:
        reduced += LN_2
        power_of_two -= 1

    term = 1.0
    series_sum = 1.0
    index = 1.0

    while index <= 80.0:
        term *= reduced / index
        series_sum += term
        if absolute_value(term) <= SERIES_TOLERANCE:
            break
        index += 1.0

    if power_of_two < -1022:
        divisor = 1.0
        subnormal_shift = -power_of_two - 1022
        while subnormal_shift > 0:
            divisor *= 2.0
            subnormal_shift -= 1
        result = (series_sum * MIN_NORMAL_FLOAT) / divisor
        power_of_two = 0
    else:
        result = series_sum

    while power_of_two > 0:
        result *= 2.0
        power_of_two -= 1
    while power_of_two < 0:
        result *= 0.5
        power_of_two += 1

    if result == 0.0 or not is_finite(result):
        raise NumericRangeError(
            "The Beta result is outside the nonzero finite Python float range."
        )
    return result


def stirling_correction_from_inverse(inverse):
    """Return the correction terms used by the Stirling approximation."""
    inverse_squared = inverse * inverse
    inverse_cubed = inverse * inverse_squared
    inverse_fifth = inverse_cubed * inverse_squared
    inverse_seventh = inverse_fifth * inverse_squared
    inverse_ninth = inverse_seventh * inverse_squared
    inverse_eleventh = inverse_ninth * inverse_squared

    return (
        inverse / 12.0
        - inverse_cubed / 360.0
        + inverse_fifth / 1260.0
        - inverse_seventh / 1680.0
        + inverse_ninth / 1188.0
        - 691.0 * inverse_eleventh / 360360.0
    )


def log_gamma(value):
    """Compute ln(Gamma(value)) using recurrence and a Stirling series."""
    if not is_finite(value) or value <= 0.0:
        raise InputValidationError(
            "Log-gamma requires a finite value greater than zero."
        )

    shifted = value
    recurrence_correction = 0.0

    while shifted < 8.0:
        recurrence_correction -= natural_log(shifted)
        shifted += 1.0

    correction = stirling_correction_from_inverse(1.0 / shifted)

    stirling = (
        (shifted - 0.5) * natural_log(shifted)
        - shifted
        + HALF_LN_2_PI
        + correction
    )
    return stirling + recurrence_correction


def log_beta(x_value, y_value):
    """Compute ln(B(x, y)) without subtracting large log-gamma values."""
    shifted_x = x_value
    shifted_y = y_value
    recurrence_correction = 0.0

    while shifted_x < 8.0:
        recurrence_correction += (
            natural_log(shifted_x + shifted_y) - natural_log(shifted_x)
        )
        shifted_x += 1.0

    while shifted_y < 8.0:
        recurrence_correction += (
            natural_log(shifted_x + shifted_y) - natural_log(shifted_y)
        )
        shifted_y += 1.0

    if shifted_x <= shifted_y:
        smaller = shifted_x
        larger = shifted_y
    else:
        smaller = shifted_y
        larger = shifted_x

    ratio = smaller / larger
    log_one_plus_ratio = natural_log_one_plus(ratio)
    log_sum = natural_log(larger) + log_one_plus_ratio
    log_smaller_fraction = natural_log(ratio) - log_one_plus_ratio
    log_larger_fraction = -log_one_plus_ratio

    inverse_smaller = 1.0 / smaller
    inverse_larger = 1.0 / larger
    inverse_sum = inverse_larger / (1.0 + ratio)
    correction = (
        stirling_correction_from_inverse(inverse_smaller)
        + stirling_correction_from_inverse(inverse_larger)
        - stirling_correction_from_inverse(inverse_sum)
    )

    stable_stirling = (
        (smaller - 0.5) * log_smaller_fraction
        + (larger - 0.5) * log_larger_fraction
        - 0.5 * log_sum
        + HALF_LN_2_PI
        + correction
    )
    return stable_stirling + recurrence_correction


def beta_function(x_value, y_value):
    """Return a representable binary64 B(x, y) for valid inputs.

    Finite positive binary64 inputs are supported. If the mathematical result
    cannot be represented as a nonzero finite Python float, the function
    raises NumericRangeError instead of returning a misleading value.
    """
    if not is_finite(x_value):
        raise InputValidationError("x must be finite.")
    if not is_finite(y_value):
        raise InputValidationError("y must be finite.")
    if x_value <= 0.0:
        raise InputValidationError("x must be greater than zero.")
    if y_value <= 0.0:
        raise InputValidationError("y must be greater than zero.")

    return exponential(log_beta(x_value, y_value))
