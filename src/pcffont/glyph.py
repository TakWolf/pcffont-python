from __future__ import annotations

from typing import Any

from pcffont.metric import PcfMetric


class PcfGlyph:
    name: str
    encoding: int
    scalable_width: int
    character_width: int
    width: int
    height: int
    offset_x: int
    offset_y: int
    bitmap: list[list[int]]
    attributes: int

    def __init__(
            self,
            name: str,
            encoding: int,
            scalable_width: int = 0,
            character_width: int = 0,
            dimensions: tuple[int, int] = (0, 0),
            offset: tuple[int, int] = (0, 0),
            bitmap: list[list[int]] | None = None,
            attributes: int = 0,
    ):
        self.name = name
        self.encoding = encoding
        self.scalable_width = scalable_width
        self.character_width = character_width
        self.width, self.height = dimensions
        self.offset_x, self.offset_y = offset
        self.bitmap = bitmap if bitmap is not None else []
        self.attributes = attributes

    def __copy__(self) -> PcfGlyph:
        return self.copy()

    def __deepcopy__(self, memo: dict[int, Any]) -> PcfGlyph:
        return self.deepcopy()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfGlyph):
            return NotImplemented
        return (self.name == other.name and
                self.encoding == other.encoding and
                self.scalable_width == other.scalable_width and
                self.character_width == other.character_width and
                self.width == other.width and
                self.height == other.height and
                self.offset_x == other.offset_x and
                self.offset_y == other.offset_y and
                self.attributes == other.attributes and
                self.bitmap == other.bitmap)

    @property
    def dimensions(self) -> tuple[int, int]:
        return self.width, self.height

    @dimensions.setter
    def dimensions(self, value: tuple[int, int]):
        self.width, self.height = value

    @property
    def offset(self) -> tuple[int, int]:
        return self.offset_x, self.offset_y

    @offset.setter
    def offset(self, value: tuple[int, int]):
        self.offset_x, self.offset_y = value

    def create_metric(self, is_ink: bool) -> PcfMetric:
        metric = PcfMetric(
            left_side_bearing=self.offset_x,
            right_side_bearing=self.offset_x + self.width,
            character_width=self.character_width,
            ascent=self.offset_y + self.height,
            descent=-self.offset_y,
            attributes=self.attributes,
        )

        if not is_ink:
            return metric

        first_row = self.height
        last_row = -1
        first_col = self.width
        last_col = -1

        for y in range(self.height):
            if y >= len(self.bitmap):
                break
            bitmap_row = self.bitmap[y]
            width_limit = min(len(bitmap_row), self.width)
            for x in range(width_limit):
                if bitmap_row[x] != 0:
                    if y < first_row:
                        first_row = y
                    if y > last_row:
                        last_row = y
                    if x < first_col:
                        first_col = x
                    if x > last_col:
                        last_col = x

        if first_row == self.height:
            metric.ascent = 0
            metric.descent = 0
            metric.right_side_bearing = metric.left_side_bearing
            return metric

        metric.ascent -= first_row
        metric.descent -= self.height - 1 - last_row if last_row != -1 else self.height
        metric.left_side_bearing += first_col
        metric.right_side_bearing -= self.width - 1 - last_col if last_col != -1 else self.width
        return metric

    def copy(self) -> PcfGlyph:
        return PcfGlyph(
            self.name,
            self.encoding,
            self.scalable_width,
            self.character_width,
            self.dimensions,
            self.offset,
            self.bitmap,
            self.attributes,
        )

    def deepcopy(self) -> PcfGlyph:
        return PcfGlyph(
            self.name,
            self.encoding,
            self.scalable_width,
            self.character_width,
            self.dimensions,
            self.offset,
            [bitmap_row.copy() for bitmap_row in self.bitmap],
            self.attributes,
        )
