from simlab.simulate import (
    simulate_power_conversion,
    simulate_power_mean,
    simulate_type1_error_conversion,
    simulate_type1_error_mean,
    simulate_power_ratio,
    simulate_type1_error_ratio,
)


def test_type1_error_mean_is_reasonable():
    res = simulate_type1_error_mean(
        n_per_group=200,
        mean=0.0,
        standard_deviation=1.0,
        trials=800,
        alpha=0.05,
        seed=0,
    )
    # Type I error should be around alpha; allow a wide tolerance to keep tests stable.
    assert 0.02 <= res.rejection_rate <= 0.08


def test_power_mean_increases_with_effect():
    low = simulate_power_mean(
        n_per_group=200,
        mean_a=0.0,
        mean_b=0.1,
        standard_deviation=1.0,
        trials=800,
        alpha=0.05,
        seed=1,
    )
    high = simulate_power_mean(
        n_per_group=200,
        mean_a=0.0,
        mean_b=0.3,
        standard_deviation=1.0,
        trials=800,
        alpha=0.05,
        seed=1,
    )
    assert high.rejection_rate > low.rejection_rate


def test_type1_error_conversion_is_reasonable():
    res = simulate_type1_error_conversion(
        n_per_group=500,
        conversion_rate=0.08,
        trials=800,
        alpha=0.05,
        seed=2,
    )
    assert 0.02 <= res.rejection_rate <= 0.08


def test_power_conversion_increases_with_lift():
    low = simulate_power_conversion(
        n_per_group=500,
        rate_a=0.08,
        rate_b=0.085,
        trials=800,
        alpha=0.05,
        seed=3,
    )
    high = simulate_power_conversion(
        n_per_group=500,
        rate_a=0.08,
        rate_b=0.095,
        trials=800,
        alpha=0.05,
        seed=3,
    )
    assert high.rejection_rate > low.rejection_rate


def test_type1_error_ratio_is_reasonable():
    res = simulate_type1_error_ratio(
        n_per_group=500,
        purchase_probability=0.05,
        purchase_amount=120.0,
        trials=800,
        alpha=0.05,
        seed=4,
    )
    assert 0.02 <= res.rejection_rate <= 0.08


def test_power_ratio_increases_with_lift():
    low = simulate_power_ratio(
        n_per_group=500,
        purchase_probability_a=0.05,
        purchase_probability_b=0.052,
        purchase_amount=120.0,
        trials=800,
        alpha=0.05,
        seed=5,
    )
    high = simulate_power_ratio(
        n_per_group=500,
        purchase_probability_a=0.05,
        purchase_probability_b=0.06,
        purchase_amount=120.0,
        trials=800,
        alpha=0.05,
        seed=5,
    )
    assert high.rejection_rate > low.rejection_rate
