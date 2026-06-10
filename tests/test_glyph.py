from copy import copy, deepcopy

from pcffont import PcfGlyph, PcfMetric


def test_glyph():
    glyph = PcfGlyph(
        name='_',
        encoding=0,
        dimensions=(1, 2),
        offset=(3, 4),
    )
    assert glyph.width == 1
    assert glyph.height == 2
    assert glyph.dimensions == (1, 2)
    assert glyph.offset_x == 3
    assert glyph.offset_y == 4
    assert glyph.offset == (3, 4)


def test_create_metric_1():
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


def test_create_metric_2():
    glyph = PcfGlyph(
        name='_',
        encoding=0,
        character_width=5,
        dimensions=(7, 10),
        offset=(0, -4),
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
        right_side_bearing=7,
        character_width=5,
        ascent=6,
        descent=4,
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


def test_copy():
    glyph_1 = PcfGlyph(
        name='_',
        encoding=0,
        character_width=1,
        dimensions=(2, 3),
        offset=(4, 5),
        bitmap=[[1, 0, 0, 1]],
        attributes=1,
    )
    glyph_2 = copy(glyph_1)

    assert glyph_1 == glyph_2
    assert glyph_1 is not glyph_2
    assert glyph_1.bitmap is glyph_2.bitmap


def test_deepcopy():
    glyph_1 = PcfGlyph(
        name='_',
        encoding=0,
        character_width=1,
        dimensions=(2, 3),
        offset=(4, 5),
        bitmap=[[1, 0, 0, 1]],
        attributes=1,
    )
    glyph_2 = deepcopy(glyph_1)

    assert glyph_1 == glyph_2
    assert glyph_1 is not glyph_2
    assert glyph_1.bitmap is not glyph_2.bitmap

    for bitmap_row_1, bitmap_row_2 in zip(glyph_1.bitmap, glyph_2.bitmap):
        assert bitmap_row_1 is not bitmap_row_2


def test_eq():
    glyph_1 = PcfGlyph(
        name='_',
        encoding=0,
        character_width=1,
        dimensions=(2, 3),
        offset=(4, 5),
        bitmap=[[1, 0, 0, 1]],
        attributes=1,
    )
    glyph_2 = PcfGlyph(
        name='_',
        encoding=0,
        character_width=1,
        dimensions=(2, 3),
        offset=(4, 5),
        bitmap=[[1, 0, 0, 1]],
        attributes=1,
    )
    assert glyph_1 == glyph_2
