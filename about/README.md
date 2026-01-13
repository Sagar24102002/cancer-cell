Breast Cancer Detection (research prototype)

This repository provides a minimal research prototype for training a deep-learning model to classify breast-cancer-related medical images (binary classification). This is a technical starting point — not a clinically validated product.

Important: Models produced from this code must NOT be used in clinical decision-making without extensive validation and regulatory approval.

Contents:
- `requirements.txt` - Python dependencies
- `data_loader.py` - PyTorch Dataset for image CSV lists
- `model.py` - ResNet18-based classifier
- `train.py` - Training script
- `evaluate.py` - Evaluation script
- `utils.py` - Helper functions

Quickstart (example):

1. Prepare a CSV file `data.csv` with columns `filepath,label` where `label` is 0 (benign) or 1 (malignant).
2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Train:

```powershell
python train.py --train_csv data_train.csv --val_csv data_val.csv --output_dir ./runs/exp1
```

4. Evaluate:

```powershell
python evaluate.py --csv data_test.csv --checkpoint runs/exp1/model_best.pth --out predictions.csv
```

See each script header for more options.

Disclaimer: This code is for research and education only. Clinical use requires additional data, rigorous validation, and regulatory oversight.
