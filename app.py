from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

# ─────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data")

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
fund_master = pd.read_csv(os.path.join(RAW_DIR, "01_fund_master.csv"))
nav_history = pd.read_csv(os.path.join(RAW_DIR, "02_nav_history.csv"))
sip = pd.read_csv(os.path.join(RAW_DIR, "04_monthly_sip_inflows.csv"))
scheme_perf = pd.read_csv(os.path.join(RAW_DIR, "07_scheme_performance.csv"))

# ─────────────────────────────────────────
# ROUTE 1 - Home
# ─────────────────────────────────────────
@app.route('/')
def home():
    return jsonify({
        "message": "Mutual Fund Analytics API",
        "version": "1.0",
        "endpoints": [
            "/api/funds",
            "/api/funds/<category>",
            "/api/nav/<amfi_code>",
            "/api/sip-trends",
            "/api/top-performers"
        ]
    })

# ─────────────────────────────────────────
# ROUTE 2 - Get all funds
# ─────────────────────────────────────────
@app.route('/api/funds')
def get_all_funds():
    funds = fund_master[[
        'amfi_code', 'fund_house', 'scheme_name',
        'category', 'sub_category', 'risk_category',
        'expense_ratio_pct'
    ]].to_dict(orient='records')
    
    return jsonify({
        "total": len(funds),
        "funds": funds
    })

# ─────────────────────────────────────────
# ROUTE 3 - Get funds by category
# ─────────────────────────────────────────
@app.route('/api/funds/<category>')
def get_funds_by_category(category):
    filtered = fund_master[
        fund_master['category'].str.lower() == category.lower()
    ]
    
    if filtered.empty:
        return jsonify({"error": f"No funds found for category: {category}"}), 404
    
    funds = filtered[[
        'amfi_code', 'fund_house', 'scheme_name',
        'sub_category', 'risk_category', 'expense_ratio_pct'
    ]].to_dict(orient='records')
    
    return jsonify({
        "category": category,
        "total": len(funds),
        "funds": funds
    })

# ─────────────────────────────────────────
# ROUTE 4 - Get NAV history by AMFI code
# ─────────────────────────────────────────
@app.route('/api/nav/<int:amfi_code>')
def get_nav(amfi_code):
    nav = nav_history[nav_history['amfi_code'] == amfi_code]
    
    if nav.empty:
        return jsonify({"error": f"No NAV data found for code: {amfi_code}"}), 404
    
    # Get fund name
    fund = fund_master[fund_master['amfi_code'] == amfi_code]
    fund_name = fund['scheme_name'].values[0] if not fund.empty else "Unknown"
    
    nav_data = nav[['date', 'nav']].tail(30).to_dict(orient='records')
    
    return jsonify({
        "amfi_code": amfi_code,
        "scheme_name": fund_name,
        "latest_nav": nav_data[-1]['nav'] if nav_data else None,
        "latest_date": nav_data[-1]['date'] if nav_data else None,
        "last_30_days": nav_data
    })

# ─────────────────────────────────────────
# ROUTE 5 - SIP Trends
# ─────────────────────────────────────────
@app.route('/api/sip-trends')
def get_sip_trends():
    sip_data = sip[['month', 'sip_inflow_crore', 
                     'active_sip_accounts_crore']].to_dict(orient='records')
    
    return jsonify({
        "total_months": len(sip_data),
        "latest_inflow_crore": sip_data[-1]['sip_inflow_crore'],
        "data": sip_data
    })

# ─────────────────────────────────────────
# ROUTE 6 - Top Performers
# ─────────────────────────────────────────
@app.route('/api/top-performers')
def get_top_performers():
    perf_cols = [c for c in scheme_perf.columns]
    
    top = scheme_perf.head(10).to_dict(orient='records')
    
    return jsonify({
        "total": len(top),
        "top_performers": top
    })

# ─────────────────────────────────────────
# RUN APP
# ─────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)