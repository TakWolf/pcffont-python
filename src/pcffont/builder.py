from __future__ import annotations

from os import PathLike
from typing import Any

from pcffont.font import PcfFont
from pcffont.format import PcfTableFormat, GlyphPad, ScanUnit
from pcffont.glyph import PcfGlyph
from pcffont.tables.accelerators import PcfAccelerators
from pcffont.tables.bitmaps import PcfBitmaps
from pcffont.tables.encodings import PcfBdfEncodings
from pcffont.tables.glyph_names import PcfGlyphNames
from pcffont.tables.metrics import PcfMetrics
from pcffont.tables.properties import PcfProperties
from pcffont.tables.scalable_widths import PcfScalableWidths
from pcffont.utils import calculate_util


class PcfFontConfig:
    font_ascent: int
    font_descent: int
    default_char: int
    draw_right_to_left: bool
    ms_byte_first: bool
    ms_bit_first: bool
    glyph_pad: GlyphPad
    scan_unit: ScanUnit

    def __init__(
            self,
            font_ascent: int = 0,
            font_descent: int = 0,
            default_char: int = PcfBdfEncodings.NO_ENCODING,
            draw_right_to_left: bool = False,
            ms_byte_first: bool = False,
            ms_bit_first: bool = False,
            glyph_pad: GlyphPad = 1,
            scan_unit: ScanUnit = 1,
    ):
        self.font_ascent = font_ascent
        self.font_descent = font_descent
        self.default_char = default_char
        self.draw_right_to_left = draw_right_to_left
        self.ms_byte_first = ms_byte_first
        self.ms_bit_first = ms_bit_first
        self.glyph_pad = glyph_pad
        self.scan_unit = scan_unit

    def __copy__(self) -> PcfFontConfig:
        return self.copy()

    def __deepcopy__(self, memo: dict[int, Any]) -> PcfFontConfig:
        return self.deepcopy()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PcfFontConfig):
            return NotImplemented
        return (self.font_ascent == other.font_ascent and
                self.font_descent == other.font_descent and
                self.default_char == other.default_char and
                self.draw_right_to_left == other.draw_right_to_left and
                self.ms_byte_first == other.ms_byte_first and
                self.ms_bit_first == other.ms_bit_first and
                self.glyph_pad == other.glyph_pad and
                self.scan_unit == other.scan_unit)

    def to_table_format(self) -> PcfTableFormat:
        return PcfTableFormat.create(
            ms_byte_first=self.ms_byte_first,
            ms_bit_first=self.ms_bit_first,
            glyph_pad=self.glyph_pad,
            scan_unit=self.scan_unit,
        )

    def copy(self) -> PcfFontConfig:
        return PcfFontConfig(
            self.font_ascent,
            self.font_descent,
            self.default_char,
            self.draw_right_to_left,
            self.ms_byte_first,
            self.ms_bit_first,
            self.glyph_pad,
            self.scan_unit,
        )

    def deepcopy(self) -> PcfFontConfig:
        return self.copy()


