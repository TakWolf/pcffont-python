import pytest

from pcffont import PcfTableFormat


def test_value_1():
    table_format = PcfTableFormat.create()
    assert table_format == PcfTableFormat.DEFAULT
    assert not table_format.ms_byte_first
    assert not table_format.ms_bit_first
    assert not table_format.ink_bounds
    assert not table_format.compressed_metrics
    assert table_format.glyph_pad_index == 0
    assert table_format.glyph_pad == 1
    assert table_format.scan_unit_index == 0
    assert table_format.scan_unit == 1


def test_value_2():
    table_format = PcfTableFormat.create(
        ms_byte_first=True,
        ms_bit_first=True,
        ink_bounds_or_compressed_metrics=True,
        glyph_pad=2,
        scan_unit=4,
    )
    assert table_format == PcfTableFormat(0b_01_00_10_11_01)
    assert table_format.ms_byte_first
    assert table_format.ms_bit_first
    assert table_format.ink_bounds
    assert table_format.compressed_metrics
    assert table_format.glyph_pad_index == 1
    assert table_format.glyph_pad == 2
    assert table_format.scan_unit_index == 2
    assert table_format.scan_unit == 4


def test_ms_byte_first():
    table_format = PcfTableFormat.DEFAULT
    assert not table_format.ms_byte_first

    table_format = table_format.replace(ms_byte_first=True)
    assert table_format.ms_byte_first

    table_format = table_format.replace(ms_byte_first=False)
    assert not table_format.ms_byte_first


def test_ms_bit_first():
    table_format = PcfTableFormat.DEFAULT
    assert not table_format.ms_bit_first

    table_format = table_format.replace(ms_bit_first=True)
    assert table_format.ms_bit_first

    table_format = table_format.replace(ms_bit_first=False)
    assert not table_format.ms_bit_first


def test_ink_bounds_or_compressed_metrics():
    table_format = PcfTableFormat.DEFAULT
    assert not table_format.ink_bounds
    assert not table_format.compressed_metrics

    table_format = table_format.replace(ink_bounds_or_compressed_metrics=True)
    assert table_format.ink_bounds
    assert table_format.compressed_metrics

    table_format = table_format.replace(ink_bounds_or_compressed_metrics=False)
    assert not table_format.ink_bounds
    assert not table_format.compressed_metrics


def test_glyph_pad():
    table_format = PcfTableFormat.DEFAULT
    assert table_format.glyph_pad == 1
    assert table_format.glyph_pad_index == 0

    table_format = table_format.replace(glyph_pad=2)
    assert table_format.glyph_pad == 2
    assert table_format.glyph_pad_index == 1

    table_format = table_format.replace(glyph_pad=4)
    assert table_format.glyph_pad == 4
    assert table_format.glyph_pad_index == 2

    table_format = table_format.replace(glyph_pad=8)
    assert table_format.glyph_pad == 8
    assert table_format.glyph_pad_index == 3

    table_format = table_format.replace(glyph_pad=1)
    assert table_format.glyph_pad == 1
    assert table_format.glyph_pad_index == 0

    with pytest.raises(ValueError):
        table_format.replace(glyph_pad=16)


def test_scan_unit():
    table_format = PcfTableFormat.DEFAULT
    assert table_format.scan_unit == 1
    assert table_format.scan_unit_index == 0

    table_format = table_format.replace(scan_unit=2)
    assert table_format.scan_unit == 2
    assert table_format.scan_unit_index == 1

    table_format = table_format.replace(scan_unit=4)
    assert table_format.scan_unit == 4
    assert table_format.scan_unit_index == 2

    table_format = table_format.replace(scan_unit=1)
    assert table_format.scan_unit == 1
    assert table_format.scan_unit_index == 0

    with pytest.raises(ValueError):
        table_format.replace(scan_unit=8)


def test_eq():
    table_format_1 = PcfTableFormat.create(
        ms_byte_first=True,
        ms_bit_first=True,
        ink_bounds_or_compressed_metrics=True,
        glyph_pad=2,
        scan_unit=4,
    )
    table_format_2 = PcfTableFormat.create(
        ms_byte_first=True,
        ms_bit_first=True,
        ink_bounds_or_compressed_metrics=True,
        glyph_pad=2,
        scan_unit=4,
    )
    assert table_format_1 == table_format_2
