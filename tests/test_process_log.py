import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from process_log import compute_new_data, process


@pytest.mark.parametrize(
    "line, line_number, expected",
    [
        ('{"a": 1}', 0, "Multiple of 5"),
        ("anything.", 5, "Multiple of 5"),
        ("with $ sign", 10, "Multiple of 5"),
        ("Process 9000 suc$esfully run", 1, "Process_9000_suc$esfully_run"),
        ("$ ends.", 1, "$_ends."),
        ("Process 498758 succesfully run.\n", 1, "Process 498758 succesfully run."),
        ("done.\r\n", 2, "done."),
        ("Match 3341 has finished", 1, "Nothing to display"),
        ("Match 444 has fin#shed", 2, "Nothing to display"),
        ('"{"player": "Cavani"}."', 1, "Nothing to display"),
        ('{"key": invalid}', 1, "Nothing to display"),
        ("{not json at all", 3, "Nothing to display"),
    ],
)
def test_compute_new_data(line: str, line_number: int, expected: str) -> None:
    assert compute_new_data(line, line_number) == expected


def test_json_rule_even_true_preserves_unicode() -> None:
    out = compute_new_data('{"player": "Mbappé"}', 2)
    assert json.loads(out) == {"player": "Mbappé", "even": True}
    assert "Mbappé" in out


def test_json_rule_even_false() -> None:
    out = compute_new_data('{"player": "Ramos"}', 3)
    assert json.loads(out) == {"player": "Ramos", "even": False}


def test_process_end_to_end(tmp_path: Path) -> None:
    log = tmp_path / "sample.log"
    log.write_text(
        'first line\n{"x": 1}\nends.\n',
        encoding="utf-8",
    )
    assert list(process(log)) == [
        "0 : Multiple of 5",
        '1 : {"x": 1, "even": false}',
        "2 : ends.",
    ]
