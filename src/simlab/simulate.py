from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

from abtk import conversion_diff, mean_diff


@dataclass(frozen=True)
class SimulationResult:
    """
    Summary of a Monte Carlo simulation.

    trials:
        How many simulated experiments were run.

    alpha:
        The p-value threshold used for "statistical significance".

    rejection_rate:
        Fraction of trials where p_value < alpha.

        - Under the null hypothesis (no real effect), this estimates the Type I error rate.
        - Under a real effect, this estimates the power.
    """

    trials: int
    alpha: float
    rejection_rate: float


def _run_trials(
    p_value_fn: Callable[[random.Random], float],
    *,
    trials: int,
    alpha: float,
    seed: int,
) -> SimulationResult:
    rng = random.Random(seed)
    rejections = 0

    for _ in range(trials):
        p = p_value_fn(rng)
        if p < alpha:
            rejections += 1

    return SimulationResult(
        trials=trials, alpha=alpha, rejection_rate=rejections / trials
    )


def simulate_type1_error_mean(
    *,
    n_per_group: int,
    mean: float,
    standard_deviation: float,
    trials: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> SimulationResult:
    """
    Estimate Type I error for the mean test under no real effect.

    We generate both groups from the same distribution (same mean and standard deviation).
    Any "significant" result is a false positive.
    """

    def one_trial(rng: random.Random) -> float:
        a = [rng.gauss(mean, standard_deviation) for _ in range(n_per_group)]
        b = [rng.gauss(mean, standard_deviation) for _ in range(n_per_group)]
        res = mean_diff(a, b, alpha=alpha)
        return float(res.p_value)

    return _run_trials(one_trial, trials=trials, alpha=alpha, seed=seed)


def simulate_power_mean(
    *,
    n_per_group: int,
    mean_a: float,
    mean_b: float,
    standard_deviation: float,
    trials: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> SimulationResult:
    """
    Estimate power for the mean test under a real effect (mean_b - mean_a).
    """

    def one_trial(rng: random.Random) -> float:
        a = [rng.gauss(mean_a, standard_deviation) for _ in range(n_per_group)]
        b = [rng.gauss(mean_b, standard_deviation) for _ in range(n_per_group)]
        res = mean_diff(a, b, alpha=alpha)
        return float(res.p_value)

    return _run_trials(one_trial, trials=trials, alpha=alpha, seed=seed)


def simulate_type1_error_conversion(
    *,
    n_per_group: int,
    conversion_rate: float,
    trials: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> SimulationResult:
    """
    Estimate Type I error for the conversion test under no real effect.

    Both groups have the same true conversion probability.
    """

    def one_trial(rng: random.Random) -> float:
        a = [1 if rng.random() < conversion_rate else 0 for _ in range(n_per_group)]
        b = [1 if rng.random() < conversion_rate else 0 for _ in range(n_per_group)]
        res = conversion_diff(a, b, alpha=alpha)
        return float(res.p_value)

    return _run_trials(one_trial, trials=trials, alpha=alpha, seed=seed)


def simulate_power_conversion(
    *,
    n_per_group: int,
    rate_a: float,
    rate_b: float,
    trials: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> SimulationResult:
    """
    Estimate power for the conversion test when rate_b differs from rate_a.
    """

    def one_trial(rng: random.Random) -> float:
        a = [1 if rng.random() < rate_a else 0 for _ in range(n_per_group)]
        b = [1 if rng.random() < rate_b else 0 for _ in range(n_per_group)]
        res = conversion_diff(a, b, alpha=alpha)
        return float(res.p_value)

    return _run_trials(one_trial, trials=trials, alpha=alpha, seed=seed)
