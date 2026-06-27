# 📊 Mutual Fund Analytics Platform

An end-to-end data analytics project on Indian Mutual Fund data — covering ETL pipeline, exploratory data analysis, live NAV fetching, SQL queries, and Flask REST API.

## 🚀 Project Overview

This project analyzes real-world mutual fund datasets to extract meaningful financial insights. It includes data ingestion from 10 structured CSV datasets, live NAV data fetching via MFAPI, and a full analytics pipeline built in Python.

## 🛠️ Tech Stack

- **Python** — Pandas, NumPy, Matplotlib, Seaborn, Plotly
- **Flask** — REST API with JSON endpoints
- **SQL / PostgreSQL** — Business queries and data storage
- **Requests** — Live NAV API integration (mfapi.in)
- **Git & GitHub** — Version control

## 📁 Project Structure

- `data/raw/` — Original CSV datasets
- `data/processed/` — Cleaned and transformed data
- `notebooks/` — Jupyter EDA notebooks
- `dashboard/` — Plotly visualizations
- `reports/` — Analysis reports
- `sql/` — SQL queries
- `data_ingestion.py` — ETL pipeline
- `live_nav_fetch.py` — Live NAV fetching
- `requirements.txt` — Dependencies


## 📦 Datasets Used

| File | Description |
|------|-------------|
| 01_fund_master.csv | Master list of all mutual fund schemes |
| 02_nav_history.csv | Historical NAV data |
| 03_aum_by_fund_house.csv | AUM breakdown by fund house |
| 04_monthly_sip_inflows.csv | Monthly SIP inflow trends |
| 05_category_inflows.csv | Inflows by fund category |
| 06_industry_folio_count.csv | Industry-level folio counts |
| 07_scheme_performance.csv | Scheme-wise performance metrics |
| 08_investor_transactions.csv | Investor transaction records |
| 09_portfolio_holdings.csv | Portfolio holdings data |
| 10_benchmark_indices.csv | Benchmark index data |

## ⚙️ Setup & Installation

**1. Clone the repository**

`git clone https://github.com/Teenadahiya/mutual-fund-analytics.git`

**2. Install dependencies**

`pip install -r requirements.txt`

**3. Run data ingestion**

`python data_ingestion.py`

**4. Fetch live NAV data**

`python live_nav_fetch.py`

## 🔑 Key Features

- ✅ ETL pipeline loading 10 real mutual fund datasets
- ✅ Live NAV fetching for 6 major schemes via MFAPI
- ✅ Data quality validation and AMFI code verification
- ✅ Fund master exploration — categories, risk grades, fund houses
- ✅ EDA with 4 visualizations — NAV trends, SIP growth, category analysis
- ✅ Flask REST API with 6 working endpoints
- 🔄 SQL business queries (in progress)

## 👩‍💻 Author
Teena Dahiya
B.Tech Computer Science | JECRC, Jaipur
[GitHub](https://github.com/Teenadahiya) • [LinkedIn](https://linkedin.com/in/teenadahiya)