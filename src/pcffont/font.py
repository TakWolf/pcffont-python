from __future__ import annotations

from collections import UserDict
from io import BytesIO
from os import PathLike
from typing import Any, BinaryIO

from pcffont.header import PcfTableType, PcfHeader
from pcffont.table import PcfTable
from pcffont.tables.accelerators import PcfAccelerators
from pcffont.tables.bitmaps import PcfBitmaps
from pcffont.tables.encodings import PcfBdfEncodings
from pcffont.tables.factory import TABLE_TYPE_REGISTRY
from pcffont.tables.glyph_names import PcfGlyphNames
from pcffont.tables.metrics import PcfMetrics
from pcffont.tables.properties import PcfProperties
from pcffont.tables.scalable_widths import PcfScalableWidths
from pcffont.utils.stream import Stream


class PcfFont(UserDict[PcfTableType, PcfTable]):
    @staticmethod
    def parse(stream: bytes | bytearray | BinaryIO) -> PcfFont:
        if isinstance(stream, (bytes, bytearray)):
            stream = BytesIO(stream)
        stream = Stream(stream)

        font = PcfFont()
        headers = PcfHeader.parse(stream)
        for header in headers:
            table = TABLE_TYPE_REGISTRY[header.table_type].parse(stream, header, font)
            font[header.table_type] = table
        return font

    @staticmethod
    def load(file_path: str | PathLike[str]) -> PcfFont:
        with open(file_path, 'rb') as file:
            return PcfFont.parse(file)

    def __setitem__(self, table_type: Any, table: Any):
        if table is None:
            self.pop(table_type, None)
            return

        if not isinstance(table_type, PcfTableType):
            raise KeyError(f"expected type 'PcfTableType', got '{type(table_type).__name__}' instead")

        if not isinstance(table, TABLE_TYPE_REGISTRY[table_type]):
            raise ValueError(f"expected type '{TABLE_TYPE_REGISTRY[table_type].__name__}', got '{type(table).__name__}' instead")

        super().__setitem__(table_type, table)

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfFont):
            return NotImplemented
        return super().__eq__(other)

    @property
    def properties(self) -> PcfProperties | None:
        return self.get(PcfTableType.PROPERTIES, None)

    @properties.setter
    def properties(self, table: PcfProperties | None):
        self[PcfTableType.PROPERTIES] = table

    @property
    def accelerators(self) -> PcfAccelerators | None:
        return self.get(PcfTableType.ACCELERATORS, None)

    @accelerators.setter
    def accelerators(self, table: PcfAccelerators | None):
        self[PcfTableType.ACCELERATORS] = table

    @property
    def metrics(self) -> PcfMetrics | None:
        return self.get(PcfTableType.METRICS, None)

    @metrics.setter
    def metrics(self, table: PcfMetrics | None):
        self[PcfTableType.METRICS] = table

    @property
    def bitmaps(self) -> PcfBitmaps | None:
        return self.get(PcfTableType.BITMAPS, None)

    @bitmaps.setter
    def bitmaps(self, table: PcfBitmaps | None):
        self[PcfTableType.BITMAPS] = table

    @property
    def ink_metrics(self) -> PcfMetrics | None:
        return self.get(PcfTableType.INK_METRICS, None)

    @ink_metrics.setter
    def ink_metrics(self, table: PcfMetrics | None):
        self[PcfTableType.INK_METRICS] = table

    @property
    def bdf_encodings(self) -> PcfBdfEncodings | None:
        return self.get(PcfTableType.BDF_ENCODINGS, None)

    @bdf_encodings.setter
    def bdf_encodings(self, table: PcfBdfEncodings | None):
        self[PcfTableType.BDF_ENCODINGS] = table

    @property
    def scalable_widths(self) -> PcfScalableWidths | None:
        return self.get(PcfTableType.SCALABLE_WIDTHS, None)

    @scalable_widths.setter
    def scalable_widths(self, table: PcfScalableWidths | None):
        self[PcfTableType.SCALABLE_WIDTHS] = table

    @property
    def glyph_names(self) -> PcfGlyphNames | None:
        return self.get(PcfTableType.GLYPH_NAMES, None)

    @glyph_names.setter
    def glyph_names(self, table: PcfGlyphNames | None):
        self[PcfTableType.GLYPH_NAMES] = table

    @property
    def bdf_accelerators(self) -> PcfAccelerators | None:
        return self.get(PcfTableType.BDF_ACCELERATORS, None)

    @bdf_accelerators.setter
    def bdf_accelerators(self, table: PcfAccelerators | None):
        self[PcfTableType.BDF_ACCELERATORS] = table

    def dump(self, stream: BinaryIO):
        stream = Stream(stream)

        headers = []
        table_offset = 4 + 4 + 4 * 4 * len(self)
        for table_type, table in sorted(self.items()):
            table_size = table.dump(stream, table_offset, self)
            headers.append(PcfHeader(table_type, table.table_format, table_size, table_offset))
            table_offset += table_size
        PcfHeader.dump(stream, headers)

    def dump_to_bytes(self) -> bytes:
        stream = BytesIO()
        self.dump(stream)
        return stream.getvalue()

    def save(self, file_path: str | PathLike[str]):
        with open(file_path, 'wb') as file:
            self.dump(file)
