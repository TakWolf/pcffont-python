from copy import copy, deepcopy

from pcffont import PcfTableFormat, PcfMetric, PcfMetrics


def test_copy():
    metrics_1 = PcfMetrics(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        metrics=[
            PcfMetric(1, 2, 3, 4, 5, 6),
            PcfMetric(6, 5, 4, 3, 2, 1),
        ],
    )
    metrics_2 = copy(metrics_1)

    assert metrics_1 == metrics_2
    assert metrics_1 is not metrics_2
    assert metrics_1.table_format is metrics_2.table_format

    for metric_1, metric_2 in zip(metrics_1, metrics_2):
        assert metric_1 is metric_2


def test_deepcopy():
    metrics_1 = PcfMetrics(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        metrics=[
            PcfMetric(1, 2, 3, 4, 5, 6),
            PcfMetric(6, 5, 4, 3, 2, 1),
        ],
    )
    metrics_2 = deepcopy(metrics_1)

    assert metrics_1 == metrics_2
    assert metrics_1 is not metrics_2
    assert metrics_1.table_format is not metrics_2.table_format

    for metric_1, metric_2 in zip(metrics_1, metrics_2):
        assert metric_1 is not metric_2


def test_eq():
    metrics_1 = PcfMetrics(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        metrics=[
            PcfMetric(1, 2, 3, 4, 5, 6),
            PcfMetric(6, 5, 4, 3, 2, 1),
        ],
    )
    metrics_2 = PcfMetrics(
        table_format=PcfTableFormat(True, True, True, 1, 2),
        metrics=[
            PcfMetric(1, 2, 3, 4, 5, 6),
            PcfMetric(6, 5, 4, 3, 2, 1),
        ],
    )
    assert metrics_1 == metrics_2
