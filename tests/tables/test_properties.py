from copy import copy, deepcopy

import pytest

from pcffont import PcfTableFormat, PcfProperties
from pcffont.error import PcfXlfdError


def test_properties_1():
    properties = PcfProperties({
        'PARAM_1': 1,
        'param_2': '2',
        'PARAM_3': None,
    })

    assert len(properties) == 2
    assert properties['param_1'] == 1
    assert properties['PARAM_2'] == '2'


def test_properties_2():
    properties = PcfProperties()

    properties.foundry = 'TakWolf Studio'
    assert properties.foundry == 'TakWolf Studio'
    assert properties['FOUNDRY'] == 'TakWolf Studio'

    properties.family_name = 'Demo Pixel'
    assert properties.family_name == 'Demo Pixel'
    assert properties['FAMILY_NAME'] == 'Demo Pixel'

    properties.weight_name = 'Medium'
    assert properties.weight_name == 'Medium'
    assert properties['WEIGHT_NAME'] == 'Medium'

    properties.slant = 'R'
    assert properties.slant == 'R'
    assert properties['SLANT'] == 'R'

    properties.setwidth_name = 'Normal'
    assert properties.setwidth_name == 'Normal'
    assert properties['SETWIDTH_NAME'] == 'Normal'

    properties.add_style_name = 'Sans Serif'
    assert properties.add_style_name == 'Sans Serif'
    assert properties['ADD_STYLE_NAME'] == 'Sans Serif'

    properties.pixel_size = 16
    assert properties.pixel_size == 16
    assert properties['PIXEL_SIZE'] == 16

    properties.point_size = 160
    assert properties.point_size == 160
    assert properties['POINT_SIZE'] == 160

    properties.resolution_x = 75
    assert properties.resolution_x == 75
    assert properties['RESOLUTION_X'] == 75

    properties.resolution_y = 240
    assert properties.resolution_y == 240
    assert properties['RESOLUTION_Y'] == 240

    properties.spacing = 'M'
    assert properties.spacing == 'M'
    assert properties['SPACING'] == 'M'

    properties.average_width = 85
    assert properties.average_width == 85
    assert properties['AVERAGE_WIDTH'] == 85

    properties.charset_registry = 'ISO8859'
    assert properties.charset_registry == 'ISO8859'
    assert properties['CHARSET_REGISTRY'] == 'ISO8859'

    properties.charset_encoding = '1'
    assert properties.charset_encoding == '1'
    assert properties['CHARSET_ENCODING'] == '1'

    assert len(properties) == 14
    properties.generate_xlfd()
    assert properties.font == '-TakWolf Studio-Demo Pixel-Medium-R-Normal-Sans Serif-16-160-75-240-M-85-ISO8859-1'


def test_properties_3():
    properties = PcfProperties()

    properties.font = '-Bitstream-Charter-Medium-R-Normal--12-120-75-75-P-68-ISO8859-1'
    properties.update_by_xlfd()
    assert properties.foundry == 'Bitstream'
    assert properties.family_name == 'Charter'
    assert properties.weight_name == 'Medium'
    assert properties.slant == 'R'
    assert properties.setwidth_name == 'Normal'
    assert properties.add_style_name is None
    assert properties.pixel_size == 12
    assert properties.point_size == 120
    assert properties.resolution_x == 75
    assert properties.resolution_y == 75
    assert properties.spacing == 'P'
    assert properties.average_width == 68
    assert properties.charset_registry == 'ISO8859'
    assert properties.charset_encoding == '1'


def test_properties_4():
    properties = PcfProperties()

    properties.font = '--------------'
    properties.update_by_xlfd()
    assert properties.foundry is None
    assert properties.family_name is None
    assert properties.weight_name is None
    assert properties.slant is None
    assert properties.setwidth_name is None
    assert properties.add_style_name is None
    assert properties.pixel_size is None
    assert properties.point_size is None
    assert properties.resolution_x is None
    assert properties.resolution_y is None
    assert properties.spacing is None
    assert properties.average_width is None
    assert properties.charset_registry is None
    assert properties.charset_encoding is None


