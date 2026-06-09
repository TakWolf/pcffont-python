from copy import copy, deepcopy

from pcffont import PcfTableFormat, PcfBitmaps


def test_copy():
    bitmaps_1 = PcfBitmaps(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        bitmaps=[
            [[1, 0, 0, 1]],
            [[0, 1, 1, 0]],
        ],
    )
    bitmaps_2 = copy(bitmaps_1)

    assert bitmaps_1 == bitmaps_2
    assert bitmaps_1 is not bitmaps_2
    assert bitmaps_1.table_format is bitmaps_2.table_format

    for bitmap_1, bitmap_2 in zip(bitmaps_1, bitmaps_2):
        assert bitmap_1 is bitmap_2


def test_deepcopy():
    bitmaps_1 = PcfBitmaps(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        bitmaps=[
            [[1, 0, 0, 1]],
            [[0, 1, 1, 0]],
        ],
    )
    bitmaps_2 = deepcopy(bitmaps_1)

    assert bitmaps_1 == bitmaps_2
    assert bitmaps_1 is not bitmaps_2
    assert bitmaps_1.table_format is not bitmaps_2.table_format

    for bitmap_1, bitmap_2 in zip(bitmaps_1, bitmaps_2):
        assert bitmap_1 is not bitmap_2
        for bitmap_row_1, bitmap_row_2 in zip(bitmap_1, bitmap_2):
            assert bitmap_row_1 is not bitmap_row_2


def test_eq():
    bitmaps_1 = PcfBitmaps(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        bitmaps=[
            [[1, 0, 0, 1]],
            [[0, 1, 1, 0]],
        ],
    )
    bitmaps_2 = PcfBitmaps(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        bitmaps=[
            [[1, 0, 0, 1]],
            [[0, 1, 1, 0]],
        ],
    )
    assert bitmaps_1 == bitmaps_2
