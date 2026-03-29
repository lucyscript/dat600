from dat600_assignment.report import render_org


def test_report_renders_org_from_verified_results() -> None:
    report = render_org()

    assert report.startswith("#+TITLE: DAT600 Assignment 3-4 Solution")
    assert "* Problem Cable Network" in report
    assert r"The MST has cost \( 26 \)" in report
    assert r"The budget \(30\) is not achievable." in report
    assert r"The maximum flow is \( 30 \)." in report
