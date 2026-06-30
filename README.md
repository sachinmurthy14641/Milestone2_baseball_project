# SIADS 696 Milestone 2 — Baseball Pitch Classification

## Project Overview

This project explores pitch classification using Statcast ball-flight data retrieved via `pybaseball`. It has two modeling components:

1. **Supervised Learning — Pitch Type Recreation**: Reproduce existing pitch classifications (8–10 standard types) using labeled Statcast data. We will compare multiple classifiers and feature sets to evaluate which combinations best recover the official labels.

2. **Unsupervised Learning — Fine-Grained Pitch Clustering**: Cluster pitches purely by their physical characteristics (ignoring labels) into 15–20 groups to surface nuance that standard categories may obscure — e.g., distinguishing hard from soft cutters, or two-seam variants by arm side.

## Data Source

- **[pybaseball](https://github.com/jldbc/pybaseball) / Statcast**: pitch-level data including velocity, spin rate, movement (induced/total), release point, extension, and plate location.
- **Seasons collected**: 2023 (720,684 pitches), 2024 (731,904 pitches), 2025 (711,897 pitches) — ~2.16M pitches combined, stored in `data/` via Git LFS.
- **Ingestion pipeline**: data is pulled with a parallelized [Modal](https://modal.com) pipeline (`src/data_pull.py`) that splits each season into monthly chunks and fetches them concurrently — about 8x faster than a sequential `pybaseball` pull (~30s vs ~4min per season). See [Data Pull](#data-pull-via-modal) below.

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
├── data/                              # Raw and processed data files (tracked via Git LFS)
│   ├── statcast_2023_raw.parquet
│   ├── statcast_2024_raw.parquet
│   └── statcast_2025_raw.parquet
├── docs/                              # Project documentation and writeups
│   ├── SIADS696_Project_Proposal.docx
│   └── Baseball Pitch Identification and Clustering Model.pdf
├── notebooks/                         # Exploratory analysis and modeling notebooks
│   ├── 01_eda.ipynb                   # Statcast EDA — distributions, movement profiles, feature correlations
│   ├── mackinnon_supervised.ipynb     # Supervised pitch classification experiments
│   ├── mackinnon_supervised_v2.ipynb
│   └── asad_unsupervised.ipynb        # Unsupervised clustering experiments
├── src/                                # Reusable modules
│   └── data_pull.py                   # Parallelized Statcast pull via Modal
├── results/                            # Model outputs, metrics, figures
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

Statcast pulls are parallelized across monthly chunks using Modal, which cuts ingestion time roughly 8x versus a sequential `pybaseball` pull (~30s vs ~4min per season). Supported seasons: 2019–2025.

```bash
# Pull one season (~720k pitches, parallelized by month)
modal run src/data_pull.py --seasons 2023

# Pull multiple seasons
modal run src/data_pull.py --seasons 2023,2024,2025
```

Data lands in `data/statcast_<season>_raw.parquet` and is tracked via Git LFS so the whole group can pull it down with a normal `git clone`/`git pull` (requires [Git LFS](https://git-lfs.com) installed locally).

## Status

- [x] Project scoping and proposal
- [x] Repository setup
- [x] Data acquisition — 2023, 2024, 2025 Statcast seasons (~2.16M pitches, 118 features), parallelized via Modal
- [x] Exploratory data analysis (`notebooks/01_eda.ipynb`)
- [ ] Feature engineering and preprocessing
- [ ] Supervised model development and comparison — in progress (`notebooks/mackinnon_supervised*.ipynb`)
- [ ] Unsupervised clustering and analysis — in progress (`notebooks/asad_unsupervised.ipynb`)
- [ ] Final writeup
