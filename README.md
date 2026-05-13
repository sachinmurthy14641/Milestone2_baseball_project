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

```
├── data/               # Raw and processed data files (not tracked in git)
├── notebooks/          # Exploratory analysis and modeling notebooks
├── src/                # Reusable helper modules
├── results/            # Model outputs, metrics, figures
└── README.md
```

## Setup

```bash
pip install pybaseball scikit-learn xgboost lightgbm umap-learn pandas matplotlib seaborn
```

## Status

Project is in early scoping phase. Data acquisition and EDA are the next steps.
