from __future__ import annotations

import math
import os
from collections import UserList
from typing import Any, TYPE_CHECKING

from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.table import PcfTable
from pcffont.utils.stream import Stream

if TYPE_CHECKING:
    from pcffont.font import PcfFont

_GLYPH_PAD_OPTIONS = [1, 2, 4, 8]
_SCAN_UNIT_OPTIONS = [1, 2, 4, 8]


def _swap_fragments(fragments: list[list[int]], scan_unit: int):
    if scan_unit == 2:
        for i in range(0, len(fragments), 2):
            fragments[i], fragments[i + 1] = fragments[i + 1], fragments[i]
    elif scan_unit == 4:
        for i in range(0, len(fragments), 4):
            fragments[i], fragments[i + 1], fragments[i + 2], fragments[i + 3] = fragments[i + 3], fragments[i + 2], fragments[i + 1], fragments[i]


class PcfBitmaps(UserList[list[list[int]]], PcfTable):
    @staticmethod
    def parse(stream: Stream, header: PcfHeader, font: PcfFont) -> PcfBitmaps:
        table_format = header.read_and_check_table_format(stream)

        glyph_pad = _GLYPH_PAD_OPTIONS[table_format.glyph_pad_index]
        scan_unit = _SCAN_UNIT_OPTIONS[table_format.scan_unit_index]

        glyphs_count = stream.read_uint32(table_format.ms_byte_first)
        bitmap_offsets = [stream.read_uint32(table_format.ms_byte_first) for _ in range(glyphs_count)]
        bitmaps_size_configs = [stream.read_uint32(table_format.ms_byte_first) for _ in range(4)]
        bitmaps_start = stream.tell()

        bitmaps = []
        for bitmap_offset, metric in zip(bitmap_offsets, font.metrics):
            stream.seek(bitmaps_start + bitmap_offset)
            glyph_row_pad = math.ceil(metric.width / (glyph_pad * 8)) * glyph_pad

            fragments = [stream.read_binary(table_format.ms_bit_first) for _ in range(glyph_row_pad * metric.height)]
            if table_format.ms_byte_first != table_format.ms_bit_first:
                _swap_fragments(fragments, scan_unit)

            bitmap = []
            for y in range(metric.height):
                bitmap_row = []
                for i in range(glyph_row_pad):
                    bitmap_row.extend(fragments[glyph_row_pad * y + i])
                bitmap_row = bitmap_row[:metric.width]
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
        glyph_pad = _GLYPH_PAD_OPTIONS[self.table_format.glyph_pad_index]
        scan_unit = _SCAN_UNIT_OPTIONS[self.table_format.scan_unit_index]

        glyphs_count = len(self)

        bitmaps_start = table_offset + 4 + 4 + 4 * glyphs_count + 4 * 4
        bitmaps_size = 0
        bitmap_offsets = []
        stream.seek(bitmaps_start)
        for bitmap, metric in zip(self, font.metrics):
            bitmap_offsets.append(bitmaps_size)
            bitmap_row_width = math.ceil(metric.width / (glyph_pad * 8)) * glyph_pad * 8

            fragments = []
            for bitmap_row in bitmap:
                if len(bitmap_row) < bitmap_row_width:
                    bitmap_row = bitmap_row + [0] * (bitmap_row_width - len(bitmap_row))
                elif len(bitmap_row) > bitmap_row_width:
                    bitmap_row = bitmap_row[:bitmap_row_width]
                for i in range(0, bitmap_row_width, 8):
                    fragments.append(bitmap_row[i:i + 8])

            if self.table_format.ms_byte_first != self.table_format.ms_bit_first:
                _swap_fragments(fragments, scan_unit)

            for fragment in fragments:
                bitmaps_size += stream.write_binary(fragment, self.table_format.ms_bit_first)

        # Compat
        if self._compat_info is not None:
            bitmaps_size_configs = list(self._compat_info)
            bitmaps_size_configs[self.table_format.glyph_pad_index] = bitmaps_size
        else:
            bitmaps_size_configs = [bitmaps_size // glyph_pad * glyph_pad_option for glyph_pad_option in _GLYPH_PAD_OPTIONS]

        stream.seek(table_offset)
        stream.write_uint32(self.table_format.value)
        stream.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        for bitmap_offset in bitmap_offsets:
            stream.write_uint32(bitmap_offset, self.table_format.ms_byte_first)
        for bitmaps_size_config in bitmaps_size_configs:
            stream.write_uint32(bitmaps_size_config, self.table_format.ms_byte_first)
        stream.seek(bitmaps_size, os.SEEK_CUR)
        stream.align_to_4_byte_with_nulls()

        table_size = stream.tell() - table_offset
        return table_size
