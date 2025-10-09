import math
import pytest
from calculator import sqrt_x, factorial_x, ln_x, power_x_b

# --- sqrt_x ---
@pytest.mark.parametrize("x, expected", [
    (0, 0.0),
    (4, 2.0),
    (9.0, 3.0),
])
def test_sqrt_x_ok(x, expected):
    assert sqrt_x(x) == expected

@pytest.mark.parametrize("x", [-1, -100.5])
def test_sqrt_x_errors(x):
    with pytest.raises(ValueError):
        sqrt_x(x)

# --- factorial_x ---
@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (5, 120),
    (10, math.factorial(10)),
])
def test_factorial_ok(n, expected):
    assert factorial_x(n) == expected

@pytest.mark.parametrize("bad", [-1, -5, 3.5])
def test_factorial_errors(bad):
    with pytest.raises(ValueError):
        factorial_x(bad)

# --- ln_x ---
@pytest.mark.parametrize("x", [1, math.e, 10.5])
def test_ln_ok(x):
    assert ln_x(x) == math.log(x)

@pytest.mark.parametrize("x", [0, -1, -10])
def test_ln_errors(x):
    with pytest.raises(ValueError):
        ln_x(x)

# --- power_x_b ---
@pytest.mark.parametrize("x,b,expected", [
    (2, 3, 8.0),
    (5, 0, 1.0),
    (9, 0.5, 3.0),
    (-2, 4, 16.0),  # negative base with integer exponent is OK
])
def test_power_ok(x, b, expected):
    assert power_x_b(x, b) == pytest.approx(expected)

@pytest.mark.parametrize("x,b", [
    (-2, 0.5),     # negative base to non-integer exponent -> complex
    (-9, 1/3),     # cube root (non-integer float) -> ValueError by our rule
])
def test_power_errors(x, b):
    with pytest.raises(ValueError):
        power_x_b(x, b)

