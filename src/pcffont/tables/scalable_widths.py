from collections import UserList
from typing import Any

from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.table import PcfTableContainer, PcfTable
from pcffont.utils.stream import Stream


class PcfScalableWidths(UserList[int], PcfTable):
    @staticmethod
    def parse(stream: Stream, header: PcfHeader, container: PcfTableContainer) -> 'PcfScalableWidths':
        table_format = header.read_and_check_table_format(stream)

        glyphs_count = stream.read_uint32(table_format.ms_byte_first)

        scalable_widths = [stream.read_int32(table_format.ms_byte_first) for _ in range(glyphs_count)]

        return PcfScalableWidths(table_format, scalable_widths)

    table_format: PcfTableFormat

    def __init__(
            self,
            table_format: PcfTableFormat | None = None,
            scalable_widths: list[int] | None = None,
    ):
        super().__init__(scalable_widths)
        self.table_format = PcfTableFormat() if table_format is None else table_format

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfScalableWidths):
            return False
        return (self.table_format == other.table_format and
                super().__eq__(other))

    def dump(self, stream: Stream, table_offset: int, container: PcfTableContainer) -> int:
        glyphs_count = len(self)

        stream.seek(table_offset)
        stream.write_uint32(self.table_format.value)
        stream.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        for scalable_width in self:
            stream.write_int32(scalable_width, self.table_format.ms_byte_first)
        stream.align_to_4_byte_with_nulls()

        table_size = stream.tell() - table_offset
        return table_size
