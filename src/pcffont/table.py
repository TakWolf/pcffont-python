from abc import abstractmethod
from typing import Protocol, runtime_checkable

import pcffont
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.utils.stream import Stream


@runtime_checkable
class PcfTable(Protocol):
    table_format: PcfTableFormat

    @staticmethod
    @abstractmethod
    def parse(stream: Stream, header: PcfHeader, font: 'pcffont.PcfFont') -> 'PcfTable':
        raise NotImplementedError()

    @abstractmethod
    def dump(self, stream: Stream, table_offset: int, font: 'pcffont.PcfFont') -> int:
        raise NotImplementedError()
