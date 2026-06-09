from copy import copy, deepcopy

import pytest

from pcffont import PcfFontConfig, PcfTableFormat


def test_to_table_format():
    assert PcfFontConfig().to_table_format() == PcfTableFormat()
    assert PcfFontConfig(
        ms_byte_first=True,
        ms_bit_first=True,
        glyph_pad_index=1,
        scan_unit_index=2,
    ).to_table_format() == PcfTableFormat(
        ms_byte_first=True,
        ms_bit_first=True,
        glyph_pad_index=1,
        scan_unit_index=2,
    )


def test_glyph_pad_1():
    config = PcfFontConfig(glyph_pad_index=-1)
    config.glyph_pad_index = 0
    assert config.glyph_pad == 1
    config.glyph_pad_index = 1
    assert config.glyph_pad == 2
    config.glyph_pad_index = 2
    assert config.glyph_pad == 4
    config.glyph_pad_index = 3
    assert config.glyph_pad == 8

    config.glyph_pad_index = 4
    with pytest.raises(IndexError):
        _ = config.glyph_pad


def test_glyph_pad_2():
    config = PcfFontConfig(glyph_pad_index=-1)
    config.glyph_pad = 1
    assert config.glyph_pad_index == 0
    config.glyph_pad = 2
    assert config.glyph_pad_index == 1
    config.glyph_pad = 4
    assert config.glyph_pad_index == 2
    config.glyph_pad = 8
    assert config.glyph_pad_index == 3

    with pytest.raises(ValueError):
        config.glyph_pad = 16


def test_scan_unit_1():
    config = PcfFontConfig(scan_unit_index=-1)
    config.scan_unit_index = 0
    assert config.scan_unit == 1
    config.scan_unit_index = 1
    assert config.scan_unit == 2
    config.scan_unit_index = 2
    assert config.scan_unit == 4

    config.scan_unit_index = 3
    with pytest.raises(IndexError):
        _ = config.scan_unit


def test_scan_unit_2():
    config = PcfFontConfig(scan_unit_index=-1)
    config.scan_unit = 1
    assert config.scan_unit_index == 0
    config.scan_unit = 2
    assert config.scan_unit_index == 1
    config.scan_unit = 4
    assert config.scan_unit_index == 2

    with pytest.raises(ValueError):
        config.scan_unit = 8


def test_copy():
    config_1 = PcfFontConfig(
        font_ascent=1,
        font_descent=2,
        default_char=3,
        draw_right_to_left=True,
        ms_byte_first=True,
        ms_bit_first=True,
        glyph_pad_index=1,
        scan_unit_index=2,
    )
    config_2 = copy(config_1)
    config_3 = deepcopy(config_1)

    assert config_1 == config_2
    assert config_1 == config_3
    assert config_1 is not config_2
    assert config_1 is not config_3


def test_eq():
    config_1 = PcfFontConfig(
        font_ascent=1,
        font_descent=2,
        default_char=3,
        draw_right_to_left=True,
        ms_byte_first=True,
        ms_bit_first=True,
        glyph_pad_index=1,
        scan_unit_index=2,
    )
    config_2 = PcfFontConfig(
        font_ascent=1,
        font_descent=2,
        default_char=3,
        draw_right_to_left=True,
        ms_byte_first=True,
        ms_bit_first=True,
        glyph_pad_index=1,
        scan_unit_index=2,
    )
    assert config_1 == config_2
