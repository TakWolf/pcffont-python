from pathlib import Path

from pcffont import PcfFont


def test_no_compat(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('unifont', 'unifont-16.0.04.pcf')
    save_path = tmp_path.joinpath('unifont-16.0.04.pcf')

    font_1 = PcfFont.load(load_path)
    font_1.accelerators._compat_info = None
    font_1.bdf_accelerators._compat_info = None
    font_1.bitmaps._compat_info = None
    font_1.save(save_path)

    font_2 = PcfFont.load(save_path)
    assert font_2.accelerators._compat_info is None
    assert font_2.bdf_accelerators._compat_info is None
    font_2.bitmaps._compat_info = None

    assert font_1.bdf_encodings == font_2.bdf_encodings
    assert font_1.glyph_names == font_2.glyph_names
    assert font_1.scalable_widths == font_2.scalable_widths
    assert font_1.metrics == font_2.metrics
    assert font_1.ink_metrics == font_2.ink_metrics
    assert font_1.bitmaps == font_2.bitmaps
    assert font_1.accelerators == font_2.accelerators
    assert font_1.bdf_accelerators == font_2.bdf_accelerators
    assert font_1.properties == font_2.properties
