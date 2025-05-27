from __future__ import annotations

import os
from collections import UserList
from typing import Any, TYPE_CHECKING

from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.table import PcfTable
from pcffont.utils.stream import Stream

if TYPE_CHECKING:
    from pcffont.font import PcfFont


class PcfGlyphNames(UserList[str], PcfTable):
    @staticmethod
    def parse(stream: Stream, header: PcfHeader, font: PcfFont) -> PcfGlyphNames:
        table_format = header.read_and_check_table_format(stream)

        glyphs_count = stream.read_uint32(table_format.ms_byte_first)
        name_offsets = [stream.read_uint32(table_format.ms_byte_first) for _ in range(glyphs_count)]
        stream.seek(4, os.SEEK_CUR)  # strings_size
        strings_start = stream.tell()

        names = []
        for name_offset in name_offsets:
            stream.seek(strings_start + name_offset)
            name = stream.read_string()
            names.append(name)

        return PcfGlyphNames(table_format, names)

    table_format: PcfTableFormat

    def __init__(
            self,
            table_format: PcfTableFormat | None = None,
            names: list[str] | None = None,
    ):
        super().__init__(names)
        self.table_format = PcfTableFormat() if table_format is None else table_format

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfGlyphNames):
            return NotImplemented
        return (self.table_format == other.table_format and
                super().__eq__(other))

    def dump(self, stream: Stream, table_offset: int, font: PcfFont) -> int:
        glyphs_count = len(self)

        strings_start = table_offset + 4 + 4 + 4 * glyphs_count + 4
        strings_size = 0
        name_offsets = []
        stream.seek(strings_start)
        for name in self:
            name_offsets.append(strings_size)
            strings_size += stream.write_string(name)

        stream.seek(table_offset)
        stream.write_uint32(self.table_format.value)
        stream.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        for name_offset in name_offsets:
            stream.write_uint32(name_offset, self.table_format.ms_byte_first)
        stream.write_uint32(strings_size, self.table_format.ms_byte_first)
        stream.seek(strings_size, os.SEEK_CUR)
        stream.align_to_4_byte_with_nulls()

        table_size = stream.tell() - table_offset
        return table_size
