from io import BytesIO
from pathlib import Path

import freetype
import pytest
from bdffont import BdfFont

from pcffont import PcfFont, PcfFontBuilder, PcfGlyph, PcfTableFormat


@pytest.fixture(scope='module')
def demo_bdf(assets_dir: Path) -> BdfFont:
    return BdfFont.load(assets_dir.joinpath('demo', 'demo.bdf'))


@pytest.fixture(scope='module')
def demo_pcf(assets_dir: Path) -> PcfFont:
    return PcfFont.load(assets_dir.joinpath('demo', 'demo.pcf'))


@pytest.mark.parametrize(
    'font_file_name', [
        'demo-lsbyte-lsbit-p1-u1.pcf',
        'demo-lsbyte-lsbit-p1-u2.pcf',
        'demo-lsbyte-lsbit-p1-u4.pcf',
        'demo-lsbyte-lsbit-p2-u1.pcf',
        'demo-lsbyte-lsbit-p2-u2.pcf',
        'demo-lsbyte-lsbit-p2-u4.pcf',
        'demo-lsbyte-lsbit-p4-u1.pcf',
        'demo-lsbyte-lsbit-p4-u2.pcf',
        'demo-lsbyte-lsbit-p4-u4.pcf',
        'demo-lsbyte-msbit-p1-u1.pcf',
        'demo-lsbyte-msbit-p1-u2.pcf',
        'demo-lsbyte-msbit-p1-u4.pcf',
        'demo-lsbyte-msbit-p2-u1.pcf',
        'demo-lsbyte-msbit-p2-u2.pcf',
        'demo-lsbyte-msbit-p2-u4.pcf',
        'demo-lsbyte-msbit-p4-u1.pcf',
        'demo-lsbyte-msbit-p4-u2.pcf',
        'demo-lsbyte-msbit-p4-u4.pcf',
        'demo-msbyte-lsbit-p1-u1.pcf',
        'demo-msbyte-lsbit-p1-u2.pcf',
        'demo-msbyte-lsbit-p1-u4.pcf',
        'demo-msbyte-lsbit-p2-u1.pcf',
        'demo-msbyte-lsbit-p2-u2.pcf',
        'demo-msbyte-lsbit-p2-u4.pcf',
        'demo-msbyte-lsbit-p4-u1.pcf',
        'demo-msbyte-lsbit-p4-u2.pcf',
        'demo-msbyte-lsbit-p4-u4.pcf',
        'demo-msbyte-msbit-p1-u1.pcf',
        'demo-msbyte-msbit-p1-u2.pcf',
        'demo-msbyte-msbit-p1-u4.pcf',
        'demo-msbyte-msbit-p2-u1.pcf',
        'demo-msbyte-msbit-p2-u2.pcf',
        'demo-msbyte-msbit-p2-u4.pcf',
        'demo-msbyte-msbit-p4-u1.pcf',
        'demo-msbyte-msbit-p4-u2.pcf',
        'demo-msbyte-msbit-p4-u4.pcf',
    ],
)
def test_demo(demo_bdf: BdfFont, demo_pcf: PcfFont, assets_dir: Path, font_file_name: str):
    bdf_font = demo_bdf
    pcf_font_0 = demo_pcf
    pcf_font_x = PcfFont.load(assets_dir.joinpath('demo', font_file_name))

    for glyph_index, glyph in enumerate(bdf_font.glyphs):
        glyph_name_0 = pcf_font_0.glyph_names[glyph_index]
        glyph_name_x = pcf_font_x.glyph_names[glyph_index]
        assert glyph_name_x == glyph.name
        assert glyph_name_x == glyph_name_0

        metric_0 = pcf_font_0.metrics[glyph_index]
        metric_x = pcf_font_x.metrics[glyph_index]
        assert metric_x.character_width == glyph.device_width_x
        assert metric_x.dimensions == glyph.dimensions
        assert metric_x.offset == glyph.offset
        assert metric_x == metric_0

        bitmap_0 = pcf_font_0.bitmaps[glyph_index]
        bitmap_x = pcf_font_x.bitmaps[glyph_index]
        assert bitmap_x == glyph.bitmap
        assert bitmap_x == bitmap_0


