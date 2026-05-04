from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

FILE = 'Book2.xlsx'

def load_sheet(sheet):
    df = pd.read_excel(FILE, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('₹', 'Rs')
    return df

@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'api': 'Electrical Industry Dashboard API',
        'version': '1.0',
        'endpoints': {
            'revenue':  '/api/revenue',
            'sectors':  '/api/sectors',
            'projects': '/api/projects',
            'summary':  '/api/summary'
        }
    })

@app.route('/api/revenue')
def revenue():
    df = load_sheet('Monthly_Revenue')
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/sectors')
def sectors():
    df = load_sheet('Sector_Analysis')
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/projects')
def projects():
    df = load_sheet('Upcoming_Projects')
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/summary')
def summary():
    rev  = load_sheet('Monthly_Revenue')
    proj = load_sheet('Upcoming_Projects')
    sec  = load_sheet('Sector_Analysis')

    # Find value column safely regardless of exact name
    val_col  = [c for c in proj.columns if 'Value' in c or 'value' in c]
    rev_col  = [c for c in rev.columns  if 'Revenue' in c or 'revenue' in c]
    grow_col = [c for c in rev.columns  if 'Growth' in c or 'growth' in c]

    return jsonify({
        'total_revenue_cr':    int(rev[rev_col[0]].sum())   if rev_col  else 0,
        'avg_growth_pct':      round(float(rev[grow_col[0]].mean()) * 100, 1) if grow_col else 0,
        'total_pipeline_cr':   int(proj[val_col[0]].sum())  if val_col  else 0,
        'companies':           int(rev['Company'].nunique()),
        'sectors':             int(sec['Sector'].nunique()) if 'Sector' in sec.columns else 0,
        'last_updated':        pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)