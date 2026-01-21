from pathlib import Path

from simlab.sweep import run_sweep_to_csv


def test_run_sweep_to_csv_writes_file(tmp_path: Path):
    out = tmp_path / "sweep.csv"
    run_sweep_to_csv(
        output_path=str(out),
        trials=200,
        alpha=0.05,
        sample_sizes=[50, 100],
        seed_base=123,
    )
    assert out.exists()
    text = out.read_text()
    assert "n_per_group" in text
    assert "power_conversion" in text
