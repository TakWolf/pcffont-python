from __future__ import annotations

from enum import IntFlag, unique
from typing import Final, Literal, get_args

GlyphPad = Literal[1, 2, 4, 8]
ScanUnit = Literal[1, 2, 4]

GLYPH_PAD_OPTIONS: Final[tuple[GlyphPad]] = get_args(GlyphPad)
SCAN_UNIT_OPTIONS: Final[tuple[ScanUnit]] = get_args(ScanUnit)

_GLYPH_PAD_MASK = 0b_00_00_11
_SCAN_UNIT_MASK = 0b_11_00_00


@unique
class PcfTableFormat(IntFlag):
    DEFAULT = 0
    MS_BYTE_FIRST = 0b_01_00
    MS_BIT_FIRST = 0b_10_00
    INK_BOUNDS_OR_COMPRESSED_METRICS = 0b_01_0000_0000

    @staticmethod
    def create(
            ms_byte_first: bool = False,
            ms_bit_first: bool = False,
            ink_bounds_or_compressed_metrics: bool = False,
            glyph_pad: GlyphPad = 1,
            scan_unit: ScanUnit = 1,
    ) -> PcfTableFormat:
        """
        :param ms_byte_first:
            If true, sets the font byte order to MSB first.
            All multi-bytes data in the file (metrics, bitmaps and everything else) will be written most significant
            byte first.
        :param ms_bit_first:
            If true, sets the font bit order to MSB first.
            Bits for each glyph will be placed in this order; i.e., the left most bit on the screen will be in the
            highest valued bit in each unit.
        :param ink_bounds_or_compressed_metrics:
            If true, the `PcfAccelerators` will include the `ink_min_bounds` and `ink_max_bounds` fields,
            or the `PcfMetrics` will be compressed.
        :param glyph_pad:
            The font glyph padding. Each glyph in the font will have each scanline padded in to a multiple of n bytes.
        :param scan_unit:
            The font scanline unit. When the font bit order is different from the font byte order, the scanline unit
            n describes what unit of data (in bytes) are to be swapped.
        """
        return PcfTableFormat.DEFAULT.replace(
            ms_byte_first,
            ms_bit_first,
            ink_bounds_or_compressed_metrics,
            glyph_pad,
            scan_unit,
        )

    @property
    def ms_byte_first(self) -> bool:
        return bool(self.value & PcfTableFormat.MS_BYTE_FIRST.value)

    @property
    def ms_bit_first(self) -> bool:
        return bool(self.value & PcfTableFormat.MS_BIT_FIRST.value)

    @property
    def ink_bounds(self) -> bool:
        return bool(self.value & PcfTableFormat.INK_BOUNDS_OR_COMPRESSED_METRICS.value)

    @property
    def compressed_metrics(self) -> bool:
        return self.ink_bounds

    @property
    def glyph_pad_index(self) -> int:
        return self.value & _GLYPH_PAD_MASK

    @property
    def glyph_pad(self) -> GlyphPad:
        return GLYPH_PAD_OPTIONS[self.glyph_pad_index]

    @property
    def scan_unit_index(self) -> int:
        return (self.value & _SCAN_UNIT_MASK) >> 4

    @property
    def scan_unit(self) -> ScanUnit:
        return SCAN_UNIT_OPTIONS[self.scan_unit_index]

    def replace(
            self,
            ms_byte_first: bool | None = None,
            ms_bit_first: bool | None = None,
            ink_bounds_or_compressed_metrics: bool | None = None,
            glyph_pad: GlyphPad | None = None,
            scan_unit: ScanUnit | None = None,
    ) -> PcfTableFormat:
        value = self.value
        if ms_byte_first is not None:
            value = value | PcfTableFormat.MS_BYTE_FIRST.value if ms_byte_first else value & ~PcfTableFormat.MS_BYTE_FIRST.value
        if ms_bit_first is not None:
            value = value | PcfTableFormat.MS_BIT_FIRST.value if ms_bit_first else value & ~PcfTableFormat.MS_BIT_FIRST.value
        if ink_bounds_or_compressed_metrics is not None:
            value = value | PcfTableFormat.INK_BOUNDS_OR_COMPRESSED_METRICS.value if ink_bounds_or_compressed_metrics else value & ~PcfTableFormat.INK_BOUNDS_OR_COMPRESSED_METRICS.value
        if glyph_pad is not None:
            value = (value & ~_GLYPH_PAD_MASK) | GLYPH_PAD_OPTIONS.index(glyph_pad)
        if scan_unit is not None:
            value = (value & ~_SCAN_UNIT_MASK) | (SCAN_UNIT_OPTIONS.index(scan_unit) << 4)
        return PcfTableFormat(value)
