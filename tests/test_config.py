from copy import copy, deepcopy

from pcffont import PcfFontConfig, PcfTableFormat


def test_to_table_format():
    assert PcfFontConfig().to_table_format() == PcfTableFormat.DEFAULT
    assert PcfFontConfig(
        ms_byte_first=True,
        ms_bit_first=True,
        glyph_pad=2,
        scan_unit=4,
    ).to_table_format() == PcfTableFormat.of(
        ms_byte_first=True,
        ms_bit_first=True,
        glyph_pad=2,
        scan_unit=4,
    )


def test_copy():
    config_1 = PcfFontConfig(
        font_ascent=1,
        font_descent=2,
        default_char=3,
        draw_right_to_left=True,
        ms_byte_first=True,
        ms_bit_first=True,
        glyph_pad=2,
        scan_unit=4,
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
        glyph_pad=2,
        scan_unit=4,
    )
    config_2 = PcfFontConfig(
        font_ascent=1,
        font_descent=2,
        default_char=3,
        draw_right_to_left=True,
        ms_byte_first=True,
        ms_bit_first=True,
        glyph_pad=2,
        scan_unit=4,
    )
    assert config_1 == config_2
