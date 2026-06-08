"""
Parallelized Statcast data pull via Modal.

Each worker pulls one month of data independently.
Results are concatenated locally and saved as parquet.

Usage:
    modal run src/data_pull.py                          # default: 2021-2023 seasons
    modal run src/data_pull.py --seasons 2023            # single season
    modal run src/data_pull.py --seasons 2021,2022,2023  # explicit seasons
"""

import modal
import sys
from datetime import date, timedelta
from pathlib import Path

app = modal.App("statcast-data-pull")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("pybaseball==2.2.7", "pandas", "pyarrow")
)

# Season date ranges (opening day → regular season end)
SEASON_DATES = {
    2019: ("2019-03-28", "2019-09-29"),
    2020: ("2020-07-23", "2020-09-27"),  # shortened COVID season
    2021: ("2021-04-01", "2021-10-03"),
    2022: ("2022-04-07", "2022-10-05"),
    2023: ("2023-03-30", "2023-10-01"),
    2024: ("2024-03-20", "2024-09-29"),
    2025: ("2025-03-27", "2025-09-28"),
}


def _month_ranges(start: str, end: str) -> list[tuple[str, str]]:
    """Split a date range into (month_start, month_end) chunks."""
    from datetime import datetime
    ranges = []
    current = datetime.strptime(start, "%Y-%m-%d").date()
    end_date = datetime.strptime(end, "%Y-%m-%d").date()

    while current <= end_date:
        # last day of current month
        if current.month == 12:
            month_end = date(current.year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(current.year, current.month + 1, 1) - timedelta(days=1)

        chunk_end = min(month_end, end_date)
        ranges.append((current.strftime("%Y-%m-%d"), chunk_end.strftime("%Y-%m-%d")))
        current = chunk_end + timedelta(days=1)

    return ranges


@app.function(image=image, timeout=300)
def pull_month(start: str, end: str) -> bytes:
    """Pull one month of Statcast data and return as parquet bytes."""
    from pybaseball import statcast
    from pybaseball import cache
    import pandas as pd
    import io

    cache.enable()
    print(f"Pulling {start} → {end}")
    df = statcast(start_dt=start, end_dt=end)

    if df is None or df.empty:
        return b""

    buf = io.BytesIO()
    df.to_parquet(buf, index=False)
    return buf.getvalue()


@app.local_entrypoint()
def main(seasons: str = "2021,2022,2023"):
    import pandas as pd
    import io

    out_dir = Path(__file__).parent.parent / "data"
    out_dir.mkdir(exist_ok=True)

    for season in [int(s.strip()) for s in seasons.split(",")]:
        if season not in SEASON_DATES:
            print(f"Unknown season {season}, skipping.")
            continue

        start, end = SEASON_DATES[season]
        chunks = _month_ranges(start, end)
        print(f"\n--- {season} season: {len(chunks)} monthly chunks ---")

        results = list(pull_month.map(
            [c[0] for c in chunks],
            [c[1] for c in chunks],
        ))

        dfs = [pd.read_parquet(io.BytesIO(r)) for r in results if r]
        if not dfs:
            print(f"No data returned for {season}.")
            continue

        df = pd.concat(dfs, ignore_index=True)
        out_path = out_dir / f"statcast_{season}_raw.parquet"
        df.to_parquet(out_path, index=False)
        print(f"Saved {len(df):,} rows → {out_path}")
