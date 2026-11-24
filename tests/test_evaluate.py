"""Sanity checks for evaluate.py. Run: python tests/test_evaluate.py [path or Hub id of the dataset]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import evaluate  # noqa: E402

DATA = sys.argv[1] if len(sys.argv) > 1 else evaluate.DATASET


def test_gold_as_prediction():
    for split in ("test", "control"):
        letters = evaluate.load_letters(DATA, split)
        res = evaluate.evaluate(letters, {x["id"]: [s[:2] for s in x["spans"]] for x in letters}, ci=False)
        assert res["char_f1"] == 1.0 and res["leak_rate"] == 0.0, res
        assert all(v == 1.0 for v in res["recall_by_family"].values())


def test_empty_prediction():
    letters = evaluate.load_letters(DATA, "test")
    res = evaluate.evaluate(letters, {}, ci=False)
    assert res["char_r"] == 0.0 and res["leak_rate"] == 1.0, res


def test_half_rule():
    # one name of 10 characters: 5 redacted characters find it, 4 do not
    letter = {"id": "x", "language": "en", "text": "Dr. Ann Smithy wrote.", "spans": [(4, 14, "names", True)]}
    assert not evaluate.score_letter(letter, [(4, 9)])["leak"]
    assert evaluate.score_letter(letter, [(4, 8)])["leak"]


if __name__ == "__main__":
    test_gold_as_prediction(); test_empty_prediction(); test_half_rule()
    print("all checks passed")
