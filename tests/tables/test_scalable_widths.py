from copy import copy, deepcopy

from pcffont import PcfTableFormat, PcfScalableWidths


def test_copy():
    scalable_widths_1 = PcfScalableWidths(
        [1, 2, 3, 4],
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
    )
    scalable_widths_2 = copy(scalable_widths_1)
    scalable_widths_3 = deepcopy(scalable_widths_1)

    assert scalable_widths_1 == scalable_widths_2
    assert scalable_widths_1 == scalable_widths_3
    assert scalable_widths_1 is not scalable_widths_2
    assert scalable_widths_1 is not scalable_widths_3


def test_eq():
    scalable_widths_1 = PcfScalableWidths(
        [1, 2, 3, 4],
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
    )
    scalable_widths_2 = PcfScalableWidths(
        [1, 2, 3, 4],
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
    )
    assert scalable_widths_1 == scalable_widths_2
