from __future__ import annotations

import os
import re
from collections import UserDict
from typing import Any, TYPE_CHECKING

from pcffont.error import PcfXlfdError
from pcffont.format import PcfTableFormat
from pcffont.header import PcfHeader
from pcffont.table import PcfTable
from pcffont.utils.stream import Stream

if TYPE_CHECKING:
    from pcffont.font import PcfFont

_KEY_FOUNDRY = 'FOUNDRY'
_KEY_FAMILY_NAME = 'FAMILY_NAME'
_KEY_WEIGHT_NAME = 'WEIGHT_NAME'
_KEY_SLANT = 'SLANT'
_KEY_SETWIDTH_NAME = 'SETWIDTH_NAME'
_KEY_ADD_STYLE_NAME = 'ADD_STYLE_NAME'
_KEY_PIXEL_SIZE = 'PIXEL_SIZE'
_KEY_POINT_SIZE = 'POINT_SIZE'
_KEY_RESOLUTION_X = 'RESOLUTION_X'
_KEY_RESOLUTION_Y = 'RESOLUTION_Y'
_KEY_SPACING = 'SPACING'
_KEY_AVERAGE_WIDTH = 'AVERAGE_WIDTH'
_KEY_CHARSET_REGISTRY = 'CHARSET_REGISTRY'
_KEY_CHARSET_ENCODING = 'CHARSET_ENCODING'

_KEY_X_HEIGHT = 'X_HEIGHT'
_KEY_CAP_HEIGHT = 'CAP_HEIGHT'
_KEY_UNDERLINE_POSITION = 'UNDERLINE_POSITION'
_KEY_UNDERLINE_THICKNESS = 'UNDERLINE_THICKNESS'

_KEY_FONT = 'FONT'
_KEY_FONT_VERSION = 'FONT_VERSION'
_KEY_COPYRIGHT = 'COPYRIGHT'
_KEY_NOTICE = 'NOTICE'

_STR_VALUE_KEYS = {
    _KEY_FOUNDRY,
    _KEY_FAMILY_NAME,
    _KEY_WEIGHT_NAME,
    _KEY_SLANT,
    _KEY_SETWIDTH_NAME,
    _KEY_ADD_STYLE_NAME,
    _KEY_SPACING,
    _KEY_CHARSET_REGISTRY,
    _KEY_CHARSET_ENCODING,
    _KEY_FONT,
    _KEY_FONT_VERSION,
    _KEY_COPYRIGHT,
    _KEY_NOTICE,
}

_INT_VALUE_KEYS = {
    _KEY_PIXEL_SIZE,
    _KEY_POINT_SIZE,
    _KEY_RESOLUTION_X,
    _KEY_RESOLUTION_Y,
    _KEY_AVERAGE_WIDTH,
    _KEY_X_HEIGHT,
    _KEY_CAP_HEIGHT,
    _KEY_UNDERLINE_POSITION,
    _KEY_UNDERLINE_THICKNESS,
}

_XLFD_STR_VALUE_KEYS = {
    _KEY_FOUNDRY,
    _KEY_FAMILY_NAME,
    _KEY_WEIGHT_NAME,
    _KEY_SLANT,
    _KEY_SETWIDTH_NAME,
    _KEY_ADD_STYLE_NAME,
    _KEY_SPACING,
    _KEY_CHARSET_REGISTRY,
    _KEY_CHARSET_ENCODING,
}

_XLFD_KEYS_ORDER = [
    _KEY_FOUNDRY,
    _KEY_FAMILY_NAME,
    _KEY_WEIGHT_NAME,
    _KEY_SLANT,
    _KEY_SETWIDTH_NAME,
    _KEY_ADD_STYLE_NAME,
    _KEY_PIXEL_SIZE,
    _KEY_POINT_SIZE,
    _KEY_RESOLUTION_X,
    _KEY_RESOLUTION_Y,
    _KEY_SPACING,
    _KEY_AVERAGE_WIDTH,
    _KEY_CHARSET_REGISTRY,
    _KEY_CHARSET_ENCODING,
]


