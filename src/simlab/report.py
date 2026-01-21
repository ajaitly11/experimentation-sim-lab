from __future__ import annotations


from simlab.simulate import (
    simulate_power_conversion,
    simulate_power_mean,
    simulate_power_ratio,
    simulate_type1_error_conversion,
    simulate_type1_error_mean,
    simulate_type1_error_ratio,
)
from simlab.intervals import wilson_interval


def _fmt(x: float) -> str:
    return f"{x:.3f}"


def _fmt_interval(successes: int, trials: int) -> str:
    iv = wilson_interval(successes, trials, confidence=0.95)
    return f"{iv.estimate:.3f} (95% CI {iv.low:.3f} to {iv.high:.3f})"


def print_report() -> None:
    print("Experimentation Simulation Report")
    print("--------------------------------")
    print("This script runs a few small simulations and prints rejection rates.")
    print("Under no effect: rejection rate approximates Type I error.")
    print("Under a real effect: rejection rate approximates power.")
    print()

    alpha = 0.05
    trials = 2000

    print("Mean metric (normal data)")
    t1 = simulate_type1_error_mean(
        n_per_group=200,
        mean=0.0,
        standard_deviation=1.0,
        trials=trials,
        alpha=alpha,
        seed=0,
    )
    pw = simulate_power_mean(
        n_per_group=200,
        mean_a=0.0,
        mean_b=0.3,
        standard_deviation=1.0,
        trials=trials,
        alpha=alpha,
        seed=1,
    )
    print("  Type I error:", _fmt_interval(t1.successes, t1.trials))
    print("  Power:", _fmt(pw.rejection_rate))
    print()

    print("Conversion metric (Bernoulli)")
    t1c = simulate_type1_error_conversion(
        n_per_group=500,
        conversion_rate=0.08,
        trials=trials,
        alpha=alpha,
        seed=2,
    )
    pwc = simulate_power_conversion(
        n_per_group=500,
        rate_a=0.08,
        rate_b=0.095,
        trials=trials,
        alpha=alpha,
        seed=3,
    )
    print("  Type I error:", _fmt_interval(t1c.successes, t1c.trials))
    print("  Power:", _fmt(pwc.rejection_rate))
    print()

    print("Ratio metric (revenue per visitor)")
    t1r = simulate_type1_error_ratio(
        n_per_group=500,
        purchase_probability=0.05,
        purchase_amount=120.0,
        trials=trials,
        alpha=alpha,
        seed=4,
    )
    pwr = simulate_power_ratio(
        n_per_group=500,
        purchase_probability_a=0.05,
        purchase_probability_b=0.06,
        purchase_amount=120.0,
        trials=trials,
        alpha=alpha,
        seed=5,
    )
    print("  Type I error:", _fmt_interval(t1r.successes, t1r.trials))
    print("  Power:", _fmt(pwr.rejection_rate))
    print()


if __name__ == "__main__":
    print_report()
