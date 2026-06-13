from copy import copy, deepcopy
from pathlib import Path

import pytest
from bdffont import BdfFont

from pcffont import PcfFont, PcfFontBuilder, PcfGlyph


@pytest.mark.parametrize(
    'font_dir, font_file_name', [
        ('demo', 'demo'),
        ('demo', 'demo-2'),
        ('unifont', 'unifont-17.0.04'),
    ],
)
def test_builder(assets_dir: Path, font_dir: str, font_file_name: str):
    font_1 = PcfFont.load(assets_dir.joinpath(font_dir, f'{font_file_name}.pcf'))
    font_2 = PcfFontBuilder.modify(font_1).build()

    bdf_font = BdfFont.load(assets_dir.joinpath(font_dir, f'{font_file_name}.bdf'))

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
            attributes=bdf_glyph.attributes,
            bitmap=bdf_glyph.bitmap,
        ))

    font_3 = builder.build()
    font_3.properties = font_1.properties

    assert font_1.dump_to_bytes() == font_2.dump_to_bytes() == font_3.dump_to_bytes()


def test_copy(assets_dir: Path):
    builder_1 = PcfFontBuilder.modify(PcfFont.load(assets_dir.joinpath('demo', 'demo.pcf')))
    builder_2 = copy(builder_1)

    assert builder_1 == builder_2
    assert builder_1 is not builder_2
    assert builder_1.config is builder_2.config
    assert builder_1.properties is builder_2.properties
    assert builder_1.glyphs is builder_2.glyphs


def test_deepcopy(assets_dir: Path):
    builder_1 = PcfFontBuilder.modify(PcfFont.load(assets_dir.joinpath('demo', 'demo.pcf')))
    builder_2 = deepcopy(builder_1)

    assert builder_1 == builder_2
    assert builder_1 is not builder_2
    assert builder_1.config is not builder_2.config
    assert builder_1.properties is not builder_2.properties
    assert builder_1.glyphs is not builder_2.glyphs

    for glyph_1, glyph_2 in zip(builder_1.glyphs, builder_2.glyphs):
        assert glyph_1 is not glyph_2


def test_eq(assets_dir: Path):
    file_path = assets_dir.joinpath('demo', 'demo.pcf')
    builder_1 = PcfFontBuilder.modify(PcfFont.load(file_path))
    builder_2 = PcfFontBuilder.modify(PcfFont.load(file_path))
    assert builder_1 == builder_2
