from pathlib import Path

from bdffont import BdfFont

from pcffont import PcfFont, PcfFontBuilder, PcfGlyph


def _create_pcf_by_bdf(file_path: Path) -> PcfFont:
    bdf_font = BdfFont.load(file_path)

    builder = PcfFontBuilder()
    builder.config.font_ascent = bdf_font.properties.font_ascent
    builder.config.font_descent = bdf_font.properties.font_descent
    if bdf_font.properties.default_char is not None:
        builder.config.default_char = bdf_font.properties.default_char
    builder.config.ms_byte_first = True
    builder.config.ms_bit_first = True
    builder.config.glyph_pad = 4

    builder.properties.update(bdf_font.properties)
    builder.properties.generate_xlfd()

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

    return builder.build()


def test_unifont(assets_dir: Path):
    pcf_path = assets_dir.joinpath('unifont', 'unifont-17.0.04.pcf')
    bdf_path = assets_dir.joinpath('unifont', 'unifont-17.0.04.bdf')

    font_1 = PcfFont.load(pcf_path)
    font_2 = _create_pcf_by_bdf(bdf_path)
    font_2.properties = font_1.properties
    assert font_1.dump_to_bytes() == font_2.dump_to_bytes()


def test_demo(assets_dir: Path):
    pcf_path = assets_dir.joinpath(assets_dir.joinpath('demo', 'demo.pcf'))
    bdf_path = assets_dir.joinpath(assets_dir.joinpath('demo', 'demo.bdf'))

    font_1 = PcfFont.load(pcf_path)
    font_2 = _create_pcf_by_bdf(bdf_path)
    font_2.properties = font_1.properties
    assert font_1.dump_to_bytes() == font_2.dump_to_bytes()


def test_demo_2(assets_dir: Path):
    pcf_path = assets_dir.joinpath(assets_dir.joinpath('demo', 'demo-2.pcf'))
    bdf_path = assets_dir.joinpath(assets_dir.joinpath('demo', 'demo-2.bdf'))

    font_1 = PcfFont.load(pcf_path)
    font_2 = _create_pcf_by_bdf(bdf_path)
    font_2.properties = font_1.properties
    assert font_1.dump_to_bytes() == font_2.dump_to_bytes()
