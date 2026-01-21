from simlab.intervals import wilson_interval


def test_wilson_interval_basic_properties():
    iv = wilson_interval(successes=50, trials=100, confidence=0.95)
    assert 0.0 <= iv.low <= iv.estimate <= iv.high <= 1.0


def test_wilson_interval_extremes():
    iv0 = wilson_interval(successes=0, trials=100, confidence=0.95)
    assert iv0.low == 0.0
    assert iv0.high > 0.0

    iv1 = wilson_interval(successes=100, trials=100, confidence=0.95)
    assert iv1.high == 1.0
    assert iv1.low < 1.0