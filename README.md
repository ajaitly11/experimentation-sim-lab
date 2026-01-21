# Experimentation Simulation Lab

This repository is a small “simulation lab” for validating A/B testing methods.

It answers questions like:
- Do our tests have the false positive rate we expect?
- How much power do we have to detect a realistic effect?
- How do sample size, noise, and effect size change the results?

These are practical questions in experimentation platforms, because analytical formulas
are often based on approximations. Simulation gives a direct way to check behaviour.

---

## What is Type I error?

Type I error is a false positive.

If there is truly no difference between A and B, but our analysis reports a statistically
significant result, that is a Type I error.

If we use `alpha = 0.05`, we are saying:
- “In the long run, I am willing to accept about a 5% false positive rate.”

A good testing method should produce a Type I error rate close to alpha when the null is true.

---

## What is power?

Power is the probability that we detect a real effect.

If B truly improves a metric, power answers:
- “How often will we actually detect that improvement as significant?”

A common target is 80% power. That is not a law, but it is a widely used baseline.

---

## How this repo works

This repo calls functions from the [A/B Experimentation Toolkit](https://github.com/ajaitly11/ab-experimentation-toolkit)  and runs many simulated experiments using Monte Carlo simulation.

Each simulation:
1) generates random data for group A and group B,
2) runs the corresponding A/B test function,
3) records whether the p-value is below alpha,
4) repeats this many times and reports the rejection rate.

Under no real effect:
- rejection rate ≈ Type I error

Under a real effect:
- rejection rate ≈ power

---

## Setup

This repo uses Python 3.10+.

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
pip install pytest ruff black pre-commit
```

This repo depends on [abtk](https://github.com/ajaitly11/ab-experimentation-toolkit).
If you have the ab-experimentation-toolkit repo next to this one:

```bash
pip install -e ../ab-experimentation-toolkit
```

Run tests:

```bash
pytest
```

Run checks:

```bash
ruff check .
black --check .
```

---

Example: Type I error for a mean test

```python
from simlab.simulate import simulate_type1_error_mean

result = simulate_type1_error_mean(
    n_per_group=200,
    mean=0.0,
    standard_deviation=1.0,
    trials=2000,
    alpha=0.05,
    seed=0,
)

print(result)
```
If the method behaves as expected, the rejection rate will be close to 0.05.

---

Example: Power for a conversion test

from simlab.simulate import simulate_power_conversion

```python
result = simulate_power_conversion(
    n_per_group=500,
    rate_a=0.08,
    rate_b=0.095,
    trials=2000,
    alpha=0.05,
    seed=1,
)

print(result)
```

If the effect is large enough (and the sample size is large enough),
the rejection rate will be meaningfully higher than 0.05.

---

## Mini report script

You can run a small set of simulations and print a compact summary:

```bash
python -m simlab.report
```
This prints Type I error and power estimates for:
	- a mean metric
	- a conversion metric
	- a ratio metric (revenue per visitor)

## Parameter sweep (power and Type I error across sample sizes)

You can run a small sweep across sample sizes and write results to a CSV file:

```bash
python -m simlab.sweep
```

This writes:
	-	results/sweep.csv

The CSV contains one row per sample size and reports:
	-	estimated Type I error (under no real effect)
	-	estimated power (under a real effect)

How to interpret-the output
	-	Under no real effect, the rejection rate should be close to alpha (for example, ~0.05).
If it is much higher, the test is too “eager” and produces too many false positives.
If it is much lower, the test is overly conservative.
	-	Under a real effect, the rejection rate is the estimated power.
Power should generally increase as sample size increases.

This is a practical way to sanity-check the behaviour of a testing method without relying
only on theory.

## Why confidence intervals appear in simulation output

A simulation estimate like “power = 0.62” is based on a finite number of trials.
If you re-run the simulation with a different random seed, the estimate will move a bit.

A rejection rate is a proportion:
- each trial either rejects (p-value < alpha) or does not reject
- across many trials we count rejections and divide by the number of trials

This makes it natural to report a confidence interval for the proportion.
The report script uses a Wilson interval, which behaves well even when the estimate is near 0 or 1.
