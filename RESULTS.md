# Results

All numbers come from `results.json`, which `evaluate.py` writes from the prediction files in the `baselines/` folder of the dataset repo. Rows are sorted by character F1 on the test split. The best value in each column is bold.

- **Char F1, precision, recall:** every character is either inside a gold identifier span or not. A character counts as found when any predicted span covers it. Labels are ignored.
- **Leak rate:** share of letters in which at least one direct identifier (name, ID, contact, street address) is less than 50 % covered by predictions.
- **Recall by family:** share of gold spans that are at least 50 % covered. Locations include hospitals and other organisations. Age includes ages in years, weeks and days.
- **95 % CI:** bootstrap over letters, 1,000 samples, seed 7.

I ran every model once with the setting below, fixed in writing before the first run. No model was trained or tuned on this dataset. The test split was opened once for these numbers.

The written setting also listed three GLiNER models (urchade/gliner_multi_pii-v1, knowledgator/gliner-pii-large-v1.0, fastino/gliner2-privacy-filter-PII-multi). Their run was too slow, I stopped it, and they have no row.

| Model | Setting |
|---|---|
| Horizon-Labs/pii-redactor-base | transformers pipeline on each line, aggregation first |
| LukasKunhardt/german-clinical-deid (mine) | own package, threshold from the model config (0.01) |
| LukasKunhardt/pii-filter-small (mine) | 512-token windows, argmax |
| LukasKunhardt/german-clinical-deid-base (mine) | own package, threshold from the model config (0.01) |
| openai/privacy-filter (opf, Viterbi) | opf package, Viterbi decoding (default) |
| Horizon-Labs/pii-redactor-small | transformers pipeline on lines packed up to 384 tokens, aggregation first |
| OpenMed/privacy-filter-multilingual-v2 | transformers pipeline on lines packed up to 384 tokens, aggregation first |
| iiiorg/piiranha-v1-detect-personal-information | transformers pipeline on each line, aggregation first |
| openai/privacy-filter (transformers pipeline) | transformers pipeline on lines packed up to 384 tokens, aggregation first |

## Test split (1,980 letters)

| Model | Char F1 [95 % CI] | Precision | Recall | Leak rate [95 % CI] | Names | IDs | Contact | Locations | Dates | Age |
|---|---|---|---|---|---|---|---|---|---|---|
| Horizon-Labs/pii-redactor-base | **0.881 [0.878, 0.883]** | **0.931** | 0.835 | 0.283 [0.263, 0.303] | 0.96 | 0.99 | **1.00** | 0.88 | 0.66 | **0.81** |
| LukasKunhardt/german-clinical-deid (mine) | 0.842 [0.838, 0.846] | 0.776 | 0.921 | 0.197 [0.179, 0.214] | 0.92 | **1.00** | **1.00** | 0.90 | **1.00** | 0.18 |
| LukasKunhardt/pii-filter-small (mine) | 0.827 [0.823, 0.830] | 0.908 | 0.758 | 0.734 [0.715, 0.754] | 0.93 | 0.99 | 0.97 | 0.60 | 0.84 | 0.08 |
| LukasKunhardt/german-clinical-deid-base (mine) | 0.786 [0.782, 0.791] | 0.671 | **0.949** | **0.141 [0.126, 0.156]** | **0.97** | **1.00** | **1.00** | **0.94** | **1.00** | 0.62 |
| openai/privacy-filter (opf, Viterbi) | 0.745 [0.739, 0.752] | 0.857 | 0.660 | 0.874 [0.860, 0.889] | 0.76 | 0.82 | 0.84 | 0.50 | 0.80 | 0.08 |
| Horizon-Labs/pii-redactor-small | 0.743 [0.740, 0.747] | 0.722 | 0.766 | 0.528 [0.507, 0.550] | 0.96 | 0.99 | **1.00** | 0.83 | 0.47 | 0.65 |
| OpenMed/privacy-filter-multilingual-v2 | 0.659 [0.656, 0.662] | 0.630 | 0.691 | 0.746 [0.726, 0.766] | 0.88 | **1.00** | **1.00** | 0.78 | 0.41 | 0.63 |
| iiiorg/piiranha-v1-detect-personal-information | 0.658 [0.654, 0.662] | 0.912 | 0.514 | 1.000 [1.000, 1.000] | 0.66 | 0.34 | 0.65 | 0.78 | 0.12 | 0.04 |
| openai/privacy-filter (transformers pipeline) | 0.635 [0.629, 0.640] | 0.653 | 0.617 | 0.895 [0.882, 0.908] | 0.76 | 0.83 | 0.84 | 0.49 | 0.65 | 0.09 |

