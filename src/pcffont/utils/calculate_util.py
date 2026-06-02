from collections.abc import Iterable

from pcffont.metric import PcfMetric


def calculate_max_overlap(metrics: Iterable[PcfMetric]) -> int:
    return max((metric.right_side_bearing - metric.character_width for metric in metrics), default=0)


def calculate_min_bounds(metrics: Iterable[PcfMetric]) -> PcfMetric:
    min_bounds = None
    for metric in metrics:
        if min_bounds is None:
            min_bounds = PcfMetric(
                metric.left_side_bearing,
                metric.right_side_bearing,
                metric.character_width,
                metric.ascent,
                metric.descent,
                metric.attributes,
            )
        else:
            if metric.left_side_bearing != 0 or metric.right_side_bearing != 0 or metric.character_width != 0 or metric.ascent != 0 or metric.descent != 0:
                min_bounds.left_side_bearing = min(min_bounds.left_side_bearing, metric.left_side_bearing)
                min_bounds.right_side_bearing = min(min_bounds.right_side_bearing, metric.right_side_bearing)
                min_bounds.character_width = min(min_bounds.character_width, metric.character_width)
                min_bounds.ascent = min(min_bounds.ascent, metric.ascent)
                min_bounds.descent = min(min_bounds.descent, metric.descent)
            min_bounds.attributes &= metric.attributes
    if min_bounds is None:
        min_bounds = PcfMetric()
    return min_bounds


def calculate_max_bounds(metrics: Iterable[PcfMetric]) -> PcfMetric:
    max_bounds = None
    for metric in metrics:
        if max_bounds is None:
            max_bounds = PcfMetric(
                metric.left_side_bearing,
                metric.right_side_bearing,
                metric.character_width,
                metric.ascent,
                metric.descent,
                metric.attributes,
            )
        else:
            if metric.left_side_bearing != 0 or metric.right_side_bearing != 0 or metric.character_width != 0 or metric.ascent != 0 or metric.descent != 0:
                max_bounds.left_side_bearing = max(max_bounds.left_side_bearing, metric.left_side_bearing)
                max_bounds.right_side_bearing = max(max_bounds.right_side_bearing, metric.right_side_bearing)
                max_bounds.character_width = max(max_bounds.character_width, metric.character_width)
                max_bounds.ascent = max(max_bounds.ascent, metric.ascent)
                max_bounds.descent = max(max_bounds.descent, metric.descent)
            max_bounds.attributes |= metric.attributes
    if max_bounds is None:
        max_bounds = PcfMetric()
    return max_bounds
