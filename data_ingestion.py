import pandas as pd
import os

# ─────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

# ─────────────────────────────────────────
# LOAD ALL 10 CSV DATASETS
# ─────────────────────────────────────────
csv_files = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

dataframes = {}

print("=" * 60)
print("LOADING ALL CSV DATASETS")
print("=" * 60)

for file in csv_files:
    path = os.path.join(RAW_DIR, file)
    name = file.replace(".csv", "")
    try:
        df = pd.read_csv(path)
        dataframes[name] = df
        print(f"\n📂 {file}")
        print(f"   Shape   : {df.shape}")
        print(f"   Columns : {list(df.columns)}")
        print(f"   Dtypes  :\n{df.dtypes}")
        print(f"   Head    :\n{df.head(3)}")
        anomalies = df.isnull().sum()
        if anomalies.any():
            print(f"   ⚠️  Missing values:\n{anomalies[anomalies > 0]}")
        else:
            print(f"   ✅ No missing values")
    except Exception as e:
        print(f"   ❌ Error loading {file}: {e}")

# ─────────────────────────────────────────
# EXPLORE FUND MASTER
# ─────────────────────────────────────────
print("\n" + "=" * 60)
print("FUND MASTER EXPLORATION")
print("=" * 60)

fm = dataframes.get("01_fund_master")
if fm is not None:
    if "fund_house" in fm.columns:
        print(f"\nUnique Fund Houses ({fm['fund_house'].nunique()}):")
        print(fm["fund_house"].unique())
    if "category" in fm.columns:
        print(f"\nUnique Categories ({fm['category'].nunique()}):")
        print(fm["category"].unique())
    if "sub_category" in fm.columns:
        print(f"\nUnique Sub-categories ({fm['sub_category'].nunique()}):")
        print(fm["sub_category"].unique())
    if "risk_grade" in fm.columns:
        print(f"\nUnique Risk Grades ({fm['risk_grade'].nunique()}):")
        print(fm["risk_grade"].unique())

# ─────────────────────────────────────────
# VALIDATE AMFI CODES
# ─────────────────────────────────────────
print("\n" + "=" * 60)
print("AMFI CODE VALIDATION")
print("=" * 60)

nav = dataframes.get("02_nav_history")
if fm is not None and nav is not None:
    fm_col = next((c for c in fm.columns if "scheme" in c.lower() or "amfi" in c.lower() or "code" in c.lower()), None)
    nav_col = next((c for c in nav.columns if "scheme" in c.lower() or "amfi" in c.lower() or "code" in c.lower()), None)

    if fm_col and nav_col:
        fm_codes = set(fm[fm_col].dropna().astype(str))
        nav_codes = set(nav[nav_col].dropna().astype(str))
        missing = fm_codes - nav_codes
        print(f"\nFund master codes    : {len(fm_codes)}")
        print(f"NAV history codes    : {len(nav_codes)}")
        print(f"Codes missing in NAV : {len(missing)}")
        if missing:
            print(f"Missing codes sample : {list(missing)[:10]}")
        else:
            print("✅ All AMFI codes validated — no missing codes!")
    else:
        print("⚠️  Could not find matching scheme/AMFI code columns to validate.")

# ─────────────────────────────────────────
# DATA QUALITY SUMMARY
# ─────────────────────────────────────────
print("\n" + "=" * 60)
print("DATA QUALITY SUMMARY")
print("=" * 60)

for name, df in dataframes.items():
    total = df.size
    missing = df.isnull().sum().sum()
    pct = round((missing / total) * 100, 2)
    print(f"{name:40s} | Rows: {df.shape[0]:6d} | Missing: {missing:5d} ({pct}%)")

print("\n✅ Data ingestion complete!")
print(f"✅ All {len(dataframes)} datasets loaded successfully.")
