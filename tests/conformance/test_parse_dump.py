from pathlib import Path

import pytest

from pcffont import PcfFont


@pytest.mark.parametrize(
    'font_dir, font_file_name', [
        ('demo', 'demo.pcf'),
        ('demo', 'demo-lsbyte-lsbit-p1-u1.pcf'),
        ('demo', 'demo-lsbyte-lsbit-p1-u2.pcf'),
        ('demo', 'demo-lsbyte-lsbit-p1-u4.pcf'),
        ('demo', 'demo-lsbyte-lsbit-p2-u1.pcf'),
        ('demo', 'demo-lsbyte-lsbit-p2-u2.pcf'),
        ('demo', 'demo-lsbyte-lsbit-p2-u4.pcf'),
        ('demo', 'demo-lsbyte-lsbit-p4-u1.pcf'),
        ('demo', 'demo-lsbyte-lsbit-p4-u2.pcf'),
        ('demo', 'demo-lsbyte-lsbit-p4-u4.pcf'),
        ('demo', 'demo-lsbyte-msbit-p1-u1.pcf'),
        ('demo', 'demo-lsbyte-msbit-p1-u2.pcf'),
        ('demo', 'demo-lsbyte-msbit-p1-u4.pcf'),
        ('demo', 'demo-lsbyte-msbit-p2-u1.pcf'),
        ('demo', 'demo-lsbyte-msbit-p2-u2.pcf'),
        ('demo', 'demo-lsbyte-msbit-p2-u4.pcf'),
        ('demo', 'demo-lsbyte-msbit-p4-u1.pcf'),
        ('demo', 'demo-lsbyte-msbit-p4-u2.pcf'),
        ('demo', 'demo-lsbyte-msbit-p4-u4.pcf'),
        ('demo', 'demo-msbyte-lsbit-p1-u1.pcf'),
        ('demo', 'demo-msbyte-lsbit-p1-u2.pcf'),
        ('demo', 'demo-msbyte-lsbit-p1-u4.pcf'),
        ('demo', 'demo-msbyte-lsbit-p2-u1.pcf'),
        ('demo', 'demo-msbyte-lsbit-p2-u2.pcf'),
        ('demo', 'demo-msbyte-lsbit-p2-u4.pcf'),
        ('demo', 'demo-msbyte-lsbit-p4-u1.pcf'),
        ('demo', 'demo-msbyte-lsbit-p4-u2.pcf'),
        ('demo', 'demo-msbyte-lsbit-p4-u4.pcf'),
        ('demo', 'demo-msbyte-msbit-p1-u1.pcf'),
        ('demo', 'demo-msbyte-msbit-p1-u2.pcf'),
        ('demo', 'demo-msbyte-msbit-p1-u4.pcf'),
        ('demo', 'demo-msbyte-msbit-p2-u1.pcf'),
        ('demo', 'demo-msbyte-msbit-p2-u2.pcf'),
        ('demo', 'demo-msbyte-msbit-p2-u4.pcf'),
        ('demo', 'demo-msbyte-msbit-p4-u1.pcf'),
        ('demo', 'demo-msbyte-msbit-p4-u2.pcf'),
        ('demo', 'demo-msbyte-msbit-p4-u4.pcf'),
        ('demo', 'demo-2.pcf'),
        ('spleen', 'spleen-5x8.pcf'),
        ('spleen', 'spleen-6x12.pcf'),
        ('spleen', 'spleen-8x16.pcf'),
        ('spleen', 'spleen-12x24.pcf'),
        ('spleen', 'spleen-16x32.pcf'),
        ('spleen', 'spleen-32x64.pcf'),
        ('unifont', 'unifont-17.0.05.pcf'),
    ],
)
def test_parse_dump(assets_dir: Path, font_dir: str, font_file_name: str):
    data = assets_dir.joinpath(font_dir, font_file_name).read_bytes()
    font = PcfFont.parse(data)
    assert font.dump_to_bytes() == data
