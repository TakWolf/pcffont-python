from copy import copy, deepcopy

import pytest

from pcffont import PcfTableType, PcfTableFormat, PcfFont, PcfBdfEncodings
from pcffont.error import PcfParseError
from pcffont.header import PcfHeader
from pcffont.utils.stream import Stream


def test_encodings():
    encodings = PcfBdfEncodings()

    encodings[1] = None
    assert len(encodings) == 0

    encodings[2] = PcfBdfEncodings.NO_GLYPH_INDEX
    assert len(encodings) == 0


def test_empty_dump_parse():
    font = PcfFont()

    encodings_1 = PcfBdfEncodings()
    stream = Stream()
    table_size = encodings_1.dump(stream, 0, font)
    header = PcfHeader(PcfTableType.BDF_ENCODINGS, encodings_1.table_format, table_size, 0)

    stream.seek(0)
    assert stream.read_uint32() == encodings_1.table_format.value
    assert stream.read_uint16() == 0
    assert stream.read_uint16() == 0
    assert stream.read_uint16() == 0
    assert stream.read_uint16() == 0
    assert stream.read_uint16() == PcfBdfEncodings.NO_ENCODING
    assert stream.read_uint16() == PcfBdfEncodings.NO_GLYPH_INDEX

    encodings_2 = PcfBdfEncodings.parse(stream, header, font)
    assert encodings_1 == encodings_2


@pytest.mark.parametrize(
    ('min_byte_2', 'max_byte_2', 'min_byte_1', 'max_byte_1'),
    [
        (1, 0, 0, 0),
        (0, 0, 1, 0),
        (0, 0x100, 0, 0),
        (0, 0, 0, 0x100),
    ],
)
def test_parse_invalid_range(min_byte_2: int, max_byte_2: int, min_byte_1: int, max_byte_1: int):
    stream = Stream()
    stream.write_uint32(PcfTableFormat.DEFAULT)
    stream.write_uint16(min_byte_2)
    stream.write_uint16(max_byte_2)
    stream.write_uint16(min_byte_1)
    stream.write_uint16(max_byte_1)
    stream.write_uint16(PcfBdfEncodings.NO_ENCODING)
    header = PcfHeader(PcfTableType.BDF_ENCODINGS, PcfTableFormat.DEFAULT, stream.tell(), 0)

    with pytest.raises(PcfParseError):
        PcfBdfEncodings.parse(stream, header, PcfFont())


def test_copy():
    encodings_1 = PcfBdfEncodings(
        {
            1: 1,
            2: 2,
            3: 3,
        },
        table_format=PcfTableFormat.create(True, True, True, 2, 4),
        default_char=1,
    )
    encodings_2 = copy(encodings_1)
    encodings_3 = deepcopy(encodings_1)

    assert encodings_1 == encodings_2
    assert encodings_1 == encodings_3
    assert encodings_1 is not encodings_2
    assert encodings_1 is not encodings_3


def test_eq():
    encodings_1 = PcfBdfEncodings(
        {
            1: 1,
            2: 2,
            3: 3,
        },
        table_format=PcfTableFormat.create(True, True, True, 2, 4),
        default_char=1,
    )
    encodings_2 = PcfBdfEncodings(
        {
            1: 1,
            2: 2,
            3: 3,
        },
        table_format=PcfTableFormat.create(True, True, True, 2, 4),
        default_char=1,
    )
    assert encodings_1 == encodings_2