class PcfFontBuilder:
    @staticmethod
    def modify(font: PcfFont) -> PcfFontBuilder:
        builder = PcfFontBuilder()
        builder.config.font_ascent = font.accelerators.font_ascent
        builder.config.font_descent = font.accelerators.font_descent
        builder.config.default_char = font.bdf_encodings.default_char
        builder.config.draw_right_to_left = font.accelerators.draw_right_to_left
        builder.config.ms_byte_first = font.bitmaps.table_format.ms_byte_first
        builder.config.ms_bit_first = font.bitmaps.table_format.ms_bit_first
        builder.config.glyph_pad = font.bitmaps.table_format.glyph_pad
        builder.config.scan_unit = font.bitmaps.table_format.scan_unit

        builder.properties = font.properties

        glyph_index_to_encoding = {glyph_index: encoding for encoding, glyph_index in font.bdf_encodings.items()}
        for glyph_index, (glyph_name, scalable_width, metric, bitmap) in enumerate(zip(font.glyph_names, font.scalable_widths, font.metrics, font.bitmaps)):
            builder.glyphs.append(PcfGlyph(
                name=glyph_name,
                encoding=glyph_index_to_encoding.get(glyph_index, PcfBdfEncodings.NO_ENCODING),
                scalable_width=scalable_width,
                character_width=metric.character_width,
                dimensions=metric.dimensions,
                offset=metric.offset,
                attributes=metric.attributes,
                bitmap=bitmap,
            ))

        return builder

    config: PcfFontConfig
    properties: PcfProperties
    glyphs: list[PcfGlyph]

    def __init__(
            self,
            config: PcfFontConfig | None = None,
            properties: PcfProperties | None = None,
            glyphs: list[PcfGlyph] | None = None,
    ):
        self.config = config if config is not None else PcfFontConfig()
        self.properties = properties if properties is not None else PcfProperties()
        self.glyphs = glyphs if glyphs is not None else []

    def __copy__(self) -> PcfFontBuilder:
        return self.copy()

    def __deepcopy__(self, memo: dict[int, Any]) -> PcfFontBuilder:
        return self.deepcopy()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PcfFontBuilder):
            return NotImplemented
        return (self.config == other.config and
                self.properties == other.properties and
                self.glyphs == other.glyphs)

    def build(self) -> PcfFont:
        table_format = self.config.to_table_format()

        bdf_encodings = PcfBdfEncodings(table_format=table_format, default_char=self.config.default_char)
        glyph_names = PcfGlyphNames(table_format=table_format)
        scalable_widths = PcfScalableWidths(table_format=table_format)
        metrics = PcfMetrics(table_format=table_format)
        bitmaps = PcfBitmaps(table_format=table_format)
        accelerators = PcfAccelerators(
            table_format=table_format,
            draw_right_to_left=self.config.draw_right_to_left,
            font_ascent=self.config.font_ascent,
            font_descent=self.config.font_descent,
        )
        properties = PcfProperties(self.properties.data, table_format=table_format)

        for glyph_index, glyph in enumerate(self.glyphs):
            bdf_encodings[glyph.encoding] = glyph_index
            glyph_names.append(glyph.name)
            scalable_widths.append(glyph.scalable_width)
            metrics.append(glyph.create_metric(False))
            bitmaps.append(glyph.bitmap)

        accelerators.max_overlap = calculate_util.calculate_max_overlap(metrics)
        accelerators.min_bounds = calculate_util.calculate_min_bounds(metrics)
        accelerators.max_bounds = calculate_util.calculate_max_bounds(metrics)
        accelerators.calculate_bounds()

        glyph_indices = set(bdf_encodings.values())

        if len(glyph_indices) == len(self.glyphs):
            bdf_accelerators = accelerators.deepcopy()
        else:
            bdf_metrics = [metrics[glyph_index] for glyph_index in glyph_indices]
            bdf_accelerators = PcfAccelerators(
                table_format=table_format,
                draw_right_to_left=self.config.draw_right_to_left,
                font_ascent=self.config.font_ascent,
                font_descent=self.config.font_descent,
            )
            bdf_accelerators.max_overlap = calculate_util.calculate_max_overlap(bdf_metrics)
            bdf_accelerators.min_bounds = calculate_util.calculate_min_bounds(bdf_metrics)
            bdf_accelerators.max_bounds = calculate_util.calculate_max_bounds(bdf_metrics)
            bdf_accelerators.calculate_bounds()

        # ink_bounds
        if accelerators.constant_metrics:
            ink_metrics = PcfMetrics(
                (glyph.create_metric(True) for glyph in self.glyphs),
                table_format=table_format,
            )

            accelerators.ink_min_bounds = calculate_util.calculate_min_bounds(ink_metrics)
            accelerators.ink_max_bounds = calculate_util.calculate_max_bounds(ink_metrics)
            accelerators.table_format = accelerators.table_format.replace(ink_bounds_or_compressed_metrics=True)
            accelerators.ink_metrics = True

            if len(glyph_indices) == len(self.glyphs):
                bdf_accelerators.ink_min_bounds = accelerators.ink_min_bounds.deepcopy()
                bdf_accelerators.ink_max_bounds = accelerators.ink_max_bounds.deepcopy()
            else:
                bdf_ink_metrics = [ink_metrics[glyph_index] for glyph_index in glyph_indices]
                bdf_accelerators.ink_min_bounds = calculate_util.calculate_min_bounds(bdf_ink_metrics)
                bdf_accelerators.ink_max_bounds = calculate_util.calculate_max_bounds(bdf_ink_metrics)
            bdf_accelerators.table_format = bdf_accelerators.table_format.replace(ink_bounds_or_compressed_metrics=True)
            bdf_accelerators.ink_metrics = True
        else:
            ink_metrics = None

            accelerators.table_format = accelerators.table_format.replace(ink_bounds_or_compressed_metrics=False)
            accelerators.ink_metrics = False

            bdf_accelerators.table_format = bdf_accelerators.table_format.replace(ink_bounds_or_compressed_metrics=False)
            bdf_accelerators.ink_metrics = False

        # compressed_metrics
        metrics.table_format = metrics.table_format.replace(ink_bounds_or_compressed_metrics=accelerators.min_bounds.compressible and accelerators.max_bounds.compressible)
        if ink_metrics is not None:
            ink_metrics.table_format = ink_metrics.table_format.replace(ink_bounds_or_compressed_metrics=accelerators.ink_min_bounds.compressible and accelerators.ink_max_bounds.compressible)

        return PcfFont(
            properties,
            accelerators,
            metrics,
            bitmaps,
            ink_metrics,
            bdf_encodings,
            scalable_widths,
            glyph_names,
            bdf_accelerators,
        )

    def save(self, file_path: str | PathLike[str]):
        self.build().save(file_path)

    def copy(self) -> PcfFontBuilder:
        return PcfFontBuilder(
            self.config,
            self.properties,
            self.glyphs,
        )

    def deepcopy(self) -> PcfFontBuilder:
        return PcfFontBuilder(
            self.config.deepcopy(),
            self.properties.deepcopy(),
            [glyph.deepcopy() for glyph in self.glyphs],
        )
