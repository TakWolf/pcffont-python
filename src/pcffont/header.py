from __future__ import annotations

from enum import IntEnum
from typing import Any

from pcffont.error import PcfParseError
from pcffont.format import PcfTableFormat
from pcffont.utils.stream import Stream

_FILE_VERSION = b'\x01fcp'


class PcfTableType(IntEnum):
    PROPERTIES = 1 << 0
    ACCELERATORS = 1 << 1
    METRICS = 1 << 2
    BITMAPS = 1 << 3
    INK_METRICS = 1 << 4
    BDF_ENCODINGS = 1 << 5
    SCALABLE_WIDTHS = 1 << 6
    GLYPH_NAMES = 1 << 7
    BDF_ACCELERATORS = 1 << 8


class PcfHeader:
    @staticmethod
    def parse(stream: Stream) -> list[PcfHeader]:
        stream.seek(0)
        if stream.read(4) != _FILE_VERSION:
            raise PcfParseError('data format not support')

        headers = {}
        tables_count = stream.read_uint32()
        for _ in range(tables_count):
            table_type = PcfTableType(stream.read_uint32())
            if table_type in headers:
                raise PcfParseError(f"duplicate table '{table_type.name}'")
            table_format = PcfTableFormat.parse(stream.read_uint32())
            table_size = stream.read_uint32()
            table_offset = stream.read_uint32()
            headers[table_type] = PcfHeader(table_type, table_format, table_size, table_offset)
        headers = [header for _, header in sorted(headers.items())]
        return headers

    @staticmethod
    def dump(stream: Stream, headers: list[PcfHeader]):
        stream.seek(0)
        stream.write(_FILE_VERSION)

        stream.write_uint32(len(headers))
        for header in headers:
            stream.write_uint32(header.table_type)
            stream.write_uint32(header.table_format.value)
            stream.write_uint32(header.table_size)
            stream.write_uint32(header.table_offset)

    table_type: PcfTableType
    table_format: PcfTableFormat
    table_size: int
    table_offset: int

    def __init__(
            self,
            table_type: PcfTableType,
            table_format: PcfTableFormat,
            table_size: int,
            table_offset: int,
    ):
        self.table_type = table_type
        self.table_format = table_format
        self.table_size = table_size
        self.table_offset = table_offset

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfHeader):
            return NotImplemented
        return (self.table_type == other.table_type and
                self.table_format == other.table_format and
                self.table_size == other.table_size and
                self.table_offset == other.table_offset)

    def read_and_check_table_format(self, stream: Stream) -> PcfTableFormat:
        stream.seek(self.table_offset)
        value = stream.read_uint32()
        if value != self.table_format.value:
            raise PcfParseError(f"inconsistent table format: '{self.table_type.name}'")
        return self.table_format
