import pytest

from pcffont.utils.stream import Stream


def test_bytes():
    stream = Stream()
    assert stream.write(b'Hello World') == 11
    assert stream.tell() == 11
    stream.seek(0)
    assert stream.read(11) == b'Hello World'
    assert stream.tell() == 11


def test_eof():
    stream = Stream()
    stream.write(b'ABC')
    with pytest.raises(EOFError):
        stream.read(4)
    stream.seek(0)
    assert stream.read(4, ignore_eof=True) == b'ABC'


def test_uint8():
    stream = Stream()
    assert stream.write_uint8(0x00) == 1
    assert stream.write_uint8(0xFF) == 1
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_uint8() == 0x00
    assert stream.read_uint8() == 0xFF
    assert stream.tell() == 2


def test_int8():
    stream = Stream()
    assert stream.write_int8(-0x80) == 1
    assert stream.write_int8(0x7F) == 1
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_int8() == -0x80
    assert stream.read_int8() == 0x7F
    assert stream.tell() == 2


def test_uint16():
    stream = Stream()
    assert stream.write_uint16(0x0000, False) == 2
    assert stream.write_uint16(0xFFFF, False) == 2
    assert stream.write_uint16(0x0000, True) == 2
    assert stream.write_uint16(0xFFFF, True) == 2
    assert stream.tell() == 8
    stream.seek(0)
    assert stream.read_uint16(False) == 0x0000
    assert stream.read_uint16(False) == 0xFFFF
    assert stream.read_uint16(True) == 0x0000
    assert stream.read_uint16(True) == 0xFFFF
    assert stream.tell() == 8


def test_int16():
    stream = Stream()
    assert stream.write_int16(-0x8000, False) == 2
    assert stream.write_int16(0x7FFF, False) == 2
    assert stream.write_int16(-0x8000, True) == 2
    assert stream.write_int16(0x7FFF, True) == 2
    assert stream.tell() == 8
    stream.seek(0)
    assert stream.read_int16(False) == -0x8000
    assert stream.read_int16(False) == 0x7FFF
    assert stream.read_int16(True) == -0x8000
    assert stream.read_int16(True) == 0x7FFF
    assert stream.tell() == 8


def test_uint32():
    stream = Stream()
    assert stream.write_uint32(0x00000000, False) == 4
    assert stream.write_uint32(0xFFFFFFFF, False) == 4
    assert stream.write_uint32(0x00000000, True) == 4
    assert stream.write_uint32(0xFFFFFFFF, True) == 4
    assert stream.tell() == 16
    stream.seek(0)
    assert stream.read_uint32(False) == 0x00000000
    assert stream.read_uint32(False) == 0xFFFFFFFF
    assert stream.read_uint32(True) == 0x00000000
    assert stream.read_uint32(True) == 0xFFFFFFFF
    assert stream.tell() == 16


def test_int32():
    stream = Stream()
    assert stream.write_int32(-0x80000000, False) == 4
    assert stream.write_int32(0x7FFFFFFF, False) == 4
    assert stream.write_int32(-0x80000000, True) == 4
    assert stream.write_int32(0x7FFFFFFF, True) == 4
    assert stream.tell() == 16
    stream.seek(0)
    assert stream.read_int32(False) == -0x80000000
    assert stream.read_int32(False) == 0x7FFFFFFF
    assert stream.read_int32(True) == -0x80000000
    assert stream.read_int32(True) == 0x7FFFFFFF
    assert stream.tell() == 16


def test_binary():
    stream = Stream()
    assert stream.write_binary([1, 1, 1, 1, 0, 0, 0, 0], False) == 1
    assert stream.write_binary([1, 1, 1, 1, 0, 0, 0, 0], True) == 1
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_binary(False) == [1, 1, 1, 1, 0, 0, 0, 0]
    assert stream.read_binary(True) == [1, 1, 1, 1, 0, 0, 0, 0]
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_binary(True) == [0, 0, 0, 0, 1, 1, 1, 1]
    assert stream.read_binary(False) == [0, 0, 0, 0, 1, 1, 1, 1]
    assert stream.tell() == 2


def test_string():
    stream = Stream()
    assert stream.write_string('ABC') == 4
    assert stream.write_string('12345') == 6
    assert stream.tell() == 10
    stream.seek(0)
    assert stream.read_string() == 'ABC'
    assert stream.read_string() == '12345'
    assert stream.tell() == 10


def test_bool():
    stream = Stream()
    assert stream.write_bool(True) == 1
    assert stream.write_bool(False) == 1
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_bool()
    assert not stream.read_bool()
    assert stream.tell() == 2


def test_align_to_4_byte():
    stream = Stream()
    stream.write(b'abc')
    assert stream.align_to_4_byte_with_nulls() == 1
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read(4) == b'abc\x00'
