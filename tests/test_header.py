from copy import copy, deepcopy

from pcffont import PcfTableType, PcfTableFormat
from pcffont.header import PcfHeader


def test_copy():
    header_1 = PcfHeader(
        table_type=PcfTableType.ACCELERATORS,
        table_format=PcfTableFormat(True, True, True, 1, 2),
        table_size=10,
        table_offset=20,
    )
    header_2 = copy(header_1)

    assert header_1 == header_2
    assert header_1 is not header_2
    assert header_1.table_format is header_2.table_format


def test_deepcopy():
    header_1 = PcfHeader(
        table_type=PcfTableType.ACCELERATORS,
        table_format=PcfTableFormat(True, True, True, 1, 2),
        table_size=10,
        table_offset=20,
    )
    header_2 = deepcopy(header_1)

    assert header_1 == header_2
    assert header_1 is not header_2
    assert header_1.table_format is not header_2.table_format


def test_eq():
    header_1 = PcfHeader(
        table_type=PcfTableType.ACCELERATORS,
        table_format=PcfTableFormat(True, True, True, 1, 2),
        table_size=10,
        table_offset=20,
    )
    header_2 = PcfHeader(
        table_type=PcfTableType.ACCELERATORS,
        table_format=PcfTableFormat(True, True, True, 1, 2),
        table_size=10,
        table_offset=20,
    )
    assert header_1 == header_2