class PcfProperties(UserDict[str, str | int], PcfTable):
    @staticmethod
    def parse(stream: Stream, header: PcfHeader, font: PcfFont) -> PcfProperties:
        table_format = header.read_and_check_table_format(stream)

        props_count = stream.read_uint32(table_format.ms_byte_first)

        prop_infos = []
        for _ in range(props_count):
            key_offset = stream.read_uint32(table_format.ms_byte_first)
            is_string_prop = stream.read_bool()
            if is_string_prop:
                value_offset = stream.read_uint32(table_format.ms_byte_first)
                prop_infos.append((key_offset, is_string_prop, value_offset))
            else:
                value = stream.read_int32(table_format.ms_byte_first)
                prop_infos.append((key_offset, is_string_prop, value))

        # Pad to next int32 boundary
        padding = 3 - ((4 + 1 + 4) * props_count + 3) % 4
        stream.seek(padding, os.SEEK_CUR)

        stream.seek(4, os.SEEK_CUR)  # strings_size
        strings_start = stream.tell()

        properties = {}
        for key_offset, is_string_prop, value in prop_infos:
            stream.seek(strings_start + key_offset)
            key = stream.read_string()
            if is_string_prop:
                stream.seek(strings_start + value)
                value = stream.read_string()
            properties[key] = value

        return PcfProperties(table_format, properties)

    table_format: PcfTableFormat

    def __init__(
            self,
            table_format: PcfTableFormat | None = None,
            properties: dict[str, str | int] | None = None,
    ):
        super().__init__(properties)
        self.table_format = PcfTableFormat() if table_format is None else table_format

    def __getitem__(self, key: Any) -> str | int:
        if isinstance(key, str):
            key = key.upper()
        return super().__getitem__(key)

    def __setitem__(self, key: Any, value: Any):
        if value is None:
            self.pop(key, None)
            return

        if not isinstance(key, str):
            raise KeyError(f"expected type 'str', got '{type(key).__name__}' instead")
        key = key.upper()

        if not key.replace('_', '').isalnum():
            raise KeyError('contains illegal characters')

        if key in _STR_VALUE_KEYS:
            if not isinstance(value, str):
                raise ValueError(f"expected type 'str', got '{type(value).__name__}' instead")
        elif key in _INT_VALUE_KEYS:
            if not isinstance(value, int):
                raise ValueError(f"expected type 'int', got '{type(value).__name__}' instead")
        else:
            if not isinstance(value, str) and not isinstance(value, int):
                raise ValueError(f"expected type 'str | int', got '{type(value).__name__}' instead")

        if key in _XLFD_STR_VALUE_KEYS:
            matched = re.search(r'[-?*,"]', value)
            if matched is not None:
                raise ValueError(f'contains illegal characters {repr(matched.group())}')

        super().__setitem__(key, value)

    def __delitem__(self, key: Any):
        if isinstance(key, str):
            key = key.upper()
        super().__delitem__(key)

    def __contains__(self, key: Any) -> bool:
        if isinstance(key, str):
            key = key.upper()
        return super().__contains__(key)

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PcfProperties):
            return NotImplemented
        return (self.table_format == other.table_format and
                super().__eq__(other))

    @property
    def foundry(self) -> str | None:
        return self.get(_KEY_FOUNDRY, None)

    @foundry.setter
    def foundry(self, value: str | None):
        self[_KEY_FOUNDRY] = value

    @property
    def family_name(self) -> str | None:
        return self.get(_KEY_FAMILY_NAME, None)

    @family_name.setter
    def family_name(self, value: str | None):
        self[_KEY_FAMILY_NAME] = value

    @property
    def weight_name(self) -> str | None:
        return self.get(_KEY_WEIGHT_NAME, None)

    @weight_name.setter
    def weight_name(self, value: str | None):
        self[_KEY_WEIGHT_NAME] = value

    @property
    def slant(self) -> str | None:
        return self.get(_KEY_SLANT, None)

    @slant.setter
    def slant(self, value: str | None):
        self[_KEY_SLANT] = value

    @property
    def setwidth_name(self) -> str | None:
        return self.get(_KEY_SETWIDTH_NAME, None)

    @setwidth_name.setter
    def setwidth_name(self, value: str | None):
        self[_KEY_SETWIDTH_NAME] = value

    @property
    def add_style_name(self) -> str | None:
        return self.get(_KEY_ADD_STYLE_NAME, None)

    @add_style_name.setter
    def add_style_name(self, value: str | None):
        self[_KEY_ADD_STYLE_NAME] = value

    @property
    def pixel_size(self) -> int | None:
        return self.get(_KEY_PIXEL_SIZE, None)

    @pixel_size.setter
    def pixel_size(self, value: int | None):
        self[_KEY_PIXEL_SIZE] = value

    @property
    def point_size(self) -> int | None:
        return self.get(_KEY_POINT_SIZE, None)

    @point_size.setter
    def point_size(self, value: int | None):
        self[_KEY_POINT_SIZE] = value

    @property
    def resolution_x(self) -> int | None:
        return self.get(_KEY_RESOLUTION_X, None)

    @resolution_x.setter
    def resolution_x(self, value: int | None):
        self[_KEY_RESOLUTION_X] = value

    @property
    def resolution_y(self) -> int | None:
        return self.get(_KEY_RESOLUTION_Y, None)

    @resolution_y.setter
    def resolution_y(self, value: int | None):
        self[_KEY_RESOLUTION_Y] = value

    @property
    def spacing(self) -> str | None:
        return self.get(_KEY_SPACING, None)

    @spacing.setter
    def spacing(self, value: str | None):
        self[_KEY_SPACING] = value

    @property
    def average_width(self) -> int | None:
        return self.get(_KEY_AVERAGE_WIDTH, None)

    @average_width.setter
    def average_width(self, value: int | None):
        self[_KEY_AVERAGE_WIDTH] = value

    @property
    def charset_registry(self) -> str | None:
        return self.get(_KEY_CHARSET_REGISTRY, None)

    @charset_registry.setter
    def charset_registry(self, value: str | None):
        self[_KEY_CHARSET_REGISTRY] = value

    @property
    def charset_encoding(self) -> str | None:
        return self.get(_KEY_CHARSET_ENCODING, None)

    @charset_encoding.setter
    def charset_encoding(self, value: str | None):
        self[_KEY_CHARSET_ENCODING] = value

    @property
    def x_height(self) -> int | None:
        return self.get(_KEY_X_HEIGHT, None)

    @x_height.setter
    def x_height(self, value: int | None):
        self[_KEY_X_HEIGHT] = value

    @property
    def cap_height(self) -> int | None:
        return self.get(_KEY_CAP_HEIGHT, None)

    @cap_height.setter
    def cap_height(self, value: int | None):
        self[_KEY_CAP_HEIGHT] = value

    @property
    def underline_position(self) -> int | None:
        return self.get(_KEY_UNDERLINE_POSITION, None)

    @underline_position.setter
    def underline_position(self, value: int | None):
        self[_KEY_UNDERLINE_POSITION] = value

    @property
    def underline_thickness(self) -> int | None:
        return self.get(_KEY_UNDERLINE_THICKNESS, None)

    @underline_thickness.setter
    def underline_thickness(self, value: int | None):
        self[_KEY_UNDERLINE_THICKNESS] = value

    @property
    def font(self) -> str | None:
        return self.get(_KEY_FONT, None)

    @font.setter
    def font(self, value: str | None):
        self[_KEY_FONT] = value

    @property
    def font_version(self) -> str | None:
        return self.get(_KEY_FONT_VERSION, None)

    @font_version.setter
    def font_version(self, value: str | None):
        self[_KEY_FONT_VERSION] = value

    @property
    def copyright(self) -> str | None:
        return self.get(_KEY_COPYRIGHT, None)

    @copyright.setter
    def copyright(self, value: str | None):
        self[_KEY_COPYRIGHT] = value

    @property
    def notice(self) -> str | None:
        return self.get(_KEY_NOTICE, None)

    @notice.setter
    def notice(self, value: str | None):
        self[_KEY_NOTICE] = value

    def generate_xlfd(self):
        tokens = ['']
        for key in _XLFD_KEYS_ORDER:
            tokens.append(str(self.get(key, '')))
        self.font = '-'.join(tokens)

    def update_by_xlfd(self):
        if self.font is None:
            raise PcfXlfdError(f"'{_KEY_FONT}' not set")
        if not self.font.startswith('-'):
            raise PcfXlfdError("not starts with '-'")
        if self.font.count('-') != 14:
            raise PcfXlfdError("must be 14 '-'")
        tokens = self.font.removeprefix('-').split('-')
        for key, token in zip(_XLFD_KEYS_ORDER, tokens):
            if token == '':
                value = None
            else:
                if key in _XLFD_STR_VALUE_KEYS:
                    value = token
                else:
                    value = int(token)
            self[key] = value

    def dump(self, stream: Stream, table_offset: int, font: PcfFont) -> int:
        props_count = len(self)

        # Pad to next int32 boundary
        padding = 3 - ((4 + 1 + 4) * props_count + 3) % 4

        strings_start = table_offset + 4 + 4 + (4 + 1 + 4) * props_count + padding + 4
        strings_size = 0
        prop_infos = []
        stream.seek(strings_start)
        for key, value in self.items():
            key_offset = strings_size
            strings_size += stream.write_string(key)
            value_offset = strings_size
            if isinstance(value, str):
                strings_size += stream.write_string(value)
            prop_infos.append((key_offset, value, value_offset))

        stream.seek(table_offset)
        stream.write_uint32(self.table_format.value)
        stream.write_uint32(props_count, self.table_format.ms_byte_first)
        for key_offset, value, value_offset in prop_infos:
            stream.write_uint32(key_offset, self.table_format.ms_byte_first)
            if isinstance(value, str):
                stream.write_bool(True)
                stream.write_uint32(value_offset, self.table_format.ms_byte_first)
            else:
                stream.write_bool(False)
                stream.write_int32(value, self.table_format.ms_byte_first)
        stream.write_nulls(padding)
        stream.write_uint32(strings_size, self.table_format.ms_byte_first)
        stream.seek(strings_size, os.SEEK_CUR)
        stream.align_to_4_byte_with_nulls()

        table_size = stream.tell() - table_offset
        return table_size
