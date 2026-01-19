from simlab.report import print_report


def test_report_runs_without_error(capsys):
    print_report()
    out = capsys.readouterr().out
    assert "Experimentation Simulation Report" in out