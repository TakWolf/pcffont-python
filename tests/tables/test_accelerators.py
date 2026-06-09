from copy import copy, deepcopy

from pcffont import PcfTableFormat, PcfMetric, PcfAccelerators


def test_calculate_bounds_1():
    accelerators = PcfAccelerators(
        no_overlap=True,
        constant_metrics=True,
        terminal_font=True,
        constant_width=True,
        ink_inside=True,
    )
    accelerators.calculate_bounds()
    assert accelerators.no_overlap
    assert accelerators.constant_metrics
    assert accelerators.terminal_font
    assert accelerators.constant_width
    assert accelerators.ink_inside


def test_calculate_bounds_2():
    accelerators = PcfAccelerators(
        max_overlap=5,
        min_bounds=PcfMetric(left_side_bearing=-2),
        max_bounds=PcfMetric(),
    )
    accelerators.calculate_bounds()
    assert not accelerators.no_overlap


def test_calculate_bounds_3():
    accelerators = PcfAccelerators(
        max_overlap=-1,
        min_bounds=PcfMetric(),
        max_bounds=PcfMetric(),
    )
    accelerators.calculate_bounds()
    assert accelerators.no_overlap


def test_calculate_bounds_4():
    accelerators = PcfAccelerators(
        font_ascent=12,
        font_descent=4,
        min_bounds=PcfMetric(
            left_side_bearing=1, 
            right_side_bearing=5,
            character_width=6,
            ascent=10, 
            descent=3,
        ),
        max_bounds=PcfMetric(
            left_side_bearing=1, 
            right_side_bearing=5,
            character_width=6, 
            ascent=10, 
            descent=3,
        ),
    )
    accelerators.calculate_bounds()
    assert accelerators.constant_metrics
    assert not accelerators.terminal_font
    assert accelerators.constant_width


def test_calculate_bounds_5():
    accelerators = PcfAccelerators(
        font_ascent=8,
        font_descent=2,
        min_bounds=PcfMetric(
            right_side_bearing=10,
            character_width=10,
            ascent=8,
            descent=2,
        ),
        max_bounds=PcfMetric(
            right_side_bearing=10,
            character_width=10,
            ascent=8,
            descent=2,
        ),
    )
    accelerators.calculate_bounds()
    assert accelerators.constant_metrics
    assert accelerators.terminal_font
    assert accelerators.constant_width


def test_calculate_bounds_6():
    accelerators = PcfAccelerators(
        min_bounds=PcfMetric(character_width=5),
        max_bounds=PcfMetric(character_width=7),
    )
    accelerators.calculate_bounds()
    assert not accelerators.constant_width


def test_calculate_bounds_7():
    accelerators = PcfAccelerators(
        min_bounds=PcfMetric(character_width=5),
        max_bounds=PcfMetric(character_width=5),
    )
    accelerators.calculate_bounds()
    assert accelerators.constant_width


def test_calculate_bounds_8():
    accelerators = PcfAccelerators(
        font_ascent=12,
        font_descent=5,
        min_bounds=PcfMetric(
            ascent=10,
            descent=3,
        ),
        max_bounds=PcfMetric(
            ascent=12,
            descent=5,
        ),
    )
    accelerators.calculate_bounds()
    assert accelerators.ink_inside


def test_calculate_bounds_9():
    accelerators = PcfAccelerators(
        max_overlap=1,
        min_bounds=PcfMetric(),
        max_bounds=PcfMetric(),
    )
    accelerators.calculate_bounds()
    assert not accelerators.ink_inside


def test_calculate_bounds_10():
    accelerators = PcfAccelerators(
        font_ascent=10,
        font_descent=5,
        min_bounds=PcfMetric(ascent=12),
        max_bounds=PcfMetric(ascent=12),
    )
    accelerators.calculate_bounds()
    assert not accelerators.ink_inside


def test_calculate_bounds_11():
    accelerators = PcfAccelerators(
        font_ascent=10,
        font_descent=5,
        min_bounds=PcfMetric(
            ascent=8,
            descent=4,
        ),
        max_bounds=PcfMetric(
            ascent=10,
            descent=6,
        ),
    )
    accelerators.calculate_bounds()
    assert not accelerators.ink_inside