## Control letters by a second writer (88 letters of the test cases, written by GLM-5.3)

| Model | Char F1 [95 % CI] | Precision | Recall | Leak rate [95 % CI] | Names | IDs | Contact | Locations | Dates | Age |
|---|---|---|---|---|---|---|---|---|---|---|
| Horizon-Labs/pii-redactor-base | **0.869 [0.854, 0.884]** | **0.860** | 0.877 | 0.250 [0.159, 0.352] | 0.96 | **1.00** | 0.99 | 0.93 | 0.71 | 0.21 |
| LukasKunhardt/german-clinical-deid (mine) | 0.771 [0.749, 0.793] | 0.677 | 0.894 | 0.216 [0.136, 0.307] | 0.90 | **1.00** | **1.00** | 0.91 | **0.97** | 0.05 |
| LukasKunhardt/pii-filter-small (mine) | 0.826 [0.805, 0.849] | 0.848 | 0.806 | 0.636 [0.534, 0.727] | 0.96 | **1.00** | 0.97 | 0.63 | 0.88 | 0.07 |
| LukasKunhardt/german-clinical-deid-base (mine) | 0.739 [0.720, 0.760] | 0.618 | **0.921** | **0.170 [0.102, 0.250]** | 0.93 | **1.00** | **1.00** | **0.96** | 0.96 | **0.25** |
| openai/privacy-filter (opf, Viterbi) | 0.752 [0.723, 0.781] | 0.799 | 0.711 | 0.750 [0.648, 0.841] | 0.82 | 0.90 | 0.87 | 0.53 | 0.81 | 0.10 |
| Horizon-Labs/pii-redactor-small | 0.747 [0.731, 0.764] | 0.680 | 0.829 | 0.239 [0.148, 0.341] | **0.99** | 0.98 | **1.00** | 0.91 | 0.41 | 0.13 |
| OpenMed/privacy-filter-multilingual-v2 | 0.682 [0.667, 0.697] | 0.620 | 0.757 | 0.534 [0.432, 0.648] | 0.89 | 0.99 | 0.99 | 0.85 | 0.45 | 0.11 |
| iiiorg/piiranha-v1-detect-personal-information | 0.685 [0.663, 0.705] | 0.852 | 0.572 | 0.989 [0.966, 1.000] | 0.65 | 0.40 | 0.65 | 0.86 | 0.14 | 0.03 |
| openai/privacy-filter (transformers pipeline) | 0.649 [0.626, 0.673] | 0.611 | 0.692 | 0.773 [0.682, 0.852] | 0.83 | 0.92 | 0.88 | 0.54 | 0.71 | 0.11 |

## Dev split (660 letters)

