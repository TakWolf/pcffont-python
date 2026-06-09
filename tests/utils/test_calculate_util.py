from pcffont import PcfMetric
from pcffont.utils import calculate_util


def test_calculate_1():
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


def test_calculate_2():
    metrics = []
    assert calculate_util.calculate_max_overlap(metrics) == 0
    assert calculate_util.calculate_min_bounds(metrics) == PcfMetric()
    assert calculate_util.calculate_max_bounds(metrics) == PcfMetric()
