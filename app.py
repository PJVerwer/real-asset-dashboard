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
        <p>This pilot project estimates the size of the real asset universe &#8212; defined as structures (residential and non-residential buildings and infrastructure) and the land on which they sit. This tool provides a multi-level view of the built environment, based on official OECD National Account data and extending estimates globally using Penn World Table bridges.</p>
        <p><b>Market USD:</b> All global and country figures are expressed in USD at market exchange rates for the reference year 2023.</p>
    </div>
    """, unsafe_allow_html=True)

    st.header("Global Hybrid Estimates (Market USD)")

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='hybrid-box'><h3>Structures</h3><h1>${int(s['global_structures'])}T</h1></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='hybrid-box'><h3>Land</h3><h1>${int(s['global_land'])}T</h1></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='hybrid-box'><h3>Total Real Assets</h3><h1>${int(s['global_total'])}T</h1></div>", unsafe_allow_html=True)

    oecd_dw   = s['oecd_dwellings']
    oecd_oth  = s['oecd_other']
    oecd_ts   = s['oecd_total_struc']
    oecd_land = s['oecd_land']
    st.markdown(f"""
    <div class="oecd-card">
        <h2 style="margin-top:0;">OECD Subset: Deep Dive</h2>
        <p style="color:#64748b; font-size:0.95rem; margin-bottom:20px;">
            The OECD dataset serves as the high-transparency primary anchor for this project, covering 33 member countries with direct national account reporting.
        </p>
        <div class="metric-row"><span class="label">Dwellings (Residential Buildings)</span><span class="value">${oecd_dw}T</span></div>
        <div class="metric-row"><span class="label">Other Buildings &amp; Structures (Commercial + Infrastructure)</span><span class="value">${oecd_oth}T</span></div>
        <div class="metric-row" style="background-color:#f8fafc; padding:10px; border-radius:8px;"><span class="label"><b>Total OECD Structures</b></span><span class="value"><b>${oecd_ts}T</b></span></div>
        <div class="metric-row"><span class="label">Land (OECD Reported + US Imputed)</span><span class="value">${oecd_land}T</span></div>
        <div class="oecd-total">
            <span>TOTAL OECD REAL ASSETS</span>
            <span>$253.5T</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 2: COUNTRY GALLERY ---
with tab2:
    st.title("Country Benchmark Gallery")
    st.markdown("#### All Figures in **USD Billions** at Market Rates")

    st.sidebar.title("Gallery Controls")
    search = st.sidebar.text_input("🔍 Filter by Country Name", "")
    sort_choice = st.sidebar.selectbox("Sort By:", ["Total Value", "Structures/GDP", "Alphabetical"])

    display_df = df.copy()
    display_df['Country'] = display_df['Country'].replace(
        {"Taiwan, Province of China": "Taiwan", "Taiwan Province of China": "Taiwan"}
    )
    for col in ("Combined_bn", "S_GDP"):
        display_df[col] = pd.to_numeric(display_df[col], errors='coerce')

    if search:
        display_df = display_df[display_df['Country'].str.contains(search, case=False)]

    if sort_choice == "Total Value":
        display_df = display_df.sort_values("Combined_bn", ascending=False, na_position='last')
    elif sort_choice == "Structures/GDP":
        display_df = display_df.sort_values("S_GDP", ascending=False, na_position='last')
    else:
        display_df = display_df.sort_values("Country")

    cols_per_row = 3
    for i in range(0, len(display_df), cols_per_row):
        row_data = display_df.iloc[i:i+cols_per_row]
        cols = st.columns(cols_per_row)
        for j, (_, country) in enumerate(row_data.iterrows()):
            with cols[j]:
                def fmt(val, suffix=""): return f"{val:,.1f}{suffix}" if pd.notnull(val) and val != 0 else "&#8212;"
                def pct(val): return f"{val*100:.1f}%" if pd.notnull(val) and val != 0 else "&#8212;"

                cname      = country['Country']
                s_bn       = fmt(country['Structures_bn'])
                l_bn       = fmt(country['Land_bn'])
                c_bn       = fmt(country['Combined_bn'])
                s_gdp      = fmt(country['S_GDP'], 'x')
                c_gdp      = fmt(country['C_GDP'], 'x')
                s_mc       = fmt(country['S_MC'], 'x')
                s_fa       = pct(country['S_FA'])

                st.markdown(f"""
                <div class="country-card">
                    <div style="font-size:1.2rem; font-weight:800; color:#011627; margin-bottom:15px; border-bottom:2px solid #ff9f1c; padding-bottom:5px;">
                        {cname}
                    </div>
                    <div style="background-color:#f1f5f9; padding:12px; border-radius:8px; margin-bottom:20px;">
                        <div class="metric-row"><span class="label">Structures</span><span class="value">${s_bn}bn</span></div>
                        <div class="metric-row"><span class="label">Land</span><span class="value">${l_bn}bn</span></div>
                        <div class="metric-row" style="border:none; font-weight:800; font-size:1rem; padding-top:5px; color:#011627;">
                            <span class="label" style="color:#011627;">Combined Real Assets</span><span class="value">${c_bn}bn</span>
                        </div>
                    </div>
                    <div style="font-size:0.75rem; font-weight:800; color:#ff9f1c; text-transform:uppercase; margin-bottom:10px; letter-spacing:0.05em;">Efficiency &amp; Intensity Benchmarks</div>
                    <div class="metric-row"><span class="label">Real Assets (Struct) / GDP</span><span class="value">{s_gdp}</span></div>
                    <div class="metric-row"><span class="label">Combined Assets / GDP</span><span class="value">{c_gdp}</span></div>
                    <div class="metric-row"><span class="label">Structures / Stock Market Cap</span><span class="value">{s_mc}</span></div>
                    <div class="metric-row" style="border:none;"><span class="label">Structures / Fixed Assets</span><span class="value">{s_fa}</span></div>
                </div>
                """, unsafe_allow_html=True)