| Model | Char F1 [95 % CI] | Precision | Recall | Leak rate [95 % CI] | Names | IDs | Contact | Locations | Dates | Age |
|---|---|---|---|---|---|---|---|---|---|---|
| Horizon-Labs/pii-redactor-base | **0.886 [0.882, 0.889]** | **0.930** | 0.845 | 0.289 [0.255, 0.326] | **0.97** | 0.99 | **1.00** | 0.87 | 0.69 | **0.75** |
| LukasKunhardt/german-clinical-deid (mine) | 0.840 [0.832, 0.848] | 0.776 | 0.915 | 0.203 [0.174, 0.235] | 0.92 | **1.00** | **1.00** | 0.91 | **1.00** | 0.15 |
| LukasKunhardt/pii-filter-small (mine) | 0.820 [0.813, 0.826] | 0.907 | 0.748 | 0.744 [0.711, 0.777] | 0.93 | 0.98 | 0.97 | 0.59 | 0.83 | 0.09 |
| LukasKunhardt/german-clinical-deid-base (mine) | 0.791 [0.784, 0.799] | 0.681 | **0.944** | **0.152 [0.124, 0.179]** | **0.97** | **1.00** | **1.00** | **0.94** | **1.00** | 0.56 |
| openai/privacy-filter (opf, Viterbi) | 0.739 [0.727, 0.751] | 0.859 | 0.649 | 0.877 [0.853, 0.902] | 0.76 | 0.81 | 0.84 | 0.50 | 0.78 | 0.07 |
| Horizon-Labs/pii-redactor-small | 0.748 [0.743, 0.753] | 0.723 | 0.775 | 0.555 [0.515, 0.592] | 0.96 | 0.98 | **1.00** | 0.83 | 0.46 | 0.59 |
| OpenMed/privacy-filter-multilingual-v2 | 0.667 [0.661, 0.672] | 0.634 | 0.703 | 0.750 [0.715, 0.782] | 0.88 | 0.99 | **1.00** | 0.79 | 0.41 | 0.58 |
| iiiorg/piiranha-v1-detect-personal-information | 0.671 [0.665, 0.678] | 0.913 | 0.531 | 1.000 [1.000, 1.000] | 0.66 | 0.35 | 0.65 | 0.78 | 0.14 | 0.04 |
| openai/privacy-filter (transformers pipeline) | 0.633 [0.623, 0.643] | 0.653 | 0.615 | 0.894 [0.870, 0.917] | 0.76 | 0.81 | 0.84 | 0.50 | 0.66 | 0.08 |

## Test split: char F1 by language

| Model | bg | cs | da | de | el | en | es | et | fi | fr | hr | hu | it | lt | lv | nl | pl | pt | ro | sk | sl | sv |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Horizon-Labs/pii-redactor-base | 0.82 | **0.88** | 0.90 | 0.90 | **0.84** | 0.93 | 0.89 | 0.84 | 0.87 | 0.92 | **0.91** | **0.84** | 0.91 | **0.82** | 0.85 | 0.92 | **0.88** | 0.89 | 0.86 | **0.89** | **0.85** | **0.90** |
| LukasKunhardt/german-clinical-deid (mine) | 0.57 | 0.87 | **0.92** | **0.93** | 0.57 | **0.96** | **0.90** | 0.81 | 0.86 | **0.94** | 0.79 | 0.73 | **0.92** | 0.73 | 0.75 | **0.93** | 0.80 | **0.92** | **0.89** | 0.84 | **0.85** | **0.90** |
| LukasKunhardt/pii-filter-small (mine) | **0.86** | 0.76 | 0.82 | 0.86 | 0.65 | 0.89 | 0.89 | **0.88** | 0.61 | 0.90 | 0.85 | 0.79 | 0.85 | 0.80 | **0.86** | 0.88 | 0.83 | 0.87 | 0.80 | 0.83 | 0.82 | 0.74 |
| LukasKunhardt/german-clinical-deid-base (mine) | 0.67 | 0.84 | 0.89 | **0.93** | 0.57 | 0.90 | 0.69 | 0.86 | **0.88** | 0.78 | 0.75 | 0.74 | 0.80 | 0.75 | 0.79 | 0.89 | 0.70 | 0.71 | 0.79 | 0.79 | 0.77 | 0.85 |
| openai/privacy-filter (opf, Viterbi) | 0.78 | 0.76 | 0.67 | 0.83 | 0.20 | 0.85 | 0.87 | 0.70 | 0.54 | 0.86 | 0.83 | 0.80 | 0.81 | 0.34 | 0.70 | 0.83 | 0.79 | 0.85 | 0.67 | 0.76 | 0.71 | 0.73 |
| Horizon-Labs/pii-redactor-small | 0.71 | 0.74 | 0.72 | 0.78 | 0.73 | 0.81 | 0.80 | 0.67 | 0.63 | 0.81 | 0.75 | 0.66 | 0.82 | 0.68 | 0.66 | 0.77 | 0.76 | 0.81 | 0.76 | 0.74 | 0.76 | 0.71 |
| OpenMed/privacy-filter-multilingual-v2 | 0.57 | 0.66 | 0.60 | 0.71 | 0.60 | 0.76 | 0.71 | 0.61 | 0.57 | 0.72 | 0.65 | 0.60 | 0.74 | 0.65 | 0.58 | 0.68 | 0.64 | 0.73 | 0.68 | 0.66 | 0.65 | 0.65 |
| iiiorg/piiranha-v1-detect-personal-information | 0.48 | 0.66 | 0.63 | 0.70 | 0.70 | 0.70 | 0.69 | 0.69 | 0.64 | 0.62 | 0.66 | 0.61 | 0.68 | 0.62 | 0.58 | 0.70 | 0.72 | 0.60 | 0.69 | 0.73 | 0.69 | 0.61 |
| openai/privacy-filter (transformers pipeline) | 0.68 | 0.65 | 0.56 | 0.72 | 0.23 | 0.75 | 0.74 | 0.56 | 0.47 | 0.75 | 0.71 | 0.62 | 0.72 | 0.28 | 0.56 | 0.71 | 0.66 | 0.73 | 0.58 | 0.65 | 0.61 | 0.59 |

