from pcffont import PcfTable, PcfProperties, PcfAccelerators, PcfMetrics, PcfBitmaps, PcfBdfEncodings, PcfScalableWidths, PcfGlyphNames


def test_isinstance():
    assert isinstance(PcfProperties(), PcfTable)
    assert isinstance(PcfAccelerators(), PcfTable)
    assert isinstance(PcfMetrics(), PcfTable)
    assert isinstance(PcfBitmaps(), PcfTable)
    assert isinstance(PcfBdfEncodings(), PcfTable)
    assert isinstance(PcfScalableWidths(), PcfTable)
    assert isinstance(PcfGlyphNames(), PcfTable)
