from copy import copy, deepcopy

from pcffont import PcfMetric, PcfGlyph
from pcffont.utils import calculate_util


def test_eq():
    metric_1 = PcfMetric(
        left_side_bearing=-3,
        right_side_bearing=8,
        character_width=4,
        ascent=9,
        descent=-5,
        attributes=1,
    )
    metric_2 = PcfMetric(
        left_side_bearing=-3,
        right_side_bearing=8,
        character_width=4,
        ascent=9,
        descent=-5,
        attributes=1,
    )
    metric_3 = PcfMetric(
        left_side_bearing=-2,
        right_side_bearing=8,
        character_width=4,
        ascent=9,
        descent=-5,
        attributes=1,
    )
    assert metric_1 == metric_2
    assert metric_1 != metric_3
    assert metric_1 != 1
    assert metric_1 != 'Hello World!'


def test_compressible():
    metric = PcfMetric(attributes=1)
    assert not metric.compressible
    metric.attributes = 0
    assert metric.compressible

    metric.left_side_bearing = -129
    assert not metric.compressible
    metric.left_side_bearing = -128
    assert metric.compressible
    metric.left_side_bearing = 128
    assert not metric.compressible
    metric.left_side_bearing = 127
    assert metric.compressible

    metric.right_side_bearing = -129
    assert not metric.compressible
    metric.right_side_bearing = -128
    assert metric.compressible
    metric.right_side_bearing = 128
    assert not metric.compressible
    metric.right_side_bearing = 127
    assert metric.compressible

    metric.character_width = -129
    assert not metric.compressible
    metric.character_width = -128
    assert metric.compressible
    metric.character_width = 128
    assert not metric.compressible
    metric.character_width = 127
    assert metric.compressible

    metric.ascent = -129
    assert not metric.compressible
    metric.ascent = -128
    assert metric.compressible
    metric.ascent = 128
    assert not metric.compressible
    metric.ascent = 127
    assert metric.compressible

    metric.descent = -129
    assert not metric.compressible
    metric.descent = -128
    assert metric.compressible
    metric.descent = 128
    assert not metric.compressible
    metric.descent = 127
    assert metric.compressible


def test_copy():
    metric_1 = PcfMetric(
        left_side_bearing=1,
        right_side_bearing=2,
        character_width=3,
        ascent=4,
        descent=5,
        attributes=6,
    )

    metric_2 = metric_1.deepcopy()
    assert metric_1 == metric_2
    assert metric_1 is not metric_2

    metric_3 = copy(metric_1)
    assert metric_1 == metric_3
    assert metric_1 is not metric_3

    metric_4 = deepcopy(metric_1)
    assert metric_1 == metric_4
    assert metric_1 is not metric_4


def test_create_by_glyph():
    glyph = PcfGlyph(
        name='_',
        encoding=0,
        character_width=5,
        dimensions=(5, 8),
        offset=(0, -2),
        bitmap=[
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ],
        attributes=1,
    )
    assert glyph.create_metric(False) == PcfMetric(
        left_side_bearing=0,
        right_side_bearing=5,
        character_width=5,
        ascent=6,
        descent=2,
        attributes=1,
    )
    assert glyph.create_metric(True) == PcfMetric(
        left_side_bearing=1,
        right_side_bearing=4,
        character_width=5,
        ascent=5,
        descent=1,
        attributes=1,
    )


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