def test_unifont(assets_dir: Path):
    bdf_font = BdfFont.load(assets_dir.joinpath('unifont', 'unifont-17.0.04.bdf'))
    pcf_font = PcfFont.load(assets_dir.joinpath('unifont', 'unifont-17.0.04.pcf'))

    for glyph_index, glyph in enumerate(bdf_font.glyphs):
        glyph_name = pcf_font.glyph_names[glyph_index]
        assert glyph.name == glyph_name

        metric = pcf_font.metrics[glyph_index]
        assert glyph.device_width_x == metric.character_width
        assert glyph.dimensions == metric.dimensions
        assert glyph.offset == metric.offset

        bitmap = pcf_font.bitmaps[glyph_index]
        assert glyph.bitmap == bitmap


@pytest.mark.parametrize("ms_byte_first", [False, True])
@pytest.mark.parametrize("ms_bit_first", [False, True])
@pytest.mark.parametrize('glyph_pad', PcfTableFormat.GLYPH_PAD_OPTIONS)
@pytest.mark.parametrize('scan_unit', PcfTableFormat.SCAN_UNIT_OPTIONS)
def test_with_freetype(demo_bdf: BdfFont, ms_byte_first: bool, ms_bit_first: bool, glyph_pad: int, scan_unit: int):
    builder = PcfFontBuilder()
    builder.config.font_ascent = demo_bdf.properties.font_ascent
    builder.config.font_descent = demo_bdf.properties.font_descent
    builder.config.ms_byte_first = ms_byte_first
    builder.config.ms_bit_first = ms_bit_first
    builder.config.glyph_pad = glyph_pad
    builder.config.scan_unit = scan_unit

    for bdf_glyph in demo_bdf.glyphs[:10]:
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

    builder.properties.update(demo_bdf.properties)
    builder.properties.generate_xlfd()

    pcf_font = builder.build()
    stream = BytesIO()
    pcf_font.dump(stream)
    stream.seek(0)
    ft_font = freetype.Face(stream)

    pcf_glyph_index_to_encoding = {glyph_index: encoding for encoding, glyph_index in pcf_font.bdf_encodings.items()}
    for pcf_glyph_index, pcf_glyph_name in enumerate(pcf_font.glyph_names):
        encoding = pcf_glyph_index_to_encoding[pcf_glyph_index]
        ft_glyph_index = ft_font.get_char_index(encoding)
        assert ft_glyph_index == pcf_glyph_index + 1

        ft_font.load_glyph(ft_glyph_index)
        ft_bitmap = ft_font.glyph.bitmap

        pcf_bitmap = pcf_font.bitmaps[pcf_glyph_index]
        pcf_metric = pcf_font.metrics[pcf_glyph_index]

        assert ft_bitmap.width == len(pcf_bitmap[0])
        assert ft_bitmap.width == pcf_metric.width
        assert ft_bitmap.rows == len(pcf_bitmap)
        assert ft_bitmap.rows == pcf_metric.height

        for y in range(ft_bitmap.rows):
            ft_bitmap_row = [
                (ft_bitmap.buffer[y * ft_bitmap.pitch + x // 8] >> (7 - x % 8)) & 1
                for x in range(ft_bitmap.width)
            ]
            pcf_bitmap_row = pcf_bitmap[y]
            assert ft_bitmap_row == pcf_bitmap_row

        pcf_bitmap_row_size = (pcf_metric.width + glyph_pad * 8 - 1) // (glyph_pad * 8) * glyph_pad
        assert ft_bitmap.pitch == pcf_bitmap_row_size
        pcf_bitmap_size = pcf_bitmap_row_size * pcf_metric.height
        assert len(ft_bitmap.buffer) == pcf_bitmap_size
