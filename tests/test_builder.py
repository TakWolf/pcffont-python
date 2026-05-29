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
    pcf_font = PcfFont.load(assets_dir.joinpath('unifont', 'unifont-17.0.04.pcf'))
    pcf_font.accelerators._compat_info = None
    pcf_font.bdf_accelerators._compat_info = None
    pcf_font.bitmaps._compat_info = None
    bdf_font = _load_pcf_by_bdf(assets_dir.joinpath('unifont', 'unifont-17.0.04.bdf'))

    assert pcf_font.bdf_encodings == bdf_font.bdf_encodings
    assert pcf_font.glyph_names == bdf_font.glyph_names
    assert pcf_font.scalable_widths == bdf_font.scalable_widths
    assert pcf_font.metrics == bdf_font.metrics
    assert pcf_font.ink_metrics == bdf_font.ink_metrics
    assert pcf_font.bitmaps == bdf_font.bitmaps
    assert pcf_font.accelerators == bdf_font.accelerators
    assert pcf_font.bdf_accelerators == bdf_font.bdf_accelerators
    assert pcf_font.properties.font.upper() == bdf_font.properties.font.upper().replace('-SANS SERIF', '-SANS')


def test_demo(assets_dir: Path):
    pcf_font = PcfFont.load(assets_dir.joinpath('demo', 'demo.pcf'))
    pcf_font.accelerators._compat_info = None
    pcf_font.bdf_accelerators._compat_info = None
    pcf_font.bitmaps._compat_info = None
    bdf_font = _load_pcf_by_bdf(assets_dir.joinpath('demo', 'demo.bdf'))

    assert pcf_font.bdf_encodings == bdf_font.bdf_encodings
    assert pcf_font.glyph_names == bdf_font.glyph_names
    assert pcf_font.scalable_widths == bdf_font.scalable_widths
    assert pcf_font.metrics == bdf_font.metrics
    assert pcf_font.ink_metrics == bdf_font.ink_metrics
    assert pcf_font.bitmaps == bdf_font.bitmaps
    assert pcf_font.accelerators == bdf_font.accelerators
    assert pcf_font.bdf_accelerators == bdf_font.bdf_accelerators
    assert pcf_font.properties.font == bdf_font.properties.font


def test_demo_2(assets_dir: Path):
    pcf_font = PcfFont.load(assets_dir.joinpath('demo', 'demo-2.pcf'))
    pcf_font.accelerators._compat_info = None
    pcf_font.bdf_accelerators._compat_info = None
    pcf_font.bitmaps._compat_info = None
    bdf_font = _load_pcf_by_bdf(assets_dir.joinpath('demo', 'demo-2.bdf'))

    assert pcf_font.bdf_encodings == bdf_font.bdf_encodings
    assert pcf_font.glyph_names == bdf_font.glyph_names
    assert pcf_font.scalable_widths == bdf_font.scalable_widths
    assert pcf_font.metrics == bdf_font.metrics
    assert pcf_font.ink_metrics == bdf_font.ink_metrics
    assert pcf_font.bitmaps == bdf_font.bitmaps
    assert pcf_font.accelerators == bdf_font.accelerators
    assert pcf_font.bdf_accelerators == bdf_font.bdf_accelerators
    assert pcf_font.properties.font == bdf_font.properties.font
