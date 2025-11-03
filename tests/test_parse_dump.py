from pathlib import Path

from pcffont import PcfFont


def test_unifont(assets_dir: Path):
    data = assets_dir.joinpath('unifont', 'unifont-17.0.03.pcf').read_bytes()
    font = PcfFont.parse(data)
    assert font.dump_to_bytes() == data
