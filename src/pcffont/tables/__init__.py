from typing import Final

from pcffont.header import PcfTableType
from pcffont.tables.accelerators import PcfAccelerators
from pcffont.tables.bitmaps import PcfBitmaps
from pcffont.tables.encodings import PcfBdfEncodings
from pcffont.tables.glyph_names import PcfGlyphNames
from pcffont.tables.metrics import PcfMetrics
from pcffont.tables.properties import PcfProperties
from pcffont.tables.scalable_widths import PcfScalableWidths

TABLE_TYPE_REGISTRY: Final = {
    PcfTableType.PROPERTIES: PcfProperties,
    PcfTableType.ACCELERATORS: PcfAccelerators,
    PcfTableType.METRICS: PcfMetrics,
    PcfTableType.BITMAPS: PcfBitmaps,
    PcfTableType.INK_METRICS: PcfMetrics,
    PcfTableType.BDF_ENCODINGS: PcfBdfEncodings,
    PcfTableType.SCALABLE_WIDTHS: PcfScalableWidths,
    PcfTableType.GLYPH_NAMES: PcfGlyphNames,
    PcfTableType.BDF_ACCELERATORS: PcfAccelerators,
}
