from copy import copy, deepcopy
from pathlib import Path

from pcffont import PcfFont


def test_copy(assets_dir: Path):
    font_1 = PcfFont.load(assets_dir.joinpath('demo', 'demo.pcf'))
    font_2 = copy(font_1)

    assert font_1 == font_2
    assert font_1 is not font_2
    assert font_1.properties is font_2.properties
    assert font_1.accelerators is font_2.accelerators
    assert font_1.metrics is font_2.metrics
    assert font_1.bitmaps is font_2.bitmaps
    assert font_1.ink_metrics is font_2.ink_metrics
    assert font_1.bdf_encodings is font_2.bdf_encodings
    assert font_1.scalable_widths is font_2.scalable_widths
    assert font_1.glyph_names is font_2.glyph_names
    assert font_1.bdf_accelerators is font_2.bdf_accelerators


def test_deepcopy(assets_dir: Path):
    font_1 = PcfFont.load(assets_dir.joinpath('demo', 'demo.pcf'))
    font_2 = deepcopy(font_1)

    assert font_1 == font_2
    assert font_1 is not font_2
    assert font_1.properties is not font_2.properties
    assert font_1.accelerators is not font_2.accelerators
    assert font_1.metrics is not font_2.metrics
    assert font_1.bitmaps is not font_2.bitmaps
    assert font_1.ink_metrics is not font_2.ink_metrics
    assert font_1.bdf_encodings is not font_2.bdf_encodings
    assert font_1.scalable_widths is not font_2.scalable_widths
    assert font_1.glyph_names is not font_2.glyph_names
    assert font_1.bdf_accelerators is not font_2.bdf_accelerators


def test_eq(assets_dir: Path):
    file_path = assets_dir.joinpath('demo', 'demo.pcf')
    font_1 = PcfFont.load(file_path)
    font_2 = PcfFont.load(file_path)
    assert font_1 == font_2
