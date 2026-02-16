import math
import pytest
from stats.personal_best import calculate_wca_avg


class TestCalculateWcaAvg:
    """Tests for calculate_wca_avg following WCA trimmed-average rules."""

    # --- Insufficient times ---

    def test_returns_none_when_fewer_than_count(self):
        assert calculate_wca_avg([10.0, 12.0, 11.0], 5) is None

    def test_returns_none_for_empty_list(self):
        assert calculate_wca_avg([], 5) is None

    def test_returns_none_for_single_time(self):
        assert calculate_wca_avg([10.0], 5) is None

    # --- Ao5 ---

    def test_ao5_basic(self):
        # times: 10, 12, 11, 9, 13 → sorted: 9, 10, 11, 12, 13 → trim best/worst → avg(10, 11, 12) = 11.0
        result = calculate_wca_avg([10.0, 12.0, 11.0, 9.0, 13.0], 5)
        assert result == pytest.approx(11.0)

    def test_ao5_identical_times(self):
        result = calculate_wca_avg([8.0, 8.0, 8.0, 8.0, 8.0], 5)
        assert result == pytest.approx(8.0)

    def test_ao5_with_decimals(self):
        # sorted: 9.12, 10.50, 11.33, 12.78, 14.01 → trim → avg(10.50, 11.33, 12.78)
        result = calculate_wca_avg([10.50, 12.78, 11.33, 9.12, 14.01], 5)
        assert result == pytest.approx((10.50 + 11.33 + 12.78) / 3)

    # --- Ao12 ---

    def test_ao12_basic(self):
        times = [10.0, 12.0, 11.0, 9.0, 13.0, 8.0, 14.0, 11.5, 10.5, 12.5, 9.5, 13.5]
        # sorted: 8, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14
        # trim best(8) and worst(14) → avg of middle 10
        expected = (9.0 + 9.5 + 10.0 + 10.5 + 11.0 + 11.5 + 12.0 + 12.5 + 13.0 + 13.5) / 10
        result = calculate_wca_avg(times, 12)
        assert result == pytest.approx(expected)

    # --- DNF handling ---

    def test_ao5_single_dnf_is_trimmed(self):
        # One DNF gets sorted as worst and trimmed
        # sorted: 9, 10, 11, 12, inf → trim 9 and inf → avg(10, 11, 12) = 11.0
        result = calculate_wca_avg([10.0, float("inf"), 11.0, 9.0, 12.0], 5)
        assert result == pytest.approx(11.0)

    def test_ao5_two_dnfs_returns_inf(self):
        result = calculate_wca_avg([10.0, float("inf"), float("inf"), 9.0, 12.0], 5)
        assert result == float("inf")

    def test_ao5_all_dnfs_returns_inf(self):
        result = calculate_wca_avg([float("inf")] * 5, 5)
        assert result == float("inf")

    # --- Window behavior ---

    def test_uses_only_first_count_elements(self):
        # Provide 7 times but ask for Ao5 → only first 5 should be used
        times = [10.0, 12.0, 11.0, 9.0, 13.0, 1.0, 1.0]
        result_ao5 = calculate_wca_avg(times, 5)
        expected = calculate_wca_avg(times[:5], 5)
        assert result_ao5 == pytest.approx(expected)

    def test_extra_times_do_not_affect_result(self):
        # The 6th/7th elements (very fast times) should not change Ao5
        base = [10.0, 12.0, 11.0, 9.0, 13.0]
        extended = base + [0.5, 0.5]
        assert calculate_wca_avg(base, 5) == pytest.approx(calculate_wca_avg(extended, 5))

    # --- Trimming correctness ---

    def test_best_and_worst_are_excluded(self):
        # 5, 10, 15, 20, 25 → trim 5 and 25 → avg(10, 15, 20) = 15.0
        result = calculate_wca_avg([5.0, 10.0, 15.0, 20.0, 25.0], 5)
        assert result == pytest.approx(15.0)

    def test_exactly_count_times(self):
        # Exactly 12 times should work
        times = [float(i) for i in range(1, 13)]
        result = calculate_wca_avg(times, 12)
        # sorted: 1..12, trim 1 and 12 → avg(2..11) = 6.5
        assert result == pytest.approx(6.5)
