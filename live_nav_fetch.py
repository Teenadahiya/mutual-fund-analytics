import requests
import pandas as pd
import os
import json
import urllib3

urllib3.disable_warnings()

# ─────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

# ─────────────────────────────────────────
# FETCH LIVE NAV - HDFC Top 100 Direct
# ─────────────────────────────────────────
print("=" * 60)
print("FETCHING LIVE NAV DATA FROM MFAPI")
print("=" * 60)

def fetch_nav(scheme_code, scheme_name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    try:
        response = requests.get(url, timeout=60 ,verify = False)
        data = response.json()
        
        meta = data.get("meta", {})
        nav_data = data.get("data", [])
        
        print(f"\n✅ {scheme_name} (Code: {scheme_code})")
        print(f"   Fund House : {meta.get('fund_house', 'N/A')}")
        print(f"   Scheme     : {meta.get('scheme_name', 'N/A')}")
        print(f"   Category   : {meta.get('scheme_category', 'N/A')}")
        print(f"   NAV records: {len(nav_data)}")
        
        if nav_data:
            print(f"   Latest NAV : ₹{nav_data[0]['nav']} on {nav_data[0]['date']}")
        
        # Save to CSV
        df = pd.DataFrame(nav_data)
        df["scheme_code"] = scheme_code
        df["scheme_name"] = scheme_name
        filename = f"live_nav_{scheme_code}.csv"
        filepath = os.path.join(RAW_DIR, filename)
        df.to_csv(filepath, index=False)
        print(f"   💾 Saved to: {filename}")
        return df
        
    except Exception as e:
        print(f"   ❌ Error fetching {scheme_name}: {e}")
        return None

# ─────────────────────────────────────────
# FETCH 5 KEY SCHEMES
# ─────────────────────────────────────────
schemes = {
    125497: "HDFC Top 100 Direct",
    119551: "SBI Bluechip",
    120503: "ICICI Bluechip",
    118632: "Nippon Large Cap",
    119092: "Axis Bluechip",
    120841: "Kotak Bluechip",
}

all_nav = []
for code, name in schemes.items():
    df = fetch_nav(code, name)
    if df is not None:
        all_nav.append(df)

# ─────────────────────────────────────────
# SAVE COMBINED NAV
# ─────────────────────────────────────────
if all_nav:
    combined = pd.concat(all_nav, ignore_index=True)
    combined_path = os.path.join(RAW_DIR, "live_nav_all_schemes.csv")
    combined.to_csv(combined_path, index=False)
    print(f"\n✅ Combined NAV saved: live_nav_all_schemes.csv")
    print(f"   Total records: {len(combined)}")

print("\n" + "=" * 60)
print("✅ Live NAV fetch complete!")
print("=" * 60)
