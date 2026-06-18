from copy import copy, deepcopy

from pcffont import PcfTableFormat, PcfGlyphNames


def test_copy():
    names_1 = PcfGlyphNames(
        ['A', 'B', 'C'],
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
    )
    names_2 = copy(names_1)
    names_3 = deepcopy(names_1)

    assert names_1 == names_2
    assert names_1 == names_3
    assert names_1 is not names_2
    assert names_1 is not names_3


def test_eq():
    names_1 = PcfGlyphNames(
        ['A', 'B', 'C'],
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
    )
    names_2 = PcfGlyphNames(
        ['A', 'B', 'C'],
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
    )
    assert names_1 == names_2
