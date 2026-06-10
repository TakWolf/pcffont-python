from copy import copy, deepcopy

from pcffont import PcfTableFormat, PcfBdfEncodings


def test_encodings():
    encodings = PcfBdfEncodings()

    encodings[1] = None
    assert len(encodings) == 0

    encodings[2] = PcfBdfEncodings.NO_GLYPH_INDEX
    assert len(encodings) == 0


def test_copy():
    encodings_1 = PcfBdfEncodings(
        {
            1: 1,
            2: 2,
            3: 3,
        },
        table_format=PcfTableFormat(True, True, True, 1, 2),
        default_char=1,
    )
    encodings_2 = copy(encodings_1)

    assert encodings_1 == encodings_2
    assert encodings_1 is not encodings_2
    assert encodings_1.table_format is encodings_2.table_format


def test_deepcopy():
    encodings_1 = PcfBdfEncodings(
        {
            1: 1,
            2: 2,
            3: 3,
        },
        table_format=PcfTableFormat(True, True, True, 1, 2),
        default_char=1,
    )
    encodings_2 = deepcopy(encodings_1)

    assert encodings_1 == encodings_2
    assert encodings_1 is not encodings_2
    assert encodings_1.table_format is not encodings_2.table_format


def test_eq():
    encodings_1 = PcfBdfEncodings(
        {
            1: 1,
            2: 2,
            3: 3,
        },
        table_format=PcfTableFormat(True, True, True, 1, 2),
        default_char=1,
    )
    encodings_2 = PcfBdfEncodings(
        {
            1: 1,
            2: 2,
            3: 3,
        },
        table_format=PcfTableFormat(True, True, True, 1, 2),
        default_char=1,
    )
    assert encodings_1 == encodings_2
