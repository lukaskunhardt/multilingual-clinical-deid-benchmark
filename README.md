# Multilingual Clinical De-identification Benchmark: scorer

Scoring code for the [Multilingual Clinical De-identification Benchmark](https://huggingface.co/datasets/LukasKunhardt/multilingual-clinical-deid-benchmark), 3,300 synthetic doctor's letters in 22 European languages with marked identifiers. It computes character-level precision, recall and F1 and the leak rate from a file of predicted spans.

## Install

```bash
pip install pandas pyarrow huggingface_hub matplotlib
```

## Score a model

Write one JSON line per letter with character offsets into `text`:

```json
{"split": "test", "id": "de-k0012", "spans": [[105, 118], [240, 250]]}
```

Then run:

```bash
python evaluate.py my-model.jsonl --out results.json
python plot.py --results results.json --out chart.png
```

`evaluate.py` reads the letters from the Hub (or from a local copy with `--data`) and prints char F1 and leak rate per split. Splits are `train`, `dev`, `test` and `control` (the control letters of the test cases).

## Files

| File | What it does |
|---|---|
| `evaluate.py` | turns the labelled spans into gold, scores predictions, bootstraps 95 % intervals, writes `results.json` |
| `plot.py` | draws char F1 against leak rate from `results.json` |
| `results.json` | scores of the nine baseline models |
| `RESULTS.md` | full tables: test, control, dev and every language |
| `tests/test_evaluate.py` | sanity checks (gold as prediction scores F1 1.0 and no leaks) |

## Metrics

- **Char F1:** each character is inside a gold identifier or not. Labels do not count, only whether a character was redacted.
- **Leak rate:** share of letters in which at least one direct identifier (name, ID, contact, street address) is less than 50 % redacted. A location counts as a street when it holds a digit and a lower-case letter.

## Reproduce the baseline tables

The prediction files of the nine baseline models are in the `baselines/` folder of the dataset repo.

```bash
huggingface-cli download LukasKunhardt/multilingual-clinical-deid-benchmark --repo-type dataset --local-dir bench
python evaluate.py bench/baselines/*.jsonl --data bench --out results.json
```

## License

MIT. The dataset itself is CC BY 4.0.
