from abc import abstractmethod
from typing import Protocol, runtime_checkable

from pcffont.format import PcfTableFormat
from pcffont.header import PcfTableType, PcfHeader
from pcffont.utils.stream import Stream


@runtime_checkable
class PcfTableContainer(Protocol):
    @abstractmethod
    def get_table(self, table_type: PcfTableType) -> 'PcfTable':
        raise NotImplementedError()


@runtime_checkable
class PcfTable(Protocol):
    @staticmethod
    @abstractmethod
    def parse(stream: Stream, header: PcfHeader, container: PcfTableContainer) -> 'PcfTable':
        raise NotImplementedError()

    table_format: PcfTableFormat

    @abstractmethod
    def dump(self, stream: Stream, table_offset: int, container: PcfTableContainer) -> int:
        raise NotImplementedError()