## Test split: leak rate by language

| Model | bg | cs | da | de | el | en | es | et | fi | fr | hr | hu | it | lt | lv | nl | pl | pt | ro | sk | sl | sv |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Horizon-Labs/pii-redactor-base | 1.00 | 0.22 | 0.22 | 0.04 | **0.90** | 0.17 | 0.33 | 0.26 | 0.52 | 0.02 | 0.07 | 0.12 | 0.06 | 0.48 | 0.57 | 0.11 | 0.04 | 0.34 | **0.09** | 0.16 | 0.11 | 0.40 |
| LukasKunhardt/german-clinical-deid (mine) | 1.00 | 0.19 | **0.00** | **0.00** | 1.00 | **0.00** | **0.01** | 0.18 | **0.14** | **0.00** | 0.01 | **0.06** | **0.00** | 0.43 | 0.70 | **0.01** | **0.00** | 0.07 | 0.43 | 0.09 | **0.00** | **0.01** |
| LukasKunhardt/pii-filter-small (mine) | **0.04** | 0.99 | 1.00 | 0.76 | 1.00 | 0.61 | 0.23 | 0.82 | 1.00 | 0.32 | 0.97 | 0.42 | 0.82 | 0.90 | 0.46 | 0.77 | 0.93 | 0.57 | 0.83 | 0.90 | 0.81 | 1.00 |
| LukasKunhardt/german-clinical-deid-base (mine) | 0.92 | **0.01** | 0.02 | **0.00** | 0.98 | **0.00** | 0.02 | **0.03** | 0.17 | **0.00** | **0.00** | **0.06** | **0.00** | **0.37** | **0.12** | 0.04 | 0.02 | **0.06** | 0.21 | **0.02** | 0.01 | 0.04 |
| openai/privacy-filter (opf, Viterbi) | 0.77 | 0.99 | 0.99 | 0.88 | 1.00 | 0.91 | 0.52 | 0.96 | 1.00 | 0.66 | 0.86 | 0.77 | 0.89 | 1.00 | 0.91 | 0.94 | 0.84 | 0.57 | 0.87 | 0.97 | 0.94 | 1.00 |
| Horizon-Labs/pii-redactor-small | 1.00 | 0.67 | 0.86 | 0.34 | 0.91 | 0.72 | 0.07 | 0.38 | 0.99 | 0.39 | 0.52 | 0.09 | 0.02 | 0.83 | 0.29 | 0.88 | **0.00** | 0.21 | 0.13 | 0.60 | 0.81 | 0.91 |
| OpenMed/privacy-filter-multilingual-v2 | 1.00 | 0.82 | 0.84 | 0.61 | 1.00 | 0.34 | 0.53 | 0.69 | 0.99 | 0.64 | 0.84 | 0.43 | 0.50 | 0.98 | 0.84 | 0.99 | 0.59 | 0.60 | 0.36 | 0.89 | 0.98 | 0.94 |
| iiiorg/piiranha-v1-detect-personal-information | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| openai/privacy-filter (transformers pipeline) | 0.77 | 1.00 | 0.99 | 0.87 | 1.00 | 0.89 | 0.56 | 1.00 | 1.00 | 0.70 | 0.93 | 0.76 | 0.89 | 1.00 | 0.96 | 0.97 | 0.84 | 0.69 | 0.90 | 0.99 | 1.00 | 1.00 |
