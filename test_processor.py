"""
test_processor.py - Hypothesis Fuzz Testing Suite for Lab 7
Uncovers input validation edge cases and verifies robustness against unexpected inputs.
"""

import math
import pytest
from hypothesis import given, strategies as st
from visa_application import parse_application, processing_average, payable_fee


# =====================================================================
# 1. Hypothesis Fuzzing Tests (Crash Detection across all text | None)
# =====================================================================

@given(st.text() | st.none())
def test_parse_application_no_crash(s):
    """Fuzz testing parse_application to ensure it never crashes on arbitrary inputs."""
    try:
        parse_application(s)
    except Exception as e:
        assert False, f"parse_application crashed with: {e}"


@given(st.text() | st.none())
def test_processing_average_no_crash(s):
    """Fuzz testing processing_average to ensure it never crashes on arbitrary inputs."""
    try:
        processing_average(s)
    except Exception as e:
        assert False, f"processing_average crashed with: {e}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    """Fuzz testing payable_fee to ensure it never crashes on arbitrary inputs."""
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e}"


# =====================================================================
# 2. Hypothesis Property-Based Tests (Behavior on valid inputs)
# =====================================================================

@given(
    visa_type=st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll')), min_size=1, max_size=30),
    entries=st.integers(min_value=0, max_value=100)
)
def test_parse_application_valid_properties(visa_type, entries):
    """Verify parse_application returns properly formatted title and integer entries on valid inputs."""
    raw = f"{visa_type}:{entries}"
    res = parse_application(raw)
    assert res is not None
    assert res[0] == visa_type.strip().title()
    assert res[1] == entries


@given(
    nums=st.lists(st.integers(min_value=0, max_value=1000), min_size=1, max_size=50)
)
def test_processing_average_valid_properties(nums):
    """Verify processing_average computes exact integer floor average on non-empty valid numbers."""
    csv_str = ",".join(str(n) for n in nums)
    expected = sum(nums) // len(nums)
    assert processing_average(csv_str) == expected


@given(
    fee=st.floats(min_value=0.0, max_value=1e6, allow_nan=False, allow_infinity=False),
    discount=st.floats(min_value=0.0, max_value=1e6, allow_nan=False, allow_infinity=False)
)
def test_payable_fee_valid_properties(fee, discount):
    """Verify payable_fee computes fee * 1.18 - discount and clamps to minimum 0.0."""
    raw = f"{fee}|{discount}"
    res = payable_fee(raw)
    expected = max(float(fee * 1.18 - discount), 0.0)
    assert math.isclose(res, expected, rel_tol=1e-5, abs_tol=1e-5)


# =====================================================================
# 3. Specific Edge-Case Unit Tests Discovered via Fuzzing
# =====================================================================

def test_parse_application_edge_cases():
    """Specific edge-cases: missing colon, multiple colons, empty fields, negative entries."""
    assert parse_application(None) is None
    assert parse_application("") is None
    assert parse_application("tourist") is None
    assert parse_application("tourist:2:extra") is None
    assert parse_application(":2") is None
    assert parse_application("tourist:abc") is None
    assert parse_application("tourist:-5") is None
    assert parse_application("  tourist  :  3  ") == ("Tourist", 3)


def test_processing_average_edge_cases():
    """Specific edge-cases: empty string, missing elements, non-integers, empty entries."""
    assert processing_average(None) == 0
    assert processing_average("") == 0
    assert processing_average("1,,3") == 2
    assert processing_average(",,") == 0
    assert processing_average("5, ten, 21") == 13  # parses 5 and 21 (sum 26 // 2 = 13)
    assert processing_average("   ") == 0


def test_payable_fee_edge_cases():
    """Specific edge-cases: missing pipe, multiple pipes, non-numeric values, negative discount."""
    assert payable_fee(None) == 0.0
    assert payable_fee("") == 0.0
    assert payable_fee("6000") == 0.0
    assert payable_fee("6000|500|100") == 0.0
    assert payable_fee("abc|500") == 0.0
    assert payable_fee("6000|xyz") == 0.0
    assert payable_fee("-100|0") == 0.0
    assert payable_fee("100|-50") == 0.0
    assert payable_fee("6000|500") == 6580.0
