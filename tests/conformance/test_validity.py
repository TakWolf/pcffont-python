import re
from io import BytesIO
from pathlib import Path

import freetype
from bdffont import BdfFont

from pcffont import PcfFont, PcfFontBuilder, PcfGlyph, PcfTableFormat


def test_demo(assets_dir: Path):
    bdf_font = BdfFont.load(assets_dir.joinpath('demo', 'demo.bdf'))
    pcf_font_0 = PcfFont.load(assets_dir.joinpath('demo', 'demo.pcf'))

    pcf_file_paths = []
    regex_font_name = re.compile(r'^demo-(lsbyte|msbyte)-(lsbit|msbit)-p([1248])-u([124])\.pcf$')
    for file_path in assets_dir.joinpath('demo').iterdir():
        if regex_font_name.match(file_path.name) is None:
            continue
        pcf_file_paths.append(file_path)
    pcf_file_paths.sort()
    assert len(pcf_file_paths) == 36

    for file_path in pcf_file_paths:
        pcf_font_x = PcfFont.load(file_path)

        for glyph_index, glyph in enumerate(bdf_font.glyphs):
            glyph_name_0 = pcf_font_0.glyph_names[glyph_index]
            glyph_name_x = pcf_font_x.glyph_names[glyph_index]
            assert glyph_name_x == glyph.name, file_path
            assert glyph_name_x == glyph_name_0, file_path

            metric_0 = pcf_font_0.metrics[glyph_index]
            metric_x = pcf_font_x.metrics[glyph_index]
            assert metric_x.character_width == glyph.device_width_x, file_path
            assert metric_x.dimensions == glyph.dimensions, file_path
            assert metric_x.offset == glyph.offset, file_path
            assert metric_x == metric_0, file_path

            bitmap_0 = pcf_font_0.bitmaps[glyph_index]
            bitmap_x = pcf_font_x.bitmaps[glyph_index]
            assert bitmap_x == glyph.bitmap, file_path
            assert bitmap_x == bitmap_0, file_path


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


def test_with_freetype(assets_dir: Path):
    bdf_font = BdfFont.load(assets_dir.joinpath('demo', 'demo.bdf'))
    bdf_font.glyphs = bdf_font.glyphs[:10]

    builder = PcfFontBuilder()
    builder.config.font_ascent = bdf_font.properties.font_ascent
    builder.config.font_descent = bdf_font.properties.font_descent

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

    for ms_byte_first in (False, True):
        for ms_bit_first in (False, True):
            for glyph_pad in PcfTableFormat.GLYPH_PAD_OPTIONS:
                for scan_unit in PcfTableFormat.SCAN_UNIT_OPTIONS:
                    builder.config.ms_byte_first = ms_byte_first
                    builder.config.ms_bit_first = ms_bit_first
                    builder.config.glyph_pad = glyph_pad
                    builder.config.scan_unit = scan_unit

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
