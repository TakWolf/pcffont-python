import os
from io import BytesIO
from typing import BinaryIO


class Stream:
    source: BinaryIO

    def __init__(self, source: bytes | bytearray | BinaryIO | None = None):
        if source is None:
            source = BytesIO()
        elif isinstance(source, (bytes, bytearray)):
            source = BytesIO(source)
        self.source = source

    def read(self, size: int, ignore_eof: bool = False) -> bytes:
        values = self.source.read(size)
        if len(values) < size and not ignore_eof:
            raise EOFError()
        return values

    def read_uint8(self) -> int:
        return int.from_bytes(self.read(1), 'big', signed=False)

    def read_uint8_list(self, count: int) -> list[int]:
        return [self.read_uint8() for _ in range(count)]

    def read_int8(self) -> int:
        return int.from_bytes(self.read(1), 'big', signed=True)

    def read_int8_list(self, count: int) -> list[int]:
        return [self.read_int8() for _ in range(count)]

    def read_uint16(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(2), 'big' if ms_byte_first else 'little', signed=False)

    def read_uint16_list(self, count: int, ms_byte_first: bool = False) -> list[int]:
        return [self.read_uint16(ms_byte_first) for _ in range(count)]

    def read_int16(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(2), 'big' if ms_byte_first else 'little', signed=True)

    def read_int16_list(self, count: int, ms_byte_first: bool = False) -> list[int]:
        return [self.read_int16(ms_byte_first) for _ in range(count)]

    def read_uint32(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(4), 'big' if ms_byte_first else 'little', signed=False)

    def read_uint32_list(self, count: int, ms_byte_first: bool = False) -> list[int]:
        return [self.read_uint32(ms_byte_first) for _ in range(count)]

    def read_int32(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(4), 'big' if ms_byte_first else 'little', signed=True)

    def read_int32_list(self, count: int, ms_byte_first: bool = False) -> list[int]:
        return [self.read_int32(ms_byte_first) for _ in range(count)]

    def read_string(self) -> str:
        values = bytearray()
        while True:
            b = self.read(1)
            if b == b'\x00':
                break
            values.extend(b)
        return values.decode()

    def read_bool(self) -> bool:
        return self.read(1) != b'\x00'

    def write(self, values: bytes) -> int:
        return self.source.write(values)

    def write_uint8(self, value: int) -> int:
        return self.write(value.to_bytes(1, 'big', signed=False))

    def write_uint8_list(self, values: list[int]) -> int:
        return sum(self.write_uint8(value) for value in values)

    def write_int8(self, value: int) -> int:
        return self.write(value.to_bytes(1, 'big', signed=True))

    def write_int8_list(self, values: list[int]) -> int:
        return sum(self.write_int8(value) for value in values)

    def write_uint16(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(2, 'big' if ms_byte_first else 'little', signed=False))

    def write_uint16_list(self, values: list[int], ms_byte_first: bool = False) -> int:
        return sum(self.write_uint16(value, ms_byte_first) for value in values)

    def write_int16(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(2, 'big' if ms_byte_first else 'little', signed=True))

    def write_int16_list(self, values: list[int], ms_byte_first: bool = False) -> int:
        return sum(self.write_int16(value, ms_byte_first) for value in values)

    def write_uint32(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(4, 'big' if ms_byte_first else 'little', signed=False))

    def write_uint32_list(self, values: list[int], ms_byte_first: bool = False) -> int:
        return sum(self.write_uint32(value, ms_byte_first) for value in values)

    def write_int32(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(4, 'big' if ms_byte_first else 'little', signed=True))

    def write_int32_list(self, values: list[int], ms_byte_first: bool = False) -> int:
        return sum(self.write_int32(value, ms_byte_first) for value in values)

    def write_string(self, value: str) -> int:
        return self.write(value.encode()) + self.write_nulls(1)

    def write_bool(self, value: bool) -> int:
        return self.write(b'\x01' if value else b'\x00')

    def write_nulls(self, size: int) -> int:
        if size > 0:
            self.write(b'\x00' * size)
        return size

    def align_to_4_bytes(self) -> int:
        return self.write_nulls(3 - (self.tell() + 3) % 4)

    def seek(self, offset: int, whence: int = os.SEEK_SET):
        self.source.seek(offset, whence)

    def tell(self) -> int:
        return self.source.tell()
