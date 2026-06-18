from __future__ import annotations

from collections import UserList
from collections.abc import Iterable
from typing import Any, TYPE_CHECKING

from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.table import PcfTable
from pcffont.utils.stream import Stream

if TYPE_CHECKING:
    from pcffont.font import PcfFont


class PcfScalableWidths(UserList[int], PcfTable):
    @staticmethod
    def parse(stream: Stream, header: PcfHeader, font: PcfFont) -> PcfScalableWidths:
        table_format = header.read_and_check_table_format(stream)

        glyphs_count = stream.read_uint32(table_format.ms_byte_first)
        scalable_widths = stream.read_int32_list(glyphs_count, table_format.ms_byte_first)

        return PcfScalableWidths(scalable_widths, table_format)

    table_format: PcfTableFormat

    def __init__(
            self,
            scalable_widths: Iterable[int] | None = None,
            table_format: PcfTableFormat = PcfTableFormat.DEFAULT,
    ):
        super().__init__(scalable_widths)
        self.table_format = table_format

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __copy__(self) -> PcfScalableWidths:
        return self.copy()

    def __deepcopy__(self, memo: dict[int, Any]) -> PcfScalableWidths:
        return self.deepcopy()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfScalableWidths):
            return NotImplemented
        return (self.table_format == other.table_format and
                super().__eq__(other))

    def dump(self, stream: Stream, table_offset: int, font: PcfFont) -> int:
        glyphs_count = len(self)

        stream.seek(table_offset)
        stream.write_uint32(self.table_format)
        stream.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        stream.write_int32_list(self.data, self.table_format.ms_byte_first)
        stream.align_to_4_bytes()

        table_size = stream.tell() - table_offset
        return table_size

    def copy(self) -> PcfScalableWidths:
        return PcfScalableWidths(self.data, self.table_format)

    def deepcopy(self) -> PcfScalableWidths:
        return self.copy()
