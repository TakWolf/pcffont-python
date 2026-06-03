import os
import struct
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
        data = self.source.read(size)
        if len(data) < size and not ignore_eof:
            raise EOFError()
        return data

    def read_uint8(self) -> int:
        return self.read(1)[0]

    def read_uint8_list(self, count: int) -> list[int]:
        return list(self.read(count))

    def read_int8(self) -> int:
        return int.from_bytes(self.read(1), 'big', signed=True)

    def read_int8_list(self, count: int) -> list[int]:
        return list(struct.unpack(f'{count}b', self.read(count)))

    def read_uint16(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(2), 'big' if ms_byte_first else 'little', signed=False)

    def read_uint16_list(self, count: int, ms_byte_first: bool = False) -> list[int]:
        return list(struct.unpack(f"{'>' if ms_byte_first else '<'}{count}H", self.read(count * 2)))

    def read_int16(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(2), 'big' if ms_byte_first else 'little', signed=True)

    def read_int16_list(self, count: int, ms_byte_first: bool = False) -> list[int]:
        return list(struct.unpack(f"{'>' if ms_byte_first else '<'}{count}h", self.read(count * 2)))

    def read_uint32(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(4), 'big' if ms_byte_first else 'little', signed=False)

    def read_uint32_list(self, count: int, ms_byte_first: bool = False) -> list[int]:
        return list(struct.unpack(f"{'>' if ms_byte_first else '<'}{count}I", self.read(count * 4)))

    def read_int32(self, ms_byte_first: bool = False) -> int:
        return int.from_bytes(self.read(4), 'big' if ms_byte_first else 'little', signed=True)

    def read_int32_list(self, count: int, ms_byte_first: bool = False) -> list[int]:
        return list(struct.unpack(f"{'>' if ms_byte_first else '<'}{count}i", self.read(count * 4)))

    def read_string(self) -> str:
        data = bytearray()
        while True:
            b = self.read(1)
            if b == b'\x00':
                break
            data.extend(b)
        return data.decode()

    def read_bool(self) -> bool:
        return self.read(1) != b'\x00'

    def write(self, data: bytes) -> int:
        return self.source.write(data)

    def write_uint8(self, value: int) -> int:
        return self.write(value.to_bytes(1, 'big', signed=False))

    def write_uint8_list(self, values: list[int]) -> int:
        return self.write(bytes(values))

    def write_int8(self, value: int) -> int:
        return self.write(value.to_bytes(1, 'big', signed=True))

    def write_int8_list(self, values: list[int]) -> int:
        return self.write(struct.pack(f'{len(values)}b', *values))

    def write_uint16(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(2, 'big' if ms_byte_first else 'little', signed=False))

    def write_uint16_list(self, values: list[int], ms_byte_first: bool = False) -> int:
        return self.write(struct.pack(f"{'>' if ms_byte_first else '<'}{len(values)}H", *values))

    def write_int16(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(2, 'big' if ms_byte_first else 'little', signed=True))

    def write_int16_list(self, values: list[int], ms_byte_first: bool = False) -> int:
        return self.write(struct.pack(f"{'>' if ms_byte_first else '<'}{len(values)}h", *values))

    def write_uint32(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(4, 'big' if ms_byte_first else 'little', signed=False))

    def write_uint32_list(self, values: list[int], ms_byte_first: bool = False) -> int:
        return self.write(struct.pack(f"{'>' if ms_byte_first else '<'}{len(values)}I", *values))

    def write_int32(self, value: int, ms_byte_first: bool = False) -> int:
        return self.write(value.to_bytes(4, 'big' if ms_byte_first else 'little', signed=True))

    def write_int32_list(self, values: list[int], ms_byte_first: bool = False) -> int:
        return self.write(struct.pack(f"{'>' if ms_byte_first else '<'}{len(values)}i", *values))

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
