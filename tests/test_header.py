from copy import copy, deepcopy

from pcffont import PcfTableType, PcfTableFormat
from pcffont.header import PcfHeader


def test_copy():
    header_1 = PcfHeader(
        table_type=PcfTableType.ACCELERATORS,
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
        table_size=10,
        table_offset=20,
    )
    header_2 = copy(header_1)
    header_3 = deepcopy(header_1)

    assert header_1 == header_2
    assert header_1 == header_3
    assert header_1 is not header_2
    assert header_1 is not header_3


def test_eq():
    header_1 = PcfHeader(
        table_type=PcfTableType.ACCELERATORS,
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
        table_size=10,
        table_offset=20,
    )
    header_2 = PcfHeader(
        table_type=PcfTableType.ACCELERATORS,
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
        table_size=10,
        table_offset=20,
    )
    assert header_1 == header_2
