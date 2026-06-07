from copy import copy, deepcopy

from pcffont import PcfTableFormat, PcfMetric, PcfAccelerators


def test_no_bounds():
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


def test_no_overlap_false():
    accelerators = PcfAccelerators(
        max_overlap=5,
        min_bounds=PcfMetric(left_side_bearing=-2),
        max_bounds=PcfMetric(),
    )
    accelerators.calculate_bounds()
    assert not accelerators.no_overlap


def test_no_overlap_true():
    accelerators = PcfAccelerators(
        max_overlap=-1,
        min_bounds=PcfMetric(),
        max_bounds=PcfMetric(),
    )
    accelerators.calculate_bounds()
    assert accelerators.no_overlap


def test_constant_metrics_true_terminal_false():
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


def test_terminal_font_true():
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


def test_constant_width_false():
    accelerators = PcfAccelerators(
        min_bounds=PcfMetric(character_width=5),
        max_bounds=PcfMetric(character_width=7),
    )
    accelerators.calculate_bounds()
    assert not accelerators.constant_width


def test_constant_width_true():
    accelerators = PcfAccelerators(
        min_bounds=PcfMetric(character_width=5),
        max_bounds=PcfMetric(character_width=5),
    )
    accelerators.calculate_bounds()
    assert accelerators.constant_width


def test_ink_inside_all_conditions_met():
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


def test_ink_inside_false_max_overlap_positive():
    accelerators = PcfAccelerators(
        max_overlap=1,
        min_bounds=PcfMetric(),
        max_bounds=PcfMetric(),
    )
    accelerators.calculate_bounds()
    assert not accelerators.ink_inside


def test_ink_inside_false_ascent_exceeds():
    accelerators = PcfAccelerators(
        font_ascent=10,
        font_descent=5,
        min_bounds=PcfMetric(ascent=12),
        max_bounds=PcfMetric(ascent=12),
    )
    accelerators.calculate_bounds()
    assert not accelerators.ink_inside


def test_ink_inside_false_descent_exceeds():
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


def test_ink_inside_false_negative_ascent_below_negative_font_descent():
    accelerators = PcfAccelerators(
        font_ascent=10,
        font_descent=5,
        min_bounds=PcfMetric(ascent=-6),
        max_bounds=PcfMetric(),
    )
    accelerators.calculate_bounds()
    assert not accelerators.ink_inside


def test_calculate_bounds_resets_when_different():
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

    accelerators_2 = accelerators_1.deepcopy()
    assert accelerators_1 == accelerators_2
    assert accelerators_1 is not accelerators_2
    assert accelerators_1.table_format is not accelerators_2.table_format
    assert accelerators_1.min_bounds is not accelerators_2.min_bounds
    assert accelerators_1.max_bounds is not accelerators_2.max_bounds
    assert accelerators_1.ink_min_bounds is not accelerators_2.ink_min_bounds
    assert accelerators_1.ink_max_bounds is not accelerators_2.ink_max_bounds

    accelerators_3 = copy(accelerators_1)
    assert accelerators_1 == accelerators_3
    assert accelerators_1 is not accelerators_3
    assert accelerators_1.table_format is accelerators_3.table_format
    assert accelerators_1.min_bounds is accelerators_3.min_bounds
    assert accelerators_1.max_bounds is accelerators_3.max_bounds
    assert accelerators_1.ink_min_bounds is accelerators_3.ink_min_bounds
    assert accelerators_1.ink_max_bounds is accelerators_3.ink_max_bounds

    accelerators_4 = deepcopy(accelerators_1)
    assert accelerators_1 == accelerators_4
    assert accelerators_1 is not accelerators_4
    assert accelerators_1.table_format is not accelerators_4.table_format
    assert accelerators_1.min_bounds is not accelerators_4.min_bounds
    assert accelerators_1.max_bounds is not accelerators_4.max_bounds
    assert accelerators_1.ink_min_bounds is not accelerators_4.ink_min_bounds
    assert accelerators_1.ink_max_bounds is not accelerators_4.ink_max_bounds
