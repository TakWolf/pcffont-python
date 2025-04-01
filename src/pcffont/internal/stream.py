from collections.abc import Iterable
from typing import BinaryIO


class Stream:
    source: BinaryIO

    def __init__(self, source: BinaryIO):
        self.source = source

    def read(self, size: int, ignore_eof: bool = False) -> bytes:
        values = self.source.read(size)
        if len(values) < size and not ignore_eof:
            raise EOFError()
        return values

    def read_int(self, size: int, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(size), 'big' if ms_byte_first else 'little', signed=True)

    def read_int_list(self, size: int, length: int, ms_byte_first: bool = False) -> list[int]:
        return [self.read_int(size, ms_byte_first) for _ in range(length)]

    def read_int8(self) -> int:
        return self.read_int(1)

    def read_int8_list(self, length: int) -> list[int]:
        return self.read_int_list(1, length)

    def read_int16(self, ms_byte_first: bool = False) -> int:
        return self.read_int(2, ms_byte_first)

    def read_int16_list(self, length: int, ms_byte_first: bool = False) -> list[int]:
        return self.read_int_list(2, length, ms_byte_first)

    def read_int32(self, ms_byte_first: bool = False) -> int:
        return self.read_int(4, ms_byte_first)

    def read_int32_list(self, length: int, ms_byte_first: bool = False) -> list[int]:
        return self.read_int_list(4, length, ms_byte_first)

    def read_uint(self, size: int, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(size), 'big' if ms_byte_first else 'little', signed=False)

    def read_uint_list(self, size: int, length: int, ms_byte_first: bool = False) -> list[int]:
        return [self.read_uint(size, ms_byte_first) for _ in range(length)]

    def read_uint8(self) -> int:
        return self.read_uint(1)

    def read_uint8_list(self, length: int) -> list[int]:
        return self.read_uint_list(1, length)

    def read_uint16(self, ms_byte_first: bool = False) -> int:
        return self.read_uint(2, ms_byte_first)

    def read_uint16_list(self, length: int, ms_byte_first: bool = False) -> list[int]:
        return self.read_uint_list(2, length, ms_byte_first)

    def read_uint32(self, ms_byte_first: bool = False) -> int:
        return self.read_uint(4, ms_byte_first)

    def read_uint32_list(self, length: int, ms_byte_first: bool = False) -> list[int]:
        return self.read_uint_list(4, length, ms_byte_first)

    def read_binary(self, ms_bit_first: bool = False) -> list[int]:
        binary = [int(c) for c in f'{self.read(1)[0]:08b}']
        if not ms_bit_first:
            binary.reverse()
        return binary

    def read_binary_list(self, length: int, ms_bit_first: bool = False) -> list[list[int]]:
        return [self.read_binary(ms_bit_first) for _ in range(length)]

    def read_string(self) -> str:
        values = bytearray()
        while True:
            b = self.read(1)
            if b == b'\x00':
                break
            values.extend(b)
        return values.decode()

    def read_string_list(self, length: int) -> list[str]:
        return [self.read_string() for _ in range(length)]

    def read_bool(self) -> bool:
        return self.read(1) != b'\x00'

    def write(self, values: bytes) -> int:
        return self.source.write(values)

    def write_int(self, value: int, size: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(size, 'big' if ms_byte_first else 'little', signed=True))

    def write_int_list(self, values: Iterable[int], size: int, ms_byte_first: bool = False) -> int:
        return sum([self.write_int(value, size, ms_byte_first) for value in values])

    def write_int8(self, value: int) -> int:
        return self.write_int(value, 1)

    def write_int8_list(self, values: Iterable[int]) -> int:
        return self.write_int_list(values, 1)

    def write_int16(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write_int(value, 2, ms_byte_first)

    def write_int16_list(self, values: Iterable[int], ms_byte_first: bool = False) -> int:
        return self.write_int_list(values, 2, ms_byte_first)

    def write_int32(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write_int(value, 4, ms_byte_first)

    def write_int32_list(self, values: Iterable[int], ms_byte_first: bool = False) -> int:
        return self.write_int_list(values, 4, ms_byte_first)

    def write_uint(self, value: int, size: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(size, 'big' if ms_byte_first else 'little', signed=False))

    def write_uint_list(self, values: Iterable[int], size: int, ms_byte_first: bool = False) -> int:
        return sum([self.write_uint(value, size, ms_byte_first) for value in values])

    def write_uint8(self, value: int) -> int:
        return self.write_uint(value, 1)

    def write_uint8_list(self, values: Iterable[int]) -> int:
        return self.write_uint_list(values, 1)

    def write_uint16(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write_uint(value, 2, ms_byte_first)

    def write_uint16_list(self, values: Iterable[int], ms_byte_first: bool = False) -> int:
        return self.write_uint_list(values, 2, ms_byte_first)

    def write_uint32(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write_uint(value, 4, ms_byte_first)

    def write_uint32_list(self, values: Iterable[int], ms_byte_first: bool = False) -> int:
        return self.write_uint_list(values, 4, ms_byte_first)

    def write_binary(self, value: list[int], ms_bit_first: bool = False) -> int:
        if not ms_bit_first:
            value = value[::-1]
        return self.write(bytes([int(''.join(map(str, value)), 2)]))

    def write_binary_list(self, values: Iterable[list[int]], ms_bit_first: bool = False) -> int:
        return sum([self.write_binary(value, ms_bit_first) for value in values])

    def write_string(self, value: str) -> int:
        return self.write(value.encode()) + self.write_nulls(1)

    def write_string_list(self, values: Iterable[str]) -> int:
        return sum([self.write_string(value) for value in values])

    def write_bool(self, value: bool) -> int:
        return self.write(b'\x01' if value else b'\x00')

    def write_nulls(self, size: int) -> int:
        for _ in range(size):
            self.write(b'\x00')
        return size

    def align_to_bit32_with_nulls(self) -> int:
        return self.write_nulls(3 - (self.tell() + 3) % 4)

    def seek(self, offset: int):
        self.source.seek(offset)

    def tell(self) -> int:
        return self.source.tell()

    def skip(self, size: int):
        self.seek(self.tell() + size)
