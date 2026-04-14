import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Experimental real asset universe size estimate", layout="wide")

# Enhanced CSS
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .page-guide { background-color: #f8fafc; border-radius: 12px; padding: 25px; border-left: 6px solid #ff9f1c; margin-bottom: 25px; }
    .hybrid-box { background-color: #011627; color: #ffffff !important; border-radius: 12px; padding: 25px; text-align: center; border: 1px solid #ff9f1c; }
    .hybrid-box h1 { color: #ffffff !important; margin: 0; font-size: 2.8rem; }
    .hybrid-box h3 { color: #ff9f1c !important; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.1em; }
    .oecd-card { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 35px; margin-top: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .country-card { background-color: #ffffff; border-radius: 12px; padding: 20px; border: 1px solid #e2e8f0; border-top: 5px solid #011627; box-shadow: 0 2px 4px rgba(0,0,0,0.05); min-height: 420px; }
    .metric-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 0.9rem; }
    .label { color: #64748b; }
    .value { font-weight: 700; color: #0f172a; }
    .oecd-total { font-size: 1.5rem; font-weight: 800; color: #011627; border-top: 3px solid #ff9f1c; margin-top: 15px; padding-top: 15px; display: flex; justify-content: space-between; }
    .meth-section { line-height: 1.6; color: #1e293b; font-size: 0.95rem; }
    .meth-section h3 { margin-top: 30px; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }
    table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.85rem; }
    th { background-color: #f1f5f9; text-align: left; padding: 12px; border: 1px solid #e2e8f0; }
    td { padding: 12px; border: 1px solid #e2e8f0; vertical-align: top; }
</style>
""", unsafe_allow_html=True)

# 2. Data Loading
@st.cache_data
def load_data():
    master = pd.read_csv('dashboard_master_v4.csv')
    summary_raw = pd.read_csv('summary_stats_v4.csv')
    summary = dict(zip(summary_raw['Metric'], summary_raw['Value']))
    return master, summary

df, s = load_data()

# 3. Navigation
tab1, tab2, tab3 = st.tabs(["📊 Executive Summary", "🏙️ Country Benchmark Gallery", "📖 Methodology & Sources"])

# --- TAB 1: EXECUTIVE SUMMARY ---
with tab1:
    st.markdown("""
    <div class="page-guide">
        <h2 style="margin-top:0;">Experimental real asset universe size estimate</h2>
        <p>This pilot project estimates the size of the real asset universe — defined as structures (residential and non-residential buildings and infrastructure) and the land on which they sit. This tool provides a multi-level view of the built environment, based on official OECD National Account data and extending estimates globally using Penn World Table bridges.</p>
        <p><b>Market USD:</b> All global and country figures are expressed in USD at market exchange rates for the reference year 2023.</p>
    </div>
    """, unsafe_allow_html=True)

    st.header("Global Hybrid Estimates (Market USD)")

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='hybrid-box'><h3>Structures</h3><h1>${int(s['global_structures'])}T</h1></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='hybrid-box'><h3>Land</h3><h1>${int(s['global_land'])}T</h1></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='hybrid-box'><h3>Total Real Assets</h3><h1>${int(s['global_total'])}T</h1></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="oecd-card">
        <h2 style="margin-top:0;">OECD Subset: Deep Dive</h2>
        <p style="color:#64748b; font-size:0.95rem; margin-bottom:20px;">
            The OECD dataset serves as the high-transparency primary anchor for this project, covering 33 member countries with direct national account reporting.
        </p>
        <div class="metric-row">
