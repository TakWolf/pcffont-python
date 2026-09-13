from itertools import permutations

from pcffont import PcfMetric
from pcffont.utils import calculate_util


def test_calculate() -> None:
    metrics = [
        PcfMetric(
            left_side_bearing=-3,
            right_side_bearing=8,
            character_width=4,
            ascent=9,
            descent=-5,
            attributes=0b_00000001,
        ),
        PcfMetric(
            left_side_bearing=7,
            right_side_bearing=3,
            character_width=1,
            ascent=-6,
            descent=0,
            attributes=0b_00010001,
        ),
        PcfMetric(
            left_side_bearing=1,
            right_side_bearing=0,
            character_width=2,
            ascent=5,
            descent=4,
            attributes=0b_10000001,
        ),
        PcfMetric(
            left_side_bearing=-5,
            right_side_bearing=-1,
            character_width=7,
            ascent=-3,
            descent=-9,
            attributes=0b_01100001,
        ),
    ]
    assert calculate_util.calculate_max_overlap(metrics) == 4
    assert calculate_util.calculate_min_bounds(metrics) == PcfMetric(
        left_side_bearing=-5,
        right_side_bearing=-1,
        character_width=1,
        ascent=-6,
        descent=-9,
        attributes=0b_00000001,
    )
    assert calculate_util.calculate_max_bounds(metrics) == PcfMetric(
        left_side_bearing=7,
        right_side_bearing=8,
        character_width=7,
        ascent=9,
        descent=4,
        attributes=0b_11110001,
    )


def test_calculate_empty() -> None:
    metrics = []
    assert calculate_util.calculate_max_overlap(metrics) == 0
    assert calculate_util.calculate_min_bounds(metrics) == PcfMetric()
    assert calculate_util.calculate_max_bounds(metrics) == PcfMetric()


def test_calculate_bounds_ignore_zero_geometry_regardless_of_order() -> None:
    zero = PcfMetric(attributes=0b_0011)
    metric_1 = PcfMetric(
        left_side_bearing=5,
        right_side_bearing=8,
        character_width=6,
        ascent=7,
        descent=2,
        attributes=0b_0101,
    )
    metric_2 = PcfMetric(
        left_side_bearing=-2,
        right_side_bearing=4,
        character_width=3,
        ascent=9,
        descent=-1,
        attributes=0b_1001,
    )
    expected_min_bounds = PcfMetric(
        left_side_bearing=-2,
        right_side_bearing=4,
        character_width=3,
        ascent=7,
        descent=-1,
        attributes=0b_0001,
    )
    expected_max_bounds = PcfMetric(
        left_side_bearing=5,
        right_side_bearing=8,
        character_width=6,
        ascent=9,
        descent=2,
        attributes=0b_1111,
    )
    for metrics in permutations([zero, metric_1, metric_2]):
        assert calculate_util.calculate_min_bounds(metrics) == expected_min_bounds
        assert calculate_util.calculate_max_bounds(metrics) == expected_max_bounds


def test_calculate_bounds_all_zero_geometry() -> None:
    metrics = [
        PcfMetric(attributes=0b_0011),
        PcfMetric(attributes=0b_0101),
    ]
    assert calculate_util.calculate_min_bounds(metrics) == PcfMetric(attributes=0b_0001)
    assert calculate_util.calculate_max_bounds(metrics) == PcfMetric(attributes=0b_0111)


def test_calculate_bounds_include_nonzero_character_width() -> None:
    metrics = [
        PcfMetric(attributes=0b_0011),
        PcfMetric(character_width=8, attributes=0b_0101),
    ]
    assert calculate_util.calculate_min_bounds(metrics) == PcfMetric(character_width=8, attributes=0b_0001)
    assert calculate_util.calculate_max_bounds(metrics) == PcfMetric(character_width=8, attributes=0b_0111)


def test_calculate_max_overlap_includes_zero_geometry() -> None:
    metrics = [
        PcfMetric(right_side_bearing=5, character_width=8),
        PcfMetric(),
    ]
    assert calculate_util.calculate_max_overlap(metrics) == 0
