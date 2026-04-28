# ETF Copilot

A production-grade AI system that answers natural language questions about a curated universe of 25 ETFs. It combines a quantitative data pipeline, machine learning signal generation, and a RAG-powered agentic layer to reason over both live financial data and market documents.

---

## Architecture overview

```
Phase 1 — Data Pipeline        ✅ Complete
Phase 2 — ML Models            🔄 In progress
Phase 3 — RAG + Agentic Layer  ⬜ Upcoming
Phase 4 — Serving + MLOps      ⬜ Upcoming
```

The system is designed so that each phase feeds the next. The quality of the agent's answers in Phase 3 is bounded by the quality of the features computed in Phase 1.

---

## Phase 1 — Data Pipeline

### What it does

Ingests 7 years of daily OHLCV price data for 25 ETFs across 5 asset classes, validates every row at the boundary, stores in DuckDB, computes a 10-feature matrix, and saves a versioned Parquet file ready to feed the ML layer.

### ETF Universe

| Asset Class    | Tickers                          |
|----------------|----------------------------------|
| US Equity      | SPY, QQQ, IWM, VTI, VOO          |
| Fixed Income   | TLT, IEF, SHY, BND, LQD          |
| Commodities    | GLD, SLV, USO, DJP, PDBC         |
| International  | EFA, EEM, VEU, IDEV, VXUS        |
| Alternatives   | VNQ, REET, BTAL, CTA, DBMF       |

### Features computed

| Feature         | Description                                      | Window   |
|-----------------|--------------------------------------------------|----------|
| `mom_1m`        | Log return momentum                              | 21 days  |
| `mom_3m`        | Log return momentum                              | 63 days  |
| `mom_12m`       | Log return momentum                              | 252 days |
| `realized_vol`  | Rolling standard deviation of daily log returns  | 21 days  |
| `vol_of_vol`    | Rolling standard deviation of realized_vol       | 63 days  |
| `beta`          | Rolling beta vs SPY benchmark                    | 63 days  |
| `vix`           | CBOE Volatility Index (FRED: VIXCLS)             | Daily    |
| `yield_slope`   | 10Y minus 2Y treasury spread (FRED: DGS10-DGS2)  | Daily    |

All momentum calculations use **adjusted close prices** to account for dividends and splits. Log returns are used instead of simple returns for time-additivity.

### Output

```
data/features/features_v1.parquet
  shape:   42,610 rows × 16 columns
  tickers: 25
  dates:   2018-01-02 to 2024-12-31
```

---

## Project structure

```
etf_copilot/
├── configs/
│   ├── settings.py          # Pydantic settings — reads from .env
│   └── universe.py          # 25 ETFs in 5 asset classes
├── src/
│   ├── ingestion/
│   │   ├── fetcher.py       # ETFIngester — yfinance + tenacity retry
│   │   └── schemas.py       # Pydantic validation schemas
│   ├── features/
│   │   ├── momentum.py      # 1m, 3m, 12m log return momentum
│   │   ├── volatility.py    # realized vol, vol-of-vol
│   │   ├── beta.py          # rolling beta vs SPY
│   │   ├── macro.py         # VIX and yield curve from FRED
│   │   └── pipeline.py      # orchestrates all features → Parquet
│   ├── storage/
│   │   └── database.py      # DuckDB wrapper — read, write, coverage report
│   └── utils/
│       └── logging.py       # loguru setup — terminal + file output
├── scripts/
│   ├── run_ingestion.py     # entry point — fetch and store all ETFs
│   └── run_features.py      # entry point — compute and save feature matrix
├── tests/
│   └── ingestion/           # pytest suite with synthetic fixtures
├── pyproject.toml           # dependencies and build config
└── .env.example             # required environment variables
```

---

## Setup

```bash
git clone https://github.com/victorhrls/etf-copilot.git
cd etf-copilot
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
# add your FRED_API_KEY to .env
```

---

## Running the pipeline

```bash
# Step 1 — ingest raw prices for all 25 ETFs
python scripts/run_ingestion.py

# Step 2 — compute features and save Parquet
python scripts/run_features.py
```

---

## Key architectural decisions

**DuckDB over PostgreSQL.** The analytical workload — cross-sectional queries, rolling windows, date range filters — maps naturally to a columnar engine. DuckDB runs in-process with no server overhead and queries Parquet files natively. For a solo ML project this is the right tradeoff.

**Adjusted close over raw close.** All momentum and return calculations use adjusted close prices. Raw close prices contain artificial discontinuities from dividends and splits that corrupt momentum signals.

**Log returns over simple returns.** Log returns are time-additive — a 3-month return is exactly the sum of daily log returns. Simple returns are not, which creates compounding errors in multi-period signals.

**Pydantic validation at ingestion.** Data is validated at the boundary — the moment it arrives from Yahoo Finance. Bad rows are logged and dropped before touching the database. Downstream code trusts the data and never re-validates.

**Tenacity retry with exponential backoff.** Yahoo Finance is unreliable. Each fetch retries up to 3 times with 2s, 4s, 8s delays. The pipeline survives transient failures without human intervention.

---

## Stack

Python · DuckDB · yfinance · FRED API · Pydantic · loguru · tenacity · pandas · pyarrow · pytest · ruff · pyproject.toml

---

## Roadmap

- **Phase 2** — Hidden Markov Model regime detection · XGBoost/LightGBM ETF ranking · SHAP explainability · MLflow experiment tracking
- **Phase 3** — FAISS vector store · RAG retrieval over ETF prospectuses · Claude agent via Anthropic API · RAGAS evaluation
- **Phase 4** — FastAPI serving · Docker · GitHub Actions CI/CD · drift monitoring