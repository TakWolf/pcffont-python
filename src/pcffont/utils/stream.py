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

    def read_int8(self) -> int:
        return int.from_bytes(self.read(1), 'big', signed=True)

    def read_uint16(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(2), 'big' if ms_byte_first else 'little', signed=False)

    def read_int16(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(2), 'big' if ms_byte_first else 'little', signed=True)

    def read_uint32(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(4), 'big' if ms_byte_first else 'little', signed=False)

    def read_int32(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(4), 'big' if ms_byte_first else 'little', signed=True)

    def read_binary(self, ms_bit_first: bool = False) -> list[int]:
        binary = [int(c) for c in f'{self.read(1)[0]:08b}']
        if not ms_bit_first:
            binary.reverse()
        return binary

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

    def write_int8(self, value: int) -> int:
        return self.write(value.to_bytes(1, 'big', signed=True))

    def write_uint16(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(2, 'big' if ms_byte_first else 'little', signed=False))

    def write_int16(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(2, 'big' if ms_byte_first else 'little', signed=True))

    def write_uint32(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(4, 'big' if ms_byte_first else 'little', signed=False))

    def write_int32(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(4, 'big' if ms_byte_first else 'little', signed=True))

    def write_binary(self, value: list[int], ms_bit_first: bool = False) -> int:
        if not ms_bit_first:
            value = value[::-1]
        return self.write(bytes([int(''.join(map(str, value)), 2)]))

    def write_string(self, value: str) -> int:
        return self.write(value.encode()) + self.write_nulls(1)

    def write_bool(self, value: bool) -> int:
        return self.write(b'\x01' if value else b'\x00')

    def write_nulls(self, size: int) -> int:
        for _ in range(size):
            self.write(b'\x00')
        return size

    def align_to_4_byte_with_nulls(self) -> int:
        return self.write_nulls(3 - (self.tell() + 3) % 4)

    def seek(self, offset: int, whence: int = os.SEEK_SET):
        self.source.seek(offset, whence)

    def tell(self) -> int:
        return self.source.tell()
