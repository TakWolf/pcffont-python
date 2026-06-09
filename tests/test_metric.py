from copy import copy, deepcopy

from pcffont import PcfMetric


def test_metric():
    metric = PcfMetric(
        left_side_bearing=1,
        right_side_bearing=2,
        character_width=3,
        ascent=4,
        descent=5,
    )
    assert metric.width == 1
    assert metric.height == 9
    assert metric.dimensions == (1, 9)
    assert metric.offset_x == 1
    assert metric.offset_y == -5
    assert metric.offset == (1, -5)


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
    metric_2 = copy(metric_1)
    metric_3 = deepcopy(metric_1)

    assert metric_1 == metric_2
    assert metric_1 == metric_3
    assert metric_1 is not metric_2
    assert metric_1 is not metric_3


def test_eq():
    metric_1 = PcfMetric(
        left_side_bearing=1,
        right_side_bearing=2,
        character_width=3,
        ascent=4,
        descent=5,
        attributes=6,
    )
    metric_2 = PcfMetric(
        left_side_bearing=1,
        right_side_bearing=2,
        character_width=3,
        ascent=4,
        descent=5,
        attributes=6,
    )
    assert metric_1 == metric_2
