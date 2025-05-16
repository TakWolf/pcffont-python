from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, runtime_checkable, TYPE_CHECKING

from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.utils.stream import Stream

if TYPE_CHECKING:
    from pcffont.font import PcfFont


@runtime_checkable
class PcfTable(Protocol):
    @staticmethod
    @abstractmethod
    def parse(stream: Stream, header: PcfHeader, font: PcfFont) -> PcfTable:
        raise NotImplementedError()

    table_format: PcfTableFormat

    @abstractmethod
    def dump(self, stream: Stream, table_offset: int, font: PcfFont) -> int:
        raise NotImplementedError()