def test_properties_5():
    properties = PcfProperties()

    properties.font = 'Bitstream-Charter-Medium-R-Normal--12-120-75-75-P-68-ISO8859-1'
    with pytest.raises(PcfXlfdError) as info:
        properties.update_by_xlfd()
    assert info.value.args[0] == "must start with '-'"


def test_properties_6():
    properties = PcfProperties()

    properties.font = '-Bitstream-Charter-Medium-R-Normal--12-120-75-75-P-68-ISO8859-1-'
    with pytest.raises(PcfXlfdError) as info:
        properties.update_by_xlfd()
    assert info.value.args[0] == 'must contain 14 XLFD fields'


def test_properties_7():
    properties = PcfProperties()

    properties.x_height = 5
    assert properties.x_height == 5
    assert properties['X_HEIGHT'] == 5

    properties.cap_height = 8
    assert properties.cap_height == 8
    assert properties['CAP_HEIGHT'] == 8

    properties.underline_position = -2
    assert properties.underline_position == -2
    assert properties['UNDERLINE_POSITION'] == -2

    properties.underline_thickness = 1
    assert properties.underline_thickness == 1
    assert properties['UNDERLINE_THICKNESS'] == 1

    assert len(properties) == 4


def test_properties_8():
    properties = PcfProperties()

    properties.font_version = '1.0.0'
    assert properties.font_version == '1.0.0'
    assert properties['FONT_VERSION'] == '1.0.0'

    properties.copyright = 'Copyright (c) TakWolf'
    assert properties.copyright == 'Copyright (c) TakWolf'
    assert properties['COPYRIGHT'] == 'Copyright (c) TakWolf'

    properties.notice = 'This is a notice.'
    assert properties.notice == 'This is a notice.'
    assert properties['NOTICE'] == 'This is a notice.'

    assert len(properties) == 3


def test_properties_9():
    properties = PcfProperties()

    properties['abc'] = 'abc'
    assert properties['ABC'] == 'abc'
    assert properties['abc'] == 'abc'


def test_properties_10():
    properties = PcfProperties()

    with pytest.raises(KeyError) as info:
        properties['abc-def'] = 'abcdef'
    assert info.value.args[0] == 'key contain illegal characters'


def test_properties_11():
    properties = PcfProperties()

    properties['NONE_PARAM'] = None
    assert 'NONE_PARAM' not in properties


def test_properties_12():
    properties = PcfProperties()

    with pytest.raises(ValueError) as info:
        properties.foundry = 1
    assert info.value.args[0] == "value of 'FOUNDRY' must be 'str'"

    with pytest.raises(ValueError) as info:
        properties.pixel_size = '1'
    assert info.value.args[0] == "value of 'PIXEL_SIZE' must be 'int'"

    with pytest.raises(ValueError) as info:
        properties['FLOAT_VALUE'] = 1.2
    assert info.value.args[0] == "value must be 'str' or 'int'"


def test_copy():
    properties_1 = PcfProperties(
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
    )
    properties_1.family_name = 'Demo Font'
    properties_1.point_size = 100
    properties_2 = copy(properties_1)
    properties_3 = deepcopy(properties_1)

    assert properties_1 == properties_2
    assert properties_1 == properties_3
    assert properties_1 is not properties_2
    assert properties_1 is not properties_3


def test_eq():
    properties_1 = PcfProperties(
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
    )
    properties_1.family_name = 'Demo Font'
    properties_1.point_size = 100

    properties_2 = PcfProperties(
        table_format=PcfTableFormat.of(True, True, True, 2, 4),
    )
    properties_2.family_name = 'Demo Font'
    properties_2.point_size = 100

    assert properties_1 == properties_2