# --- TAB 3: VERBATIM METHODOLOGY ---
with tab3:
    st.markdown("""
    <div class="meth-section">
    <h1>Global Real Asset Capital Stock</h1>
    <h2>Objectives, Methodology &amp; Data Sources</h2>
    <p>April 2026  |  Working Paper  |  Version 3c</p>
    <hr>

    <h3>1. Objective</h3>
    <p>This project estimates the global stock of real assets &#8212; defined as structures (residential and non-residential buildings and infrastructure) and the land on which they sit &#8212; expressed in USD at both market exchange rates and purchasing power parity (PPP). [cite: 5]</p>
    <p>The aim is a credible, internally consistent figure that can be benchmarked against macroeconomic and financial aggregates, including: [cite: 6]</p>
    <ul>
        <li>Gross domestic product (GDP) [cite: 7]</li>
        <li>Net national wealth / total national balance sheets [cite: 8]</li>
        <li>Total fixed assets (produced capital) [cite: 9]</li>
        <li>Equity market capitalisation [cite: 10]</li>
    </ul>
    <p>The analysis is designed to produce not merely a single global headline number, but a transparent country-level dataset that supports cross-country comparison and sensitivity analysis. [cite: 11]</p>

    <h3>2. Methodology</h3>

    <p><b>2.1 Valuation basis</b><br>
    All estimates are on a depreciated replacement cost basis (book value per national accounts), not market value. [cite: 14] This reflects the valuation approach embedded in the primary data source (OECD national balance sheets). [cite: 15] The gap between book value and market value can be material &#8212; particularly for residential land and prime commercial property &#8212; and is noted explicitly as a limitation. [cite: 16]</p>
    <p>An exception applies to United States land, which is derived from the Federal Reserve Financial Accounts (Z.1 release) using a residual method that implies market value. [cite: 17] Because land does not depreciate, the difference between book value and market value is not considered material for the land component specifically; this assumption is disclosed. [cite: 18, 19]</p>

    <p><b>2.2 Asset scope</b><br>
    Real assets are defined to include dwellings (residential buildings), other buildings and structures (non-residential buildings, infrastructure, civil engineering works), and land reported separately as a second component alongside structures. [cite: 21-24]</p>
    <p>Explicitly excluded from the estimate: machinery, equipment and weapons systems; intellectual property products (software, R&amp;D, mineral exploration); inventories; mineral and energy reserves; non-cultivated biological resources and water rights; and intangible non-produced assets. [cite: 25-31]</p>

    <p><b>2.3 Two-tier estimation approach</b><br>
    <b>Step 1 &#8212; OECD anchor:</b> For 33 OECD member countries, national balance sheet data from OECD Table 9B provides the primary estimate. [cite: 33] Note: Bulgaria and Romania are excluded as non-OECD members. [cite: 35]<br>
    <b>Step 2 &#8212; Global gross-up:</b> OECD data covers approximately 60% of the global capital stock (by market exchange rate) as implied by Penn World Table 11.0. [cite: 36] OECD country totals are scaled by the inverse of this share to derive a global estimate. [cite: 37] Non-OECD countries are represented only through this proportional bridge. [cite: 38]</p>

    <p><b>2.4 Land treatment: AN.211 classification and US imputation</b><br>
    Land values are sourced from OECD Table 9B sub-classification AN.211 ("Land, net"). [cite: 40] This classification explicitly excludes mineral and energy reserves. [cite: 41, 42] Of 33 OECD countries, 15 report AN.211 Land. [cite: 45] The remaining 17 countries are excluded from the land component, making the OECD land total a partial lower bound. [cite: 46, 47]</p>
    <p><b>United States:</b> Imputed via Federal Reserve Z.1 residual method. [cite: 48] Real estate at market value ($48.9 trillion, Q4 2023) less replacement cost of structures ($30.3 trillion) equals household-sector land of $18.6 trillion. [cite: 50] This is grossed up to the total economy using a 67.5% ratio based on Canada and UK comparability. [cite: 51-54]</p>

    <p><b>2.5 Currency conversion</b><br>
    Local currency values are converted using 2023 annual averages from IMF World Economic Outlook (April 2024) and 2023 PPP rates. [cite: 57-59]</p>

    <p><b>2.6 Reference year</b><br>
    The primary reference year is 2023. Where unavailable, the most recent prior year with data is used. [cite: 61-63]</p>

    <p><b>2.7 Equity market capitalisation benchmark</b><br>
    Sourced from WFE December 2023 Annual Statistics. [cite: 65] For countries under Euronext or Nasdaq Nordic, individual figures are estimated by weighting the aggregate by country-specific index market capitalisation. [cite: 69, 72] The UK figure is derived from the FTSE All-Share index as the LSE is absent from WFE 2023 statistics. [cite: 74-76]</p>

    <h3>3. Data Sources</h3>
    <table>
        <thead>
            <tr><th>Source</th><th>Dataset / Variables Used</th><th>Role</th></tr>
        </thead>
        <tbody>
            <tr><td>OECD Table 9B</td><td>Annual Balance Sheets for Non-Financial Assets. Variables: Fixed assets net, Dwellings net, Other buildings and structures net, AN.211 Land net.</td><td>Primary anchor &#8212; 33 OECD countries</td></tr>
            <tr><td>Penn World Table 11.0</td><td>Capital Detail Data. Variable: Nc_Struc. 180 countries, 1950&#8211;2023.</td><td>Global gross-up &#8212; OECD share calculation</td></tr>
            <tr><td>IMF WEO</td><td>World Economic Outlook, April 2024. Market rate and PPP actuals for 2023.</td><td>Currency conversion &#8212; all countries</td></tr>
            <tr><td>Federal Reserve Z.1</td><td>Table B.101. Real estate at market value; Replacement cost of structures. Q4 2023.</td><td>US land imputation</td></tr>
            <tr><td>WFE</td><td>WFE Annual Statistics, Dec 2023. Domestic equity market capitalisation.</td><td>Equity market cap benchmark</td></tr>
        </tbody>
    </table>

    <h3>4. Known Issues and Limitations</h3>
    <table>
        <thead>
            <tr><th>Category</th><th>Issue</th></tr>
        </thead>
        <tbody>
            <tr><td>Valuation basis</td><td>Book value systematically understates market value, most acutely for residential land. No market-value adjustment is applied. [cite: 86]</td></tr>
            <tr><td>Book vs. market &#8212; land</td><td>National accounts often reflect administrative assessments. US land estimate uses a market-value residual. [cite: 86]</td></tr>
            <tr><td>Infrastructure as residual</td><td>OECD data combines commercial property and infrastructure; they cannot be isolated without national sources. [cite: 86]</td></tr>
            <tr><td>Natural resources</td><td>This version uses AN.211 specifically to exclude mineral and energy reserves, water, and biological resources. [cite: 86]</td></tr>
            <tr><td>Land coverage &#8212; OECD</td><td>Only 15 OECD countries report AN.211 data. The OECD land total is a partial lower bound. [cite: 86]</td></tr>
            <tr><td>US land &#8212; imputed</td><td>Derived from a residual simplification; excludes government-owned land. Flagged (I) throughout the workbook. [cite: 86]</td></tr>
            <tr><td>Non-OECD coverage</td><td>Estimated via PWT relative shares &#8212; a materially less reliable approach than national accounts. [cite: 86]</td></tr>
            <tr><td>Equity Mkt Cap &#8212; UK</td><td>UK market capitalisation (~$2,670bn) is derived from the FTSE All-Share index as LSEG is absent from WFE 2023 statistics. [cite: 86]</td></tr>
        </tbody>
    </table>

    <hr>
    <p><i>This document accompanies the Excel workbook Global_Real_Capital_Stock_V3c_2023.xlsx. Version 3 incorporates AN.211 clean land sub-classification, US land imputation, and updated WFE market capitalisation figures. [cite: 87-93]</i></p>
    </div>
    """, unsafe_allow_html=True)
