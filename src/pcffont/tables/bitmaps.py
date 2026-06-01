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


def _swap_bytes(data: bytearray, scan_unit: int):
    if scan_unit <= 1:
        return

    for i in range(0, len(data) // scan_unit * scan_unit, scan_unit):
        for j in range(scan_unit // 2):
            left = i + j
            right = i + scan_unit - 1 - j
            data[left], data[right] = data[right], data[left]


class PcfBitmaps(UserList[list[list[int]]], PcfTable):
    @staticmethod
    def parse(stream: Stream, header: PcfHeader, font: PcfFont) -> PcfBitmaps:
        table_format = header.read_and_check_table_format(stream)

        glyphs_count = stream.read_uint32(table_format.ms_byte_first)
        bitmap_offsets = stream.read_uint32_list(glyphs_count, table_format.ms_byte_first)
        bitmaps_size_configs = stream.read_uint32_list(4, table_format.ms_byte_first)
        bitmaps_start = stream.tell()

        bitmaps = []
        for bitmap_offset, metric in zip(bitmap_offsets, font.metrics):
            bitmap_row_size = (metric.width + table_format.glyph_pad * 8 - 1) // (table_format.glyph_pad * 8) * table_format.glyph_pad

            stream.seek(bitmaps_start + bitmap_offset)
            bitmap_data = bytearray(stream.read(bitmap_row_size * metric.height))

            if table_format.ms_byte_first != table_format.ms_bit_first:
                _swap_bytes(bitmap_data, table_format.scan_unit)

            bitmap = []
            for y in range(metric.height):
                bitmap_row = []
                for i in range(bitmap_row_size):
                    b = bitmap_data[y * bitmap_row_size + i]
                    for shift in (range(7, -1, -1) if table_format.ms_bit_first else range(8)):
                        bitmap_row.append((b >> shift) & 1)
                if len(bitmap_row) > metric.width:
                    del bitmap_row[metric.width:]
                bitmap.append(bitmap_row)
            bitmaps.append(bitmap)

        table = PcfBitmaps(table_format, bitmaps)

        # Compat
        table._compat_info = bitmaps_size_configs

        return table

    table_format: PcfTableFormat
    _compat_info: list[int] | None

    def __init__(
            self,
            table_format: PcfTableFormat | None = None,
            bitmaps: list[list[list[int]]] | None = None,
    ):
        super().__init__(bitmaps)
        self.table_format = PcfTableFormat() if table_format is None else table_format
        self._compat_info = None

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfBitmaps):
            return NotImplemented
        return (self.table_format == other.table_format and
                self._compat_info == other._compat_info and
                super().__eq__(other))

    def dump(self, stream: Stream, table_offset: int, font: PcfFont) -> int:
        glyphs_count = len(self)

        bitmaps_start = table_offset + 4 + 4 + 4 * glyphs_count + 4 * 4
        bitmaps_size = 0
        bitmap_offsets = []
        stream.seek(bitmaps_start)
        for bitmap, metric in zip(self, font.metrics):
            bitmap_row_size = (metric.width + self.table_format.glyph_pad * 8 - 1) // (self.table_format.glyph_pad * 8) * self.table_format.glyph_pad

            bitmap_data = bytearray()
            for y in range(metric.height):
                if y >= len(bitmap):
                    bitmap_data.extend(b'\x00' * bitmap_row_size)
                    continue

                bitmap_row = bitmap[y]
                for i in range(bitmap_row_size):
                    b = 0
                    for shift in (range(8) if self.table_format.ms_bit_first else range(7, -1, -1)):
                        pixel_index = i * 8 + shift
                        pixel = 1 if pixel_index < min(len(bitmap_row), metric.width) and bitmap_row[pixel_index] != 0 else 0
                        b = (b << 1) | pixel
                    bitmap_data.append(b)

            if self.table_format.ms_byte_first != self.table_format.ms_bit_first:
                _swap_bytes(bitmap_data, self.table_format.scan_unit)

            bitmap_offsets.append(bitmaps_size)
            bitmaps_size += stream.write(bitmap_data)

        # Compat
        if self._compat_info is not None:
            bitmaps_size_configs = list(self._compat_info)
            bitmaps_size_configs[self.table_format.glyph_pad_index] = bitmaps_size
        else:
            bitmaps_size_configs = [
                bitmaps_size // self.table_format.glyph_pad * glyph_pad_option
                for glyph_pad_option in PcfTableFormat.GLYPH_PAD_OPTIONS
            ]

        stream.seek(table_offset)
        stream.write_uint32(self.table_format.value)
        stream.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        stream.write_uint32_list(bitmap_offsets, self.table_format.ms_byte_first)
        stream.write_uint32_list(bitmaps_size_configs, self.table_format.ms_byte_first)
        stream.seek(bitmaps_size, os.SEEK_CUR)
        stream.align_to_4_bytes()

        table_size = stream.tell() - table_offset
        return table_size
