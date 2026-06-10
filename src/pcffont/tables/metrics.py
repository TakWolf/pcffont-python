from __future__ import annotations

from collections import UserList
from collections.abc import Iterable
from typing import Any, TYPE_CHECKING

from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.metric import PcfMetric
from pcffont.table import PcfTable
from pcffont.utils.stream import Stream

if TYPE_CHECKING:
    from pcffont.font import PcfFont


class PcfMetrics(UserList[PcfMetric], PcfTable):
    @staticmethod
    def parse(stream: Stream, header: PcfHeader, font: PcfFont) -> PcfMetrics:
        table_format = header.read_and_check_table_format(stream)

        if table_format.compressed_metrics:
            glyphs_count = stream.read_uint16(table_format.ms_byte_first)
        else:
            glyphs_count = stream.read_uint32(table_format.ms_byte_first)

        metrics = PcfMetrics(table_format=table_format)
        for _ in range(glyphs_count):
            metric = PcfMetric.parse(stream, table_format.ms_byte_first, table_format.compressed_metrics)
            metrics.append(metric)
        return metrics

    table_format: PcfTableFormat

    def __init__(
            self,
            metrics: Iterable[PcfMetric] | None = None,
            table_format: PcfTableFormat | None = None,
    ):
        super().__init__(metrics)
        self.table_format = table_format if table_format is not None else PcfTableFormat()

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __copy__(self) -> PcfMetrics:
        return self.copy()

    def __deepcopy__(self, memo: dict[int, Any]) -> PcfMetrics:
        return self.deepcopy()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfMetrics):
            return NotImplemented
        return (self.table_format == other.table_format and
                super().__eq__(other))

    def dump(self, stream: Stream, table_offset: int, font: PcfFont) -> int:
        glyphs_count = len(self)

        stream.seek(table_offset)
        stream.write_uint32(self.table_format.value)
        if self.table_format.compressed_metrics:
            stream.write_uint16(glyphs_count, self.table_format.ms_byte_first)
        else:
            stream.write_uint32(glyphs_count, self.table_format.ms_byte_first)
        for metric in self:
            metric.dump(stream, self.table_format.ms_byte_first, self.table_format.compressed_metrics)
        stream.align_to_4_bytes()

        table_size = stream.tell() - table_offset
        return table_size

    def copy(self) -> PcfMetrics:
        return PcfMetrics(self.data, self.table_format)

    def deepcopy(self) -> PcfMetrics:
        return PcfMetrics(
            (metric.deepcopy() for metric in self),
            self.table_format.deepcopy(),
        )
