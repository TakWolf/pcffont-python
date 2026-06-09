from copy import copy, deepcopy

from pcffont import PcfTableFormat, PcfGlyphNames


def test_copy():
    names_1 = PcfGlyphNames(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        names=['A', 'B', 'C'],
    )
    names_2 = copy(names_1)

    assert names_1 == names_2
    assert names_1 is not names_2
    assert names_1.table_format is names_2.table_format


def test_deepcopy():
    names_1 = PcfGlyphNames(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        names=['A', 'B', 'C'],
    )
    names_2 = deepcopy(names_1)

    assert names_1 == names_2
    assert names_1 is not names_2
    assert names_1.table_format is not names_2.table_format


def test_eq():
    names_1 = PcfGlyphNames(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        names=['A', 'B', 'C'],
    )
    names_2 = PcfGlyphNames(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        names=['A', 'B', 'C'],
    )
    assert names_1 == names_2
