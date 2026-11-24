"""Score de-identification predictions on the multilingual clinical de-identification benchmark.

A prediction file is JSON lines, one letter per line:
    {"split": "test", "id": "de-k0012", "spans": [[start, end], ...]}
Spans are character offsets into the letter text. Labels are not needed: the benchmark only asks
whether a character was redacted. Letters without a line count as "nothing redacted".

    python evaluate.py baselines/*.jsonl --out results.json

Splits: "train", "dev", "test" (main letters) and "control" (the control letters of the test cases).
"""
import argparse
import json
import os
import random

import pandas as pd

DATASET = "LukasKunhardt/multilingual-clinical-deid-benchmark"
FAMILIES = ["names", "ids", "contact", "locations", "dates", "age"]


def gold_span(text, start, end, label):
    """(start, end, family, direct). Direct identifiers expose a person on their own and decide the leak rate."""
    if label == "LOCATION":
        s = text[start:end]
        # a street has a house number and lower-case letters; postcodes such as "LT-13031" or "D02 X285" do not
        street = any(c.isdigit() for c in s) and any(c.islower() for c in s)
        return start, end, "locations", street
    family = {"NAME": "names", "ID": "ids", "CONTACT": "contact", "ORGANIZATION": "locations", "DATE": "dates", "AGE": "age"}[label]
    return start, end, family, family in ("names", "ids", "contact")


def load_letters(data, split):
    """Letters of one split as a list of dicts with id, language, text and gold spans."""
    if split == "control":
        name = "control/control-00000-of-00001.parquet"
    else:
        name = f"data/{split}-00000-of-00001.parquet"
    path = os.path.join(data, name) if os.path.isdir(data) else f"hf://datasets/{data}/{name}"
    df = pd.read_parquet(path, columns=["id", "language", "split", "text", "spans"])
    if split == "control":
        df = df[df["split"] == "test"]
    df = df.sort_values("language", kind="stable")
    letters = []
    for r in df.itertuples():
        spans = [gold_span(r.text, int(s["start"]), int(s["end"]), s["label"]) for s in r.spans if s["end"] > s["start"]]
        letters.append({"id": r.id, "language": r.language, "text": r.text, "spans": spans})
    return letters


def mask(n, spans):
    m = bytearray(n)
    for s, e in spans:
        m[max(0, s):min(n, e)] = b"\x01" * (min(n, e) - max(0, s))
    return m


def score_letter(letter, pred):
    """Character counts, per-family hits and the leak flag for one letter."""
    n = len(letter["text"])
    gm = mask(n, [(s, e) for s, e, *_ in letter["spans"]])
    pm = mask(n, [(s, e) for s, e in pred if e > s])
    out = {"gold": sum(gm), "pred": sum(pm), "both": sum(a & b for a, b in zip(gm, pm)), "leak": False,
           "has_direct": any(d for *_, d in letter["spans"]), "hits": {f: [0, 0] for f in FAMILIES}}
    for s, e, family, direct in letter["spans"]:
        # a gold span counts as found when at least half of its characters are redacted
        hit = sum(pm[s:e]) / (e - s) >= 0.5
        out["hits"][family][0] += hit
        out["hits"][family][1] += 1
        out["leak"] = out["leak"] or (direct and not hit)
    return out


def aggregate(rows, light=False):
    both, gold, pred = (sum(r[k] for r in rows) for k in ("both", "gold", "pred"))
    p = both / pred if pred else 0.0
    r = both / gold if gold else 0.0
    direct = [x for x in rows if x["has_direct"]]
    out = {"n_letters": len(rows), "char_p": p, "char_r": r, "char_f1": 2 * p * r / (p + r) if p + r else 0.0,
           "leak_rate": sum(x["leak"] for x in direct) / max(1, len(direct))}
    if not light:
        tot = {f: [sum(x["hits"][f][i] for x in rows) for i in (0, 1)] for f in FAMILIES}
        out["recall_by_family"] = {f: h / n if n else None for f, (h, n) in tot.items()}
    return out


def bootstrap(rows, n=1000, seed=7):
    """95 % interval from resampling whole letters."""
    rng = random.Random(seed)
    vals = {"char_f1": [], "leak_rate": []}
    for _ in range(n):
        agg = aggregate([rows[rng.randrange(len(rows))] for _ in rows], light=True)
        for k in vals:
            vals[k].append(agg[k])
    for v in vals.values():
        v.sort()
    return {k: [v[int(0.025 * n)], v[int(0.975 * n) - 1]] for k, v in vals.items()}


def evaluate(letters, preds, ci=True):
    rows = [score_letter(x, preds.get(x["id"]) or []) for x in letters]
    res = aggregate(rows)
    if ci:
        res["ci95"] = bootstrap(rows)
    langs = sorted({x["language"] for x in letters})
    res["by_language"] = {lang: aggregate([r for r, x in zip(rows, letters) if x["language"] == lang], light=True) for lang in langs}
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("predictions", nargs="+", help="JSON lines files; the file name (without .jsonl) is the model name")
    ap.add_argument("--data", default=DATASET, help="Hub dataset id or a local copy of the dataset repo")
    ap.add_argument("--out", default="results.json")
    ap.add_argument("--no-ci", action="store_true", help="skip the bootstrap (faster)")
    a = ap.parse_args()
    letters, results = {}, {}
    for path in a.predictions:
        model = os.path.basename(path).removesuffix(".jsonl")
        by_split = {}
        for x in map(json.loads, open(path, encoding="utf-8")):
            by_split.setdefault(x["split"], {})[x["id"]] = x["spans"]
        results[model] = {}
        for split, preds in sorted(by_split.items()):
            if split not in letters:
                letters[split] = load_letters(a.data, split)
            res = results[model][split] = evaluate(letters[split], preds, ci=not a.no_ci)
            print(f"{model:40s} {split:8s} letters={res['n_letters']:5d} char_f1={res['char_f1']:.3f} leak_rate={res['leak_rate']:.3f}")
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1)


if __name__ == "__main__":
    main()
