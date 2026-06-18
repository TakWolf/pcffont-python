import pytest

from pcffont import PcfTableFormat


def test_value_1():
    table_format = PcfTableFormat.of()
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
    table_format = PcfTableFormat.of(
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

    table_format = table_format.with_ms_byte_first(True)
    assert table_format.ms_byte_first

    table_format = table_format.with_ms_byte_first(False)
    assert not table_format.ms_byte_first


def test_ms_bit_first():
    table_format = PcfTableFormat.DEFAULT
    assert not table_format.ms_bit_first

    table_format = table_format.with_ms_bit_first(True)
    assert table_format.ms_bit_first

    table_format = table_format.with_ms_bit_first(False)
    assert not table_format.ms_bit_first


def test_ink_bounds():
    table_format = PcfTableFormat.DEFAULT
    assert not table_format.ink_bounds

    table_format = table_format.with_ink_bounds(True)
    assert table_format.ink_bounds

    table_format = table_format.with_ink_bounds(False)
    assert not table_format.ink_bounds


def test_compressed_metrics():
    table_format = PcfTableFormat.DEFAULT
    assert not table_format.compressed_metrics

    table_format = table_format.with_compressed_metrics(True)
    assert table_format.compressed_metrics

    table_format = table_format.with_compressed_metrics(False)
    assert not table_format.compressed_metrics


def test_glyph_pad_1():
    table_format = PcfTableFormat.DEFAULT
    assert table_format.glyph_pad_index == 0
    assert table_format.glyph_pad == 1

    table_format = table_format.with_glyph_pad_index(1)
    assert table_format.glyph_pad_index == 1
    assert table_format.glyph_pad == 2

    table_format = table_format.with_glyph_pad_index(2)
    assert table_format.glyph_pad_index == 2
    assert table_format.glyph_pad == 4

    table_format = table_format.with_glyph_pad_index(3)
    assert table_format.glyph_pad_index == 3
    assert table_format.glyph_pad == 8

    table_format = table_format.with_glyph_pad_index(0)
    assert table_format.glyph_pad_index == 0
    assert table_format.glyph_pad == 1

    with pytest.raises(IndexError):
        table_format.with_glyph_pad_index(4)


def test_glyph_pad_2():
    table_format = PcfTableFormat.DEFAULT
    assert table_format.glyph_pad == 1
    assert table_format.glyph_pad_index == 0

    table_format = table_format.with_glyph_pad(2)
    assert table_format.glyph_pad == 2
    assert table_format.glyph_pad_index == 1

    table_format = table_format.with_glyph_pad(4)
    assert table_format.glyph_pad == 4
    assert table_format.glyph_pad_index == 2

    table_format = table_format.with_glyph_pad(8)
    assert table_format.glyph_pad == 8
    assert table_format.glyph_pad_index == 3

    table_format = table_format.with_glyph_pad(1)
    assert table_format.glyph_pad == 1
    assert table_format.glyph_pad_index == 0

    with pytest.raises(ValueError):
        table_format.with_glyph_pad(16)


def test_scan_unit_1():
    table_format = PcfTableFormat.DEFAULT
    assert table_format.scan_unit_index == 0
    assert table_format.scan_unit == 1

    table_format = table_format.with_scan_unit_index(1)
    assert table_format.scan_unit_index == 1
    assert table_format.scan_unit == 2

    table_format = table_format.with_scan_unit_index(2)
    assert table_format.scan_unit_index == 2
    assert table_format.scan_unit == 4

    table_format = table_format.with_scan_unit_index(0)
    assert table_format.scan_unit_index == 0
    assert table_format.scan_unit == 1

    with pytest.raises(IndexError):
        table_format.with_scan_unit_index(3)


def test_scan_unit_2():
    table_format = PcfTableFormat.DEFAULT
    assert table_format.scan_unit == 1
    assert table_format.scan_unit_index == 0

    table_format = table_format.with_scan_unit(2)
    assert table_format.scan_unit == 2
    assert table_format.scan_unit_index == 1

    table_format = table_format.with_scan_unit(4)
    assert table_format.scan_unit == 4
    assert table_format.scan_unit_index == 2

    table_format = table_format.with_scan_unit(1)
    assert table_format.scan_unit == 1
    assert table_format.scan_unit_index == 0

    with pytest.raises(ValueError):
        table_format.with_scan_unit(8)


def test_eq():
    table_format_1 = PcfTableFormat.of(
        ms_byte_first=True,
        ms_bit_first=True,
        ink_bounds_or_compressed_metrics=True,
        glyph_pad=2,
        scan_unit=4,
    )
    table_format_2 = PcfTableFormat.of(
        ms_byte_first=True,
        ms_bit_first=True,
        ink_bounds_or_compressed_metrics=True,
        glyph_pad=2,
        scan_unit=4,
    )
    assert table_format_1 == table_format_2