def test_calculate_bounds_12():
    accelerators = PcfAccelerators(
        font_ascent=10,
        font_descent=5,
        min_bounds=PcfMetric(ascent=-6),
        max_bounds=PcfMetric(),
    )
    accelerators.calculate_bounds()
    assert not accelerators.ink_inside


def test_calculate_bounds_13():
    accelerators = PcfAccelerators(
        constant_metrics=True,
        terminal_font=True,
        min_bounds=PcfMetric(left_side_bearing=1),
        max_bounds=PcfMetric(left_side_bearing=2),
    )
    accelerators.calculate_bounds()
    assert not accelerators.constant_metrics
    assert not accelerators.terminal_font


def test_copy():
    accelerators_1 = PcfAccelerators(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        no_overlap=True,
        constant_metrics=True,
        terminal_font=True,
        constant_width=True,
        ink_inside=True,
        ink_metrics=True,
        draw_right_to_left=True,
        font_ascent=1,
        font_descent=2,
        max_overlap=4,
        min_bounds=PcfMetric(1, 2, 3, 4, 5, 6),
        max_bounds=PcfMetric(6, 5, 4, 3, 2, 1),
        ink_min_bounds=PcfMetric(7, 8, 9, 10, 11, 12),
        ink_max_bounds=PcfMetric(12, 11, 10, 9, 8, 7),
    )
    accelerators_2 = copy(accelerators_1)

    assert accelerators_1 == accelerators_2
    assert accelerators_1 is not accelerators_2
    assert accelerators_1.table_format is accelerators_2.table_format
    assert accelerators_1.min_bounds is accelerators_2.min_bounds
    assert accelerators_1.max_bounds is accelerators_2.max_bounds
    assert accelerators_1.ink_min_bounds is accelerators_2.ink_min_bounds
    assert accelerators_1.ink_max_bounds is accelerators_2.ink_max_bounds


def test_deepcopy():
    accelerators_1 = PcfAccelerators(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        no_overlap=True,
        constant_metrics=True,
        terminal_font=True,
        constant_width=True,
        ink_inside=True,
        ink_metrics=True,
        draw_right_to_left=True,
        font_ascent=1,
        font_descent=2,
        max_overlap=4,
        min_bounds=PcfMetric(1, 2, 3, 4, 5, 6),
        max_bounds=PcfMetric(6, 5, 4, 3, 2, 1),
        ink_min_bounds=PcfMetric(7, 8, 9, 10, 11, 12),
        ink_max_bounds=PcfMetric(12, 11, 10, 9, 8, 7),
    )
    accelerators_2 = deepcopy(accelerators_1)

    assert accelerators_1 == accelerators_2
    assert accelerators_1 is not accelerators_2
    assert accelerators_1.table_format is not accelerators_2.table_format
    assert accelerators_1.min_bounds is not accelerators_2.min_bounds
    assert accelerators_1.max_bounds is not accelerators_2.max_bounds
    assert accelerators_1.ink_min_bounds is not accelerators_2.ink_min_bounds
    assert accelerators_1.ink_max_bounds is not accelerators_2.ink_max_bounds


def test_eq():
    accelerators_1 = PcfAccelerators(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        no_overlap=True,
        constant_metrics=True,
        terminal_font=True,
        constant_width=True,
        ink_inside=True,
        ink_metrics=True,
        draw_right_to_left=True,
        font_ascent=1,
        font_descent=2,
        max_overlap=4,
        min_bounds=PcfMetric(1, 2, 3, 4, 5, 6),
        max_bounds=PcfMetric(6, 5, 4, 3, 2, 1),
        ink_min_bounds=PcfMetric(7, 8, 9, 10, 11, 12),
        ink_max_bounds=PcfMetric(12, 11, 10, 9, 8, 7),
    )
    accelerators_2 = PcfAccelerators(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        no_overlap=True,
        constant_metrics=True,
        terminal_font=True,
        constant_width=True,
        ink_inside=True,
        ink_metrics=True,
        draw_right_to_left=True,
        font_ascent=1,
        font_descent=2,
        max_overlap=4,
        min_bounds=PcfMetric(1, 2, 3, 4, 5, 6),
        max_bounds=PcfMetric(6, 5, 4, 3, 2, 1),
        ink_min_bounds=PcfMetric(7, 8, 9, 10, 11, 12),
        ink_max_bounds=PcfMetric(12, 11, 10, 9, 8, 7),
    )
    assert accelerators_1 == accelerators_2
