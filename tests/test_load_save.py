import re
from pathlib import Path

from pcffont import PcfFont


def test_unifont(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('unifont', 'unifont-17.0.04.pcf')
    save_path = tmp_path.joinpath('unifont-17.0.04.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_spleen(assets_dir: Path, tmp_path: Path):
    load_paths = []
    for load_path in assets_dir.joinpath('spleen').iterdir():
        if re.match(r'^spleen-.*\.pcf$', load_path.name) is None:
            continue
        load_paths.append(load_path)
    load_paths.sort()
    assert len(load_paths) == 6

    for load_path in load_paths:
        save_path = tmp_path.joinpath(load_path.name)
        font = PcfFont.load(load_path)
        font.save(save_path)
        assert load_path.read_bytes() == save_path.read_bytes(), load_path


def test_demo(assets_dir: Path, tmp_path: Path):
    load_paths = []
    for load_path in assets_dir.joinpath('demo').iterdir():
        if re.match(r'^demo.*\.pcf$', load_path.name) is None:
            continue
        load_paths.append(load_path)
    load_paths.sort()
    assert len(load_paths) == 38

    for load_path in load_paths:
        save_path = tmp_path.joinpath(load_path.name)
        font = PcfFont.load(load_path)
        font.save(save_path)
        assert load_path.read_bytes() == save_path.read_bytes(), load_path
