from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ProportionInterval:
    """
    Confidence interval for a proportion.

    estimate:
        Point estimate of the proportion.

    low, high:
        Lower and upper bounds of the confidence interval.
    """

    estimate: float
    low: float
    high: float


def _normal_inverse_cdf(p: float) -> float:
    """
    Approximate inverse CDF for a standard normal distribution.

    This matches the style used in your other repos and is accurate enough
    for confidence intervals and planning utilities.
    """
    if not (0.0 < p < 1.0):
        raise ValueError("p must be between 0 and 1 (exclusive).")

    a = [
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    ]
    b = [
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e00,
        3.754408661907416e00,
    ]

    plow = 0.02425
    phigh = 1.0 - plow

    if p < plow:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0
        )

    if p > phigh:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(
            (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
            / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
        )

    q = p - 0.5
    r = q * q
    return (
        (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q
    ) / ((((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0))


def wilson_interval(
    successes: int, trials: int, *, confidence: float = 0.95
) -> ProportionInterval:
    """
    Wilson score interval for a binomial proportion.

    In our simulation setting:
    - trials = number of simulated experiments
    - successes = number of trials where p_value < alpha

    The estimate is:
        p_hat = successes / trials

    We also want an interval that reflects Monte Carlo sampling uncertainty.
    A rejection rate is a proportion, so a binomial model is a reasonable approximation.

    The Wilson interval behaves well even when the estimate is near 0 or 1,
    and it tends to perform better than the basic "p ± z * sqrt(p(1-p)/n)" interval.

    Returns a ProportionInterval (estimate, low, high).
    """
    if trials <= 0:
        raise ValueError("trials must be positive.")
    if successes < 0 or successes > trials:
        raise ValueError("successes must be between 0 and trials.")
    if confidence <= 0.0 or confidence >= 1.0:
        raise ValueError("confidence must be between 0 and 1 (exclusive).")

    z = _normal_inverse_cdf(0.5 + confidence / 2.0)
    n = float(trials)
    phat = successes / n

    denom = 1.0 + (z**2) / n
    center = (phat + (z**2) / (2.0 * n)) / denom
    half_width = (z / denom) * math.sqrt(
        (phat * (1.0 - phat) / n) + ((z**2) / (4.0 * n * n))
    )

    low = max(0.0, center - half_width)
    high = min(1.0, center + half_width)
    return ProportionInterval(estimate=phat, low=low, high=high)
