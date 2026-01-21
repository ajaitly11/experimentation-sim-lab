from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

from simlab.simulate import (
    simulate_power_conversion,
    simulate_power_mean,
    simulate_power_ratio,
    simulate_type1_error_conversion,
    simulate_type1_error_mean,
    simulate_type1_error_ratio,
)


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def run_sweep_to_csv(
    *,
    output_path: str,
    trials: int,
    alpha: float,
    sample_sizes: Sequence[int],
    seed_base: int = 0,
) -> None:
    """
    Run a small sweep across sample sizes and write results to a CSV file.

    This is meant to be:
    - reproducible
    - readable
    - easy to share

    Each row corresponds to one simulated setting and reports the rejection rate.
    """
    out = Path(output_path)
    _ensure_parent(out)

    rows: List[dict] = []

    for i, n in enumerate(sample_sizes):
        # Mean metric settings
        mean_t1 = simulate_type1_error_mean(
            n_per_group=n,
            mean=0.0,
            standard_deviation=1.0,
            trials=trials,
            alpha=alpha,
            seed=seed_base + 10_000 + i,
        )
        mean_pw = simulate_power_mean(
            n_per_group=n,
            mean_a=0.0,
            mean_b=0.3,
            standard_deviation=1.0,
            trials=trials,
            alpha=alpha,
            seed=seed_base + 20_000 + i,
        )

        # Conversion settings
        conv_t1 = simulate_type1_error_conversion(
            n_per_group=n,
            conversion_rate=0.08,
            trials=trials,
            alpha=alpha,
            seed=seed_base + 30_000 + i,
        )
        conv_pw = simulate_power_conversion(
            n_per_group=n,
            rate_a=0.08,
            rate_b=0.095,
            trials=trials,
            alpha=alpha,
            seed=seed_base + 40_000 + i,
        )

        # Ratio settings (revenue per visitor)
        ratio_t1 = simulate_type1_error_ratio(
            n_per_group=n,
            purchase_probability=0.05,
            purchase_amount=120.0,
            trials=trials,
            alpha=alpha,
            seed=seed_base + 50_000 + i,
        )
        ratio_pw = simulate_power_ratio(
            n_per_group=n,
            purchase_probability_a=0.05,
            purchase_probability_b=0.06,
            purchase_amount=120.0,
            trials=trials,
            alpha=alpha,
            seed=seed_base + 60_000 + i,
        )

        rows.append(
            {
                "n_per_group": n,
                "alpha": alpha,
                "trials": trials,
                "type1_mean": mean_t1.rejection_rate,
                "power_mean": mean_pw.rejection_rate,
                "type1_conversion": conv_t1.rejection_rate,
                "power_conversion": conv_pw.rejection_rate,
                "type1_ratio": ratio_t1.rejection_rate,
                "power_ratio": ratio_pw.rejection_rate,
            }
        )

    fieldnames = list(rows[0].keys())
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def main() -> None:
    """
    Default sweep used for quick sanity checks.

    This keeps runtime modest so it can be run locally and in CI if needed.
    """
    run_sweep_to_csv(
        output_path="results/sweep.csv",
        trials=1000,
        alpha=0.05,
        sample_sizes=[100, 200, 500, 1000],
        seed_base=0,
    )
    print("Wrote results/sweep.csv")


if __name__ == "__main__":
    main()