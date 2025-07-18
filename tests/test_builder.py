from pathlib import Path

from bdffont import BdfFont

from pcffont import PcfFont, PcfFontBuilder, PcfGlyph


def _load_pcf_by_bdf(file_path: Path) -> PcfFont:
    bdf_font = BdfFont.load(file_path)

    builder = PcfFontBuilder()
    builder.config.font_ascent = bdf_font.properties.font_ascent
    builder.config.font_descent = bdf_font.properties.font_descent
    if bdf_font.properties.default_char is not None:
        builder.config.default_char = bdf_font.properties.default_char
    builder.config.ms_byte_first = True
    builder.config.ms_bit_first = True
    builder.config.glyph_pad_index = 2

    for bdf_glyph in bdf_font.glyphs:
        builder.glyphs.append(PcfGlyph(
            name=bdf_glyph.name,
            encoding=bdf_glyph.encoding,
            scalable_width=bdf_glyph.scalable_width_x,
            character_width=bdf_glyph.device_width_x,
            dimensions=bdf_glyph.dimensions,
            offset=bdf_glyph.offset,
            bitmap=bdf_glyph.bitmap,
        ))

    builder.properties.update(bdf_font.properties)
    builder.properties.generate_xlfd()

    return builder.build()


def test_unifont(assets_dir: Path):
    font_1 = PcfFont.load(assets_dir.joinpath('unifont', 'unifont-16.0.04.pcf'))
    font_1.accelerators._compat_info = None
    font_1.bdf_accelerators._compat_info = None
    font_1.bitmaps._compat_info = None
    font_2 = _load_pcf_by_bdf(assets_dir.joinpath('unifont', 'unifont-16.0.04.bdf'))

    assert font_1.bdf_encodings == font_2.bdf_encodings
    assert font_1.glyph_names == font_2.glyph_names
    assert font_1.scalable_widths == font_2.scalable_widths
    assert font_1.metrics == font_2.metrics
    assert font_1.ink_metrics == font_2.ink_metrics
    assert font_1.bitmaps == font_2.bitmaps
    assert font_1.accelerators == font_2.accelerators
    assert font_1.bdf_accelerators == font_2.bdf_accelerators
    assert font_1.properties.font.upper() == font_2.properties.font.upper().replace('-SANS SERIF', '-SANS')


def test_demo(assets_dir: Path):
    font_1 = PcfFont.load(assets_dir.joinpath('demo', 'demo.pcf'))
    font_1.accelerators._compat_info = None
    font_1.bdf_accelerators._compat_info = None
    font_1.bitmaps._compat_info = None
    font_2 = _load_pcf_by_bdf(assets_dir.joinpath('demo', 'demo.bdf'))

    assert font_1.bdf_encodings == font_2.bdf_encodings
    assert font_1.glyph_names == font_2.glyph_names
    assert font_1.scalable_widths == font_2.scalable_widths
    assert font_1.metrics == font_2.metrics
    assert font_1.ink_metrics == font_2.ink_metrics
    assert font_1.bitmaps == font_2.bitmaps
    assert font_1.accelerators == font_2.accelerators
    assert font_1.bdf_accelerators == font_2.bdf_accelerators
    assert font_1.properties.font == font_2.properties.font


def test_demo_2(assets_dir: Path):
    font_1 = PcfFont.load(assets_dir.joinpath('demo', 'demo-2.pcf'))
    font_1.accelerators._compat_info = None
    font_1.bdf_accelerators._compat_info = None
    font_1.bitmaps._compat_info = None
    font_2 = _load_pcf_by_bdf(assets_dir.joinpath('demo', 'demo-2.bdf'))

    assert font_1.bdf_encodings == font_2.bdf_encodings
    assert font_1.glyph_names == font_2.glyph_names
    assert font_1.scalable_widths == font_2.scalable_widths
    assert font_1.metrics == font_2.metrics
    assert font_1.ink_metrics == font_2.ink_metrics
    assert font_1.bitmaps == font_2.bitmaps
    assert font_1.accelerators == font_2.accelerators
    assert font_1.bdf_accelerators == font_2.bdf_accelerators
    assert font_1.properties.font == font_2.properties.font
