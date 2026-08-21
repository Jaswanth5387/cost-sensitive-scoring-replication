# Data

The raw dataset is not committed because `creditcard.csv` is about 150 MB.

Expected local path:

```text
data/raw/creditcard.csv
```

Source used for the current run:

- Zenodo record: https://zenodo.org/records/7395559
- DOI: `10.5281/zenodo.7395559`
- File: `creditcard.csv`
- MD5: `e90efcb83d69faf99fcab8b0255024de`

The same file is described as the European cardholder credit-card fraud dataset with 284,807 transactions and 492 frauds.

To fetch and verify it:

```bash
python scripts/download_data.py
```
