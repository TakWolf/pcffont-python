import re
from pathlib import Path

from bdffont import BdfFont

from pcffont import PcfFont


def test_demo(assets_dir: Path):
    bdf_font = BdfFont.load(assets_dir.joinpath('demo', 'demo.bdf'))
    pcf_font_0 = PcfFont.load(assets_dir.joinpath('demo', 'demo.pcf'))

    pcf_file_paths = []
    for file_path in assets_dir.joinpath('demo').iterdir():
        if re.match(r'^demo-(lsbyte|msbyte)-(lsbit|msbit)-p([1248])-u([124])\.pcf$', file_path.name) is None:
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
