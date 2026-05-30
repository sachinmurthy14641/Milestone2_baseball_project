# SIADS 696 Milestone 2 — Baseball Pitch Classification

## Project Overview

This project explores pitch classification using Statcast ball-flight data retrieved via `pybaseball`. It has two modeling components:

1. **Supervised Learning — Pitch Type Recreation**: Reproduce existing pitch classifications (8–10 standard types) using labeled Statcast data. We will compare multiple classifiers and feature sets to evaluate which combinations best recover the official labels.

2. **Unsupervised Learning — Fine-Grained Pitch Clustering**: Cluster pitches purely by their physical characteristics (ignoring labels) into 15–20 groups to surface nuance that standard categories may obscure — e.g., distinguishing hard from soft cutters, or two-seam variants by arm side.

## Data Source

- **pybaseball / Statcast**: pitch-level data including velocity, spin rate, movement (induced/total), release point, extension, and plate location.

## Planned Modeling Approaches

### Supervised

- Baseline: Logistic Regression / Random Forest
- Comparison models: Gradient Boosting (XGBoost/LightGBM), SVM, Neural Net (TBD)
- Feature set experiments: movement-only, velocity + movement, full Statcast feature set

### Unsupervised

- K-Means and/or Gaussian Mixture Models across 15–20 clusters
- Dimensionality reduction for visualization (PCA, UMAP)
- Analysis of how clusters map to (and diverge from) official pitch types

## Repository Structure

```text
├── data/               # Raw and processed data files (not tracked in git)
├── docs/               # Project documentation and writeups
├── notebooks/          # Exploratory analysis and modeling notebooks
│   └── 01_eda.ipynb    # Statcast EDA — distributions, movement profiles, feature correlations
├── src/                # Reusable modules
│   └── data_pull.py    # Parallelized Statcast pull via Modal
├── results/            # Model outputs, metrics, figures
└── README.md
```

## Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

pip install pybaseball scikit-learn xgboost lightgbm umap-learn pandas matplotlib seaborn jupyter ipykernel modal

# Register Jupyter kernel
python -m ipykernel install --user --name baseball-pitch --display-name "Python (baseball-pitch)"
```

### Data Pull (via Modal)

```bash
# Pull one season (~720k pitches, parallelized by month)
modal run src/data_pull.py --seasons 2023

# Pull multiple seasons
modal run src/data_pull.py --seasons 2021,2022,2023
```

## Status

- [x] Project scoping and proposal
- [x] Repository setup
- [x] Data acquisition — 2023 Statcast season (720k pitches, 118 features)
- [x] Exploratory data analysis (`notebooks/01_eda.ipynb`)
- [ ] Feature engineering and preprocessing
- [ ] Supervised model development and comparison
- [ ] Unsupervised clustering and analysis
- [ ] Final writeup
