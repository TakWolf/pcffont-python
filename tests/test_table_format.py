import pytest

from pcffont import PcfTableFormat


def test_value():
    assert PcfTableFormat().value == 0
    assert PcfTableFormat(glyph_pad_index=2).value == 2
    assert PcfTableFormat(ms_byte_first=True, ms_bit_first=True).value == 12
    assert PcfTableFormat(ms_byte_first=True, ms_bit_first=True, glyph_pad_index=2).value == 14
    assert PcfTableFormat(ink_bounds_or_compressed_metrics=True, glyph_pad_index=2).value == 258
    assert PcfTableFormat(ms_byte_first=True, ms_bit_first=True, ink_bounds_or_compressed_metrics=True, glyph_pad_index=2).value == 270


def test_parse():
    table_format = PcfTableFormat.parse(270)
    assert table_format.ms_byte_first
    assert table_format.ms_bit_first
    assert table_format.ink_bounds_or_compressed_metrics
    assert table_format.ink_bounds
    assert table_format.compressed_metrics
    assert table_format.glyph_pad_index == 2
    assert table_format.scan_unit_index == 0


def test_eq():
    table_format_1 = PcfTableFormat(ms_byte_first=True)
    table_format_2 = PcfTableFormat(ms_byte_first=True)
    table_format_3 = PcfTableFormat(glyph_pad_index=2)
    assert table_format_1 == table_format_2
    assert table_format_1 != table_format_3
    assert table_format_1 != 1
    assert table_format_1 != 'Hello World!'


def test_glyph_pad():
    table_format = PcfTableFormat(glyph_pad_index=-1)
    table_format.glyph_pad = 1
    assert table_format.glyph_pad_index == 0
    table_format.glyph_pad = 2
    assert table_format.glyph_pad_index == 1
    table_format.glyph_pad = 4
    assert table_format.glyph_pad_index == 2
    table_format.glyph_pad = 8
    assert table_format.glyph_pad_index == 3

    with pytest.raises(ValueError):
        table_format.glyph_pad = 16


def test_scan_unit():
    table_format = PcfTableFormat(scan_unit_index=-1)
    table_format.scan_unit = 1
    assert table_format.scan_unit_index == 0
    table_format.scan_unit = 2
    assert table_format.scan_unit_index == 1
    table_format.scan_unit = 4
    assert table_format.scan_unit_index == 2

    with pytest.raises(ValueError):
        table_format.scan_unit = 8


def test_bitmaps_size_configs():
    table_format = PcfTableFormat()
    table_format.glyph_pad = 1
    assert table_format.bitmaps_size_configs(16) == [16, 32, 64, 128]
    table_format.glyph_pad = 2
    assert table_format.bitmaps_size_configs(16) == [8, 16, 32, 64]
    table_format.glyph_pad = 4
    assert table_format.bitmaps_size_configs(16) == [4, 8, 16, 32]
    table_format.glyph_pad = 8
    assert table_format.bitmaps_size_configs(16) == [2, 4, 8, 16]
