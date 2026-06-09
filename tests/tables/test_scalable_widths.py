from copy import copy, deepcopy

from pcffont import PcfTableFormat, PcfScalableWidths


def test_copy():
    scalable_widths_1 = PcfScalableWidths(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        scalable_widths=[1, 2, 3, 4],
    )
    scalable_widths_2 = copy(scalable_widths_1)

    assert scalable_widths_1 == scalable_widths_2
    assert scalable_widths_1 is not scalable_widths_2
    assert scalable_widths_1.table_format is scalable_widths_2.table_format


def test_deepcopy():
    scalable_widths_1 = PcfScalableWidths(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        scalable_widths=[1, 2, 3, 4],
    )
    scalable_widths_2 = deepcopy(scalable_widths_1)

    assert scalable_widths_1 == scalable_widths_2
    assert scalable_widths_1 is not scalable_widths_2
    assert scalable_widths_1.table_format is not scalable_widths_2.table_format


def test_eq():
    scalable_widths_1 = PcfScalableWidths(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        scalable_widths=[1, 2, 3, 4],
    )
    scalable_widths_2 = PcfScalableWidths(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        scalable_widths=[1, 2, 3, 4],
    )
    assert scalable_widths_1 == scalable_widths_2
