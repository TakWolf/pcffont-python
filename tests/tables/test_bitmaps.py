from copy import copy, deepcopy

from pcffont import PcfTableFormat, PcfBitmaps


def test_copy():
    bitmaps_1 = PcfBitmaps(
        [
            [[1, 0, 0, 1]],
            [[0, 1, 1, 0]],
        ],
        table_format=PcfTableFormat.create(True, True, True, 2, 4),
    )
    bitmaps_2 = copy(bitmaps_1)

    assert bitmaps_1 == bitmaps_2
    assert bitmaps_1 is not bitmaps_2

    for bitmap_1, bitmap_2 in zip(bitmaps_1, bitmaps_2):
        assert bitmap_1 is bitmap_2


def test_deepcopy():
    bitmaps_1 = PcfBitmaps(
        [
            [[1, 0, 0, 1]],
            [[0, 1, 1, 0]],
        ],
        table_format=PcfTableFormat.create(True, True, True, 2, 4),
    )
    bitmaps_2 = deepcopy(bitmaps_1)

    assert bitmaps_1 == bitmaps_2
    assert bitmaps_1 is not bitmaps_2

    for bitmap_1, bitmap_2 in zip(bitmaps_1, bitmaps_2):
        assert bitmap_1 is not bitmap_2
        for bitmap_row_1, bitmap_row_2 in zip(bitmap_1, bitmap_2):
            assert bitmap_row_1 is not bitmap_row_2


def test_eq():
    bitmaps_1 = PcfBitmaps(
        [
            [[1, 0, 0, 1]],
            [[0, 1, 1, 0]],
        ],
        table_format=PcfTableFormat.create(True, True, True, 2, 4),
    )
    bitmaps_2 = PcfBitmaps(
        [
            [[1, 0, 0, 1]],
            [[0, 1, 1, 0]],
        ],
        table_format=PcfTableFormat.create(True, True, True, 2, 4),
    )
    assert bitmaps_1 == bitmaps_2
