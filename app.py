import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="MBM Revenue Estimation Model",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────
# ACADEMIC / Q1 JOURNAL DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --ink:       #1a1a2e;
    --ink-soft:  #3d3d5c;
    --ink-muted: #6b6b8a;
    --rule:      #d4c9b0;
    --paper:     #faf8f4;
    --paper-2:   #f3efe8;
    --accent:    #1b4f72;
    --accent-2:  #c0392b;
    --gold:      #b7860b;
    --mono:      'JetBrains Mono', monospace;
}

html, body, [class*="css"] {
    font-family: 'Source Serif 4', Georgia, serif;
    background-color: var(--paper) !important;
    color: var(--ink) !important;
}
.main { background-color: var(--paper) !important; }
.block-container {
    padding: 2.5rem 3rem 3rem 3rem !important;
    max-width: 1280px !important;
}

section[data-testid="stSidebar"] {
    background-color: var(--ink) !important;
    border-right: 1px solid #2e2e4a;
}
section[data-testid="stSidebar"] * {
    color: #c8c8dc !important;
    font-family: 'Source Serif 4', serif !important;
}
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    font-size: 0.78rem !important;
    letter-spacing: 0.01em;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #e8e8f0 !important;
    font-family: 'Playfair Display', serif !important;
}

.journal-header {
    border-top: 3px double var(--ink);
    border-bottom: 1px solid var(--ink);
    padding: 1.4rem 0 1rem 0;
    margin-bottom: 0.2rem;
}
.journal-meta {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--ink-muted);
    font-family: 'Source Serif 4', serif;
    font-weight: 300;
    margin-bottom: 0.5rem;
}
.journal-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.0rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.15;
    margin: 0.3rem 0;
    letter-spacing: -0.01em;
}
.journal-subtitle {
    font-family: 'Source Serif 4', serif;
    font-style: italic;
    font-size: 1.0rem;
    color: var(--ink-soft);
    margin: 0.4rem 0 0 0;
    font-weight: 300;
}
.journal-rule {
    border: none;
    border-top: 1px solid var(--ink);
    margin: 0.8rem 0 1.5rem 0;
}

.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    font-family: 'Source Serif 4', serif;
    font-weight: 600;
    margin-bottom: 0.15rem;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--ink);
    border-bottom: 1px solid var(--rule);
    padding-bottom: 0.35rem;
    margin: 1.6rem 0 0.8rem 0;
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1px;
    background: var(--ink);
    border: 1px solid var(--ink);
    margin-bottom: 1.8rem;
}
.kpi-card {
    background: var(--paper);
    padding: 1rem 1.2rem;
    text-align: left;
}
.kpi-label {
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--ink-muted);
    font-family: 'Source Serif 4', serif;
    font-weight: 300;
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1;
}
.kpi-sub {
    font-size: 0.70rem;
    color: var(--accent);
    font-family: 'Source Serif 4', serif;
    margin-top: 0.2rem;
    font-weight: 300;
}

.fig-caption {
    font-size: 0.78rem;
    color: var(--ink-muted);
    font-style: italic;
    text-align: left;
    margin-top: 0.3rem;
    border-top: 1px solid var(--rule);
    padding-top: 0.4rem;
    font-family: 'Source Serif 4', serif;
}
.fig-label {
    font-weight: 600;
    font-style: normal;
    color: var(--ink-soft);
    font-size: 0.72rem;
    letter-spacing: 0.05em;
}

.abstract-box {
    border-left: 3px solid var(--ink);
    background: var(--paper-2);
    padding: 1rem 1.4rem;
    margin: 1rem 0 1.5rem 0;
    font-size: 0.88rem;
    line-height: 1.75;
    color: var(--ink-soft);
    font-family: 'Source Serif 4', serif;
}

.footnote {
    font-size: 0.72rem;
    color: var(--ink-muted);
    border-top: 1px solid var(--rule);
    padding-top: 0.5rem;
    margin-top: 1rem;
    font-family: 'Source Serif 4', serif;
    font-style: italic;
}

.mech-badge {
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.05em;
    padding: 3px 8px;
    border-radius: 2px;
    margin: 2px;
}
.mech-on  { background: #1b4f72; color: #d6e8f5; }
.mech-off { background: #e8e4dc; color: #8a8a9a; }

.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid var(--ink) !important;
    gap: 0 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Source Serif 4', serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--ink-muted) !important;
    padding: 0.5rem 1.2rem !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
    color: var(--ink) !important;
    border-bottom: 2px solid var(--ink) !important;
    font-weight: 600 !important;
}

.sidebar-section {
    font-family: 'Playfair Display', serif !important;
    font-size: 0.80rem !important;
    color: #9090b0 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid #2e2e4a !important;
    padding-bottom: 0.3rem !important;
    margin: 1.2rem 0 0.6rem 0 !important;
}

.stSelectbox label, .stNumberInput label, .stSlider label {
    font-family: 'Source Serif 4', serif !important;
    font-size: 0.8rem !important;
    color: var(--ink-soft) !important;
}

.stButton > button {
    font-family: 'Source Serif 4', serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    background: var(--ink) !important;
    color: var(--paper) !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0.5rem 1.2rem !important;
}
.stButton > button:hover { background: var(--accent) !important; }

hr { border-color: var(--rule) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────
TECHNOLOGIES = [
    "Solar PV & Wind Energy", "Green Hydrogen", "SAF (Sust. Aviation Fuel)",
    "CCUS", "Battery Storage & EVs", "Low-carbon Steel & Cement",
    "Ammonia (green/blue)", "Methanol (green/e-methanol)",
    "Reforestation / REDD+ / NBS", "Blue Carbon (mangroves)",
    "Direct Air Capture (DAC)", "Building Energy Efficiency",
    "Carbon Offsetting / MRV Tech", "Energy Mgmt & Analytics",
]
TECH_SHORT = [
    "Solar/Wind","Green H₂","SAF","CCUS",
    "Battery/EV","Steel/Cement","Ammonia","Methanol",
    "Reforestation","Blue Carbon","DAC","Bldg Eff.",
    "MRV Tech","Energy Mgmt"
]
DEFAULTS = {
    "annual_output":      [500000,50000,150000,100000,300000,250000,180000,120000,80000,30000,50000,400000,0,0],
    "installed_capacity": [200,100,80,50,150,50,80,60,0,0,25,0,10,5],
    "capacity_factor":    [0.30,0.45,0.85,0.90,0.25,0.90,0.90,0.90,1.0,1.0,0.95,1.0,0.90,0.95],
    "project_lifetime":   [25,20,20,30,15,25,25,20,30,30,20,20,15,10],
    "capex_per_kw":       [1200,2500,3000,4000,1800,5000,3500,3200,500,300,150,800,400,200],
    "opex_pct":           [0.015,0.025,0.030,0.035,0.020,0.040,0.030,0.030,0.10,0.12,0.05,0.05,0.08,0.10],
    "feedstock_cost":     [0,8e6,6e6,2e6,1e6,5e6,4e6,3e6,5e5,2e5,3e6,0,0,0],
    "other_opex":         [5e5,2e6,1.5e6,1e6,8e5,2e6,1.5e6,1.2e6,3e5,1e5,2e6,1e6,5e5,8e5],
    "wacc":               [0.07,0.09,0.10,0.10,0.08,0.10,0.09,0.09,0.06,0.06,0.10,0.07,0.08,0.08],
    "market_price":       [70,4500,2800,80,90,700,950,1300,12,30,500,100,50000,25000],
    "clients":            [0,0,0,0,0,0,0,0,0,0,0,0,30,20],
    "co2_abated_factor":  [0.45,0.90,0.70,0.85,0.30,0.80,0.85,0.75,1.0,1.0,1.0,0.40,0.95,0.35],
    "ets":    [1,1,1,1,0,1,1,1,0,0,1,1,1,1],
    "ctax":   [1,1,1,1,1,1,1,1,1,0,1,1,1,1],
    "fuel":   [0,0,1,0,1,0,0,0,0,0,0,0,0,0],
    "cfd":    [1,1,1,1,0,1,1,1,0,0,1,0,0,0],
    "cbam":   [0,1,0,1,0,1,1,0,0,0,0,0,0,1],
    "corsia": [0,0,1,0,0,0,0,0,0,0,0,0,1,0],
    "imo":    [0,1,0,0,0,0,1,1,0,0,0,0,1,1],
    "vcm":    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    "amc":    [1,1,1,1,1,1,1,1,1,0,1,0,0,0],
    "feebate":[0,0,0,0,1,0,0,0,0,0,0,1,0,0],
}
DEFAULT_PRICES = {
    "ets":100,"ctax":50,"fuel":240,"cfd_strike":120,"cfd_ref":80,
    "cbam":55,"corsia":22.25,"imo":380,"vcm":100,"amc":100,
    "feebate":50,"electricity":60,"gas":8,"biomass":40
}

ACADEMIC_COLORS = [
    "#1b4f72","#c0392b","#b7860b","#1a5276","#6e2f1a",
    "#1d6a3e","#4a235a","#7b241c","#0e6655","#2c3e50"
]
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(250,248,244,0)",
    plot_bgcolor="rgba(250,248,244,0)",
    font=dict(family="Source Serif 4, Georgia, serif", size=11, color="#1a1a2e"),
    title_font=dict(family="Playfair Display, serif", size=13, color="#1a1a2e"),
    legend=dict(
        bgcolor="rgba(250,248,244,0.9)",
        bordercolor="#d4c9b0", borderwidth=1,
        font=dict(size=10, family="Source Serif 4, serif")
    ),
    xaxis=dict(
        showgrid=True, gridcolor="#e8e4dc", gridwidth=0.5,
        linecolor="#1a1a2e", linewidth=0.8,
        tickfont=dict(size=9, family="JetBrains Mono, monospace"),
        title_font=dict(size=10, family="Source Serif 4, serif")
    ),
    yaxis=dict(
        showgrid=True, gridcolor="#e8e4dc", gridwidth=0.5,
        linecolor="#1a1a2e", linewidth=0.8,
        tickfont=dict(size=9, family="JetBrains Mono, monospace"),
        title_font=dict(size=10, family="Source Serif 4, serif")
    ),
    margin=dict(l=60, r=20, t=40, b=60),
)

# ─────────────────────────────────────────────────────────────────
# CALCULATION ENGINE
# ─────────────────────────────────────────────────────────────────
def calc_crf(wacc, lifetime):
    if wacc == 0: return 1/lifetime
    return (wacc*(1+wacc)**lifetime) / ((1+wacc)**lifetime - 1)

def compute_revenues(prices, t, ti):
    output     = ti["annual_output"][t]
    cap_kw     = ti["installed_capacity"][t] * 1000
    lifetime   = ti["project_lifetime"][t]
    wacc       = ti["wacc"][t]
    capex_kw   = ti["capex_per_kw"][t]
    opex_pct   = ti["opex_pct"][t]
    feedstock  = ti["feedstock_cost"][t]
    other_opex = ti["other_opex"][t]
    mkt_price  = ti["market_price"][t]
    co2_factor = ti["co2_abated_factor"][t]
    clients    = ti["clients"][t]

    capex_total = capex_kw * cap_kw
    ann_capex   = capex_total * calc_crf(wacc, lifetime)
    fixed_opex  = capex_total * opex_pct
    total_cost  = ann_capex + fixed_opex + feedstock + other_opex
    co2_abated  = output * co2_factor

    direct_rev  = (clients * mkt_price) if t in [12,13] else (output * mkt_price)
    ets_rev     = co2_abated * prices["ets"]     if DEFAULTS["ets"][t]     else 0
    ctax_rev    = co2_abated * prices["ctax"]    if DEFAULTS["ctax"][t]    else 0
    vcm_rev     = co2_abated * prices["vcm"]     if DEFAULTS["vcm"][t]     else 0
    fuel_rev    = (output * ti["capacity_factor"][t] * prices["fuel"] * 0.85) if DEFAULTS["fuel"][t] and output > 0 else 0
    cfd_rev     = (output * max(0, prices["cfd_strike"] - prices["cfd_ref"]) * 0.5) if DEFAULTS["cfd"][t] and output > 0 else 0
    cbam_rev    = co2_abated * prices["cbam"] * 0.85   if DEFAULTS["cbam"][t]   else 0
    corsia_rev  = co2_abated * prices["corsia"] * 1.05 if DEFAULTS["corsia"][t] else 0
    imo_rev     = co2_abated * prices["imo"] * 0.95    if DEFAULTS["imo"][t]    else 0
    amc_rev     = (output/1000) * prices["amc"] * 0.5  if DEFAULTS["amc"][t]   else 0
    feebate_rev = co2_abated * prices["feebate"] * 0.5 if DEFAULTS["feebate"][t] else 0

    mbm_total = ets_rev+ctax_rev+fuel_rev+cfd_rev+cbam_rev+corsia_rev+imo_rev+vcm_rev+amc_rev+feebate_rev
    total_rev = mbm_total + direct_rev
    return {
        "capex_total":capex_total,"ann_capex":ann_capex,"fixed_opex":fixed_opex,
        "total_cost":total_cost,"co2_abated":co2_abated,"direct_rev":direct_rev,
        "mbm_total":mbm_total,"total_rev":total_rev,"net_cf":total_rev-total_cost,
        "lifetime_rev":total_rev*lifetime,
        "rev_cost_ratio":total_rev/total_cost if total_cost>0 else 0,
        "mbm_breakdown":{
            "ETS":ets_rev,"Carbon Tax":ctax_rev,"Fuel Mandate":fuel_rev,
            "CfD":cfd_rev,"CBAM":cbam_rev,"CORSIA":corsia_rev,
            "IMO Levy":imo_rev,"VCM/CDM":vcm_rev,"AMC":amc_rev,"Feebate":feebate_rev
        }
    }

# ─────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────
if "tech_inputs" not in st.session_state:
    st.session_state.tech_inputs = {k: list(v) for k, v in DEFAULTS.items()}
if "prices" not in st.session_state:
    st.session_state.prices = dict(DEFAULT_PRICES)

def fmt_m(v): return f"${v/1e6:,.1f}M"

# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### MBM Parameters")
    st.caption("Adjust global market-based mechanism prices")
    p = st.session_state.prices

    st.markdown('<div class="sidebar-section">Carbon Markets</div>', unsafe_allow_html=True)
    p["ets"]     = st.slider("ETS / Carbon Market (USD/tCO₂e)", 10, 300, p["ets"], 5)
    p["ctax"]    = st.slider("Carbon Tax Rate (USD/tCO₂e)", 0, 200, p["ctax"], 5)
    p["vcm"]     = st.slider("VCM / CDM Credit (USD/tCO₂e)", 5, 300, p["vcm"], 5)
    p["cbam"]    = st.slider("CBAM Import Cost (USD/tCO₂e)", 10, 150, p["cbam"], 5)
    p["corsia"]  = st.slider("CORSIA Credit (USD/tCO₂e)", 3, 100, int(p["corsia"]), 1)
    p["imo"]     = st.slider("IMO Levy (USD/tCO₂e)", 50, 800, p["imo"], 10)
    p["feebate"] = st.slider("Feebate Rate (USD/tCO₂e)", 0, 150, p["feebate"], 5)

    st.markdown('<div class="sidebar-section">Policy Instruments</div>', unsafe_allow_html=True)
    p["cfd_strike"] = st.slider("CfD Strike Price (USD/MWh)", 50, 300, p["cfd_strike"], 5)
    p["cfd_ref"]    = st.slider("CfD Reference Price (USD/MWh)", 30, 200, p["cfd_ref"], 5)
    p["fuel"]       = st.slider("Fuel Mandate Price (USD/MWh)", 100, 600, p["fuel"], 10)
    p["amc"]        = st.slider("AMC Price (USD/unit)", 50, 300, p["amc"], 10)

    st.markdown('<div class="sidebar-section">Commodity Inputs</div>', unsafe_allow_html=True)
    p["electricity"] = st.slider("Grid Electricity (USD/MWh)", 20, 200, p["electricity"], 5)
    p["gas"]         = st.slider("Natural Gas (USD/MMBtu)", 2, 30, p["gas"], 1)
    p["biomass"]     = st.slider("Biomass Feedstock (USD/MWh)", 10, 120, p["biomass"], 5)

    st.session_state.prices = p
    st.divider()
    if st.button("↺  Reset to Default Values", use_container_width=True):
        st.session_state.prices = dict(DEFAULT_PRICES)
        st.session_state.tech_inputs = {k: list(v) for k, v in DEFAULTS.items()}
        st.rerun()

# ─────────────────────────────────────────────────────────────────
# JOURNAL HEADER
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="journal-header">
    <div class="journal-meta">Revenue Estimation Model &nbsp;·&nbsp; Technology Innovation &nbsp;·&nbsp; Market-Based Mechanisms</div>
    <div class="journal-title">Revenue Estimation Model for Technology Innovation<br>under Market-Based Mechanism Interventions</div>
    <div class="journal-subtitle">An integrated techno-economic framework for carbon pricing, policy instruments, and direct product revenue across sustainable technology portfolios</div>
</div>
<hr class="journal-rule">
<div class="abstract-box">
<strong>Abstract.</strong> This interactive model estimates annual and lifetime revenues for fourteen sustainable technology categories subject to market-based mechanism (MBM) interventions including emissions trading systems, carbon taxation, contracts for difference, border adjustment mechanisms, voluntary carbon markets, and advance market commitments. The framework integrates techno-economic inputs — capital cost annualisation via capital recovery factor, levelised cost estimation, and CO₂ abatement accounting — with parameterised policy price signals adjustable via the control panel. Outputs include per-mechanism revenue attribution, net annual cash flow, and portfolio-level aggregation under user-defined carbon price scenarios.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "I.  Portfolio Results",
    "II.  Technology Analysis",
    "III.  Scenario Analysis",
    "IV.  Data Tables"
])

# ═══════════════════════════════════════════════════════════════
# TAB I
# ═══════════════════════════════════════════════════════════════
with tab1:
    all_results = [compute_revenues(st.session_state.prices, i, st.session_state.tech_inputs) for i in range(14)]
    total_rev   = sum(r["total_rev"]  for r in all_results)
    total_mbm   = sum(r["mbm_total"]  for r in all_results)
    total_dir   = sum(r["direct_rev"] for r in all_results)
    total_cost  = sum(r["total_cost"] for r in all_results)
    total_netcf = sum(r["net_cf"]     for r in all_results)
    total_co2   = sum(r["co2_abated"] for r in all_results)
    mbm_share   = total_mbm/total_rev*100 if total_rev>0 else 0

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Total Annual Revenue</div>
            <div class="kpi-value">{fmt_m(total_rev)}</div>
            <div class="kpi-sub">Portfolio aggregate</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">MBM Revenue</div>
            <div class="kpi-value">{fmt_m(total_mbm)}</div>
            <div class="kpi-sub">{mbm_share:.1f}% of total</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Direct Product Revenue</div>
            <div class="kpi-value">{fmt_m(total_dir)}</div>
            <div class="kpi-sub">{100-mbm_share:.1f}% of total</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Net Annual Cash Flow</div>
            <div class="kpi-value">{fmt_m(total_netcf)}</div>
            <div class="kpi-sub">After OPEX &amp; CAPEX</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">CO₂ Abated</div>
            <div class="kpi-value">{total_co2/1e6:.2f}M</div>
            <div class="kpi-sub">tCO₂e per annum</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">§1. Revenue Attribution by Technology</div>', unsafe_allow_html=True)
    techs_sorted = sorted(range(14), key=lambda i: all_results[i]["total_rev"], reverse=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name="MBM Revenue",
        x=[TECH_SHORT[i] for i in techs_sorted],
        y=[all_results[i]["mbm_total"]/1e6 for i in techs_sorted],
        marker_color="#1b4f72", marker_line_width=0))
    fig1.add_trace(go.Bar(name="Direct Product Revenue",
        x=[TECH_SHORT[i] for i in techs_sorted],
        y=[all_results[i]["direct_rev"]/1e6 for i in techs_sorted],
        marker_color="#b7860b", marker_line_width=0))
    fig1.add_trace(go.Bar(name="Total Cost (OPEX+CAPEX)",
        x=[TECH_SHORT[i] for i in techs_sorted],
        y=[-all_results[i]["total_cost"]/1e6 for i in techs_sorted],
        marker_color="#c0392b", marker_line_width=0, opacity=0.75))
    fig1.update_layout(**PLOT_LAYOUT, barmode="relative", height=380,
        legend=dict(orientation="h", y=-0.28, x=0,
            bgcolor="rgba(250,248,244,0.9)", bordercolor="#d4c9b0", borderwidth=1,
            font=dict(size=10, family="Source Serif 4, serif")),
        yaxis_title="USD Million (annual)",
        xaxis=dict(**PLOT_LAYOUT["xaxis"], tickangle=-35))
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('<div class="fig-caption"><span class="fig-label">Figure 1.</span> Annual revenue decomposition by technology, ranked by total revenue. Negative bars represent annualised capital and operating expenditure. MBM revenues comprise policy-driven income streams; direct revenues reflect market sales of the primary product or service.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-title">§2. MBM Mechanism Mix</div>', unsafe_allow_html=True)
        mbm_agg = {}
        for r in all_results:
            for k, v in r["mbm_breakdown"].items():
                mbm_agg[k] = mbm_agg.get(k,0)+v
        mbm_f = {k:v for k,v in mbm_agg.items() if v>0}
        fig2 = go.Figure(go.Pie(
            labels=list(mbm_f.keys()), values=list(mbm_f.values()),
            hole=0.52, textinfo="label+percent",
            textfont=dict(family="Source Serif 4, serif", size=9),
            marker=dict(colors=ACADEMIC_COLORS, line=dict(color="#faf8f4", width=1.5))))
        fig2.update_layout(**PLOT_LAYOUT, height=320, showlegend=False, margin=dict(l=10,r=10,t=20,b=10))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="fig-caption"><span class="fig-label">Figure 2.</span> Portfolio-level MBM revenue distribution across active policy mechanisms.</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-title">§3. Net Cash Flow by Technology</div>', unsafe_allow_html=True)
        ncf_colors = ["#1b4f72" if all_results[i]["net_cf"]>=0 else "#c0392b" for i in range(14)]
        fig3 = go.Figure(go.Bar(
            x=TECH_SHORT, y=[all_results[i]["net_cf"]/1e6 for i in range(14)],
            marker_color=ncf_colors, marker_line_width=0))
        fig3.add_hline(y=0, line_color="#1a1a2e", line_width=0.8)
        fig3.update_layout(**PLOT_LAYOUT, height=320, yaxis_title="USD Million",
            xaxis=dict(**PLOT_LAYOUT["xaxis"], tickangle=-40,
                tickfont=dict(size=8, family="JetBrains Mono, monospace")))
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('<div class="fig-caption"><span class="fig-label">Figure 3.</span> Net annual cash flow per technology. Negative values (red) indicate operating deficit under current parameter assumptions.</div>', unsafe_allow_html=True)

    st.markdown('<div class="footnote">Note: All monetary values reported in nominal USD. MBM revenues are estimated using parameterised price signals applied to CO₂ abatement volumes derived from technology-specific emission factors. Total cost includes annualised CAPEX computed via the Capital Recovery Factor (CRF), fixed OPEX, feedstock costs, and other variable operating expenditures.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB II
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">§4. Technology-Level Parameter Configuration</div>', unsafe_allow_html=True)
    selected = st.selectbox("Select Technology", TECHNOLOGIES, index=0, label_visibility="collapsed")
    t  = TECHNOLOGIES.index(selected)
    ti = st.session_state.tech_inputs
    st.markdown(f"<div class='journal-meta' style='margin:0.5rem 0 1rem 0'>Configuring: <strong>{selected}</strong></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="section-label">Scale & Output</div>', unsafe_allow_html=True)
        ti["annual_output"][t]      = st.number_input("Annual Output (MWh/yr or t/yr)", 0, 10_000_000, int(ti["annual_output"][t]), 10000, key=f"ao_{t}")
        ti["installed_capacity"][t] = st.number_input("Installed Capacity (MW)", 0, 5000, int(ti["installed_capacity"][t]), 10, key=f"ic_{t}")
        ti["capacity_factor"][t]    = st.slider("Capacity Factor", 0.0, 1.0, ti["capacity_factor"][t], 0.01, key=f"cf_{t}")
        ti["project_lifetime"][t]   = st.slider("Project Lifetime (years)", 5, 50, int(ti["project_lifetime"][t]), 1, key=f"pl_{t}")
    with col2:
        st.markdown('<div class="section-label">Cost Structure</div>', unsafe_allow_html=True)
        ti["capex_per_kw"][t]   = st.number_input("CAPEX per kW (USD/kW)", 0, 20000, int(ti["capex_per_kw"][t]), 100, key=f"ck_{t}")
        ti["opex_pct"][t]       = st.slider("Fixed OPEX (% of CAPEX p.a.)", 0.0, 0.20, ti["opex_pct"][t], 0.005, format="%.3f", key=f"op_{t}")
        ti["feedstock_cost"][t] = st.number_input("Feedstock Cost (USD/yr)", 0, 50_000_000, int(ti["feedstock_cost"][t]), 100000, key=f"fc_{t}")
        ti["other_opex"][t]     = st.number_input("Other Variable OPEX (USD/yr)", 0, 20_000_000, int(ti["other_opex"][t]), 100000, key=f"ov_{t}")
        ti["wacc"][t]           = st.slider("WACC / Discount Rate", 0.01, 0.25, ti["wacc"][t], 0.005, format="%.3f", key=f"wc_{t}")
    with col3:
        st.markdown('<div class="section-label">Revenue Parameters</div>', unsafe_allow_html=True)
        ti["market_price"][t]      = st.number_input("Market Selling Price", 0, 100000, int(ti["market_price"][t]), 10, key=f"mp_{t}")
        ti["co2_abated_factor"][t] = st.slider("CO₂ Abated per Unit (tCO₂e/unit)", 0.0, 2.0, ti["co2_abated_factor"][t], 0.01, key=f"ca_{t}")
        if t in [12,13]:
            ti["clients"][t] = st.number_input("Number of Clients", 0, 10000, int(ti["clients"][t]), 1, key=f"cl_{t}")

    r = compute_revenues(st.session_state.prices, t, ti)
    st.divider()

    st.markdown(f"""
    <div class="kpi-grid" style="grid-template-columns:repeat(4,1fr)">
        <div class="kpi-card">
            <div class="kpi-label">Total Annual Revenue</div>
            <div class="kpi-value">{fmt_m(r["total_rev"])}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">MBM Revenue</div>
            <div class="kpi-value">{fmt_m(r["mbm_total"])}</div>
            <div class="kpi-sub">{r["mbm_total"]/r["total_rev"]*100 if r["total_rev"]>0 else 0:.1f}% of total</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Net Cash Flow</div>
            <div class="kpi-value">{fmt_m(r["net_cf"])}</div>
            <div class="kpi-sub">R/C Ratio: {r["rev_cost_ratio"]:.2f}×</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">CO₂ Abated</div>
            <div class="kpi-value">{r["co2_abated"]/1e3:.1f}k</div>
            <div class="kpi-sub">tCO₂e per annum</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title">§5. MBM Revenue Attribution</div>', unsafe_allow_html=True)
        mbm_data = {k:v for k,v in r["mbm_breakdown"].items() if v>0}
        if mbm_data:
            fig_mbm = go.Figure(go.Bar(
                x=list(mbm_data.keys()), y=[v/1e6 for v in mbm_data.values()],
                marker_color=ACADEMIC_COLORS[:len(mbm_data)], marker_line_width=0))
            fig_mbm.update_layout(**PLOT_LAYOUT, height=300, yaxis_title="USD Million")
            st.plotly_chart(fig_mbm, use_container_width=True)
            st.markdown(f'<div class="fig-caption"><span class="fig-label">Figure 4.</span> Active MBM revenue streams for {selected}.</div>', unsafe_allow_html=True)
        else:
            st.info("No active MBM mechanisms applicable for this technology.")

    with col_b:
        st.markdown('<div class="section-title">§6. Cost–Revenue Decomposition</div>', unsafe_allow_html=True)
        wf_cats = ["Direct Rev.","MBM Rev.","Ann. CAPEX","Fixed OPEX","Feedstock","Var. OPEX"]
        wf_vals = [r["direct_rev"]/1e6, r["mbm_total"]/1e6,
                   -r["ann_capex"]/1e6, -r["fixed_opex"]/1e6,
                   -ti["feedstock_cost"][t]/1e6, -ti["other_opex"][t]/1e6]
        wf_colors = ["#1b4f72","#b7860b","#c0392b","#c0392b","#c0392b","#c0392b"]
        fig_wf = go.Figure(go.Bar(
            x=wf_cats, y=wf_vals, marker_color=wf_colors, marker_line_width=0))
        fig_wf.add_hline(y=0, line_color="#1a1a2e", line_width=0.8)
        fig_wf.update_layout(**PLOT_LAYOUT, height=300, yaxis_title="USD Million",
            xaxis=dict(**PLOT_LAYOUT["xaxis"], tickangle=-25))
        st.plotly_chart(fig_wf, use_container_width=True)
        st.markdown(f'<div class="fig-caption"><span class="fig-label">Figure 5.</span> Cost–revenue waterfall for {selected}. Ann. CAPEX computed via CRF at WACC = {ti["wacc"][t]*100:.1f}%, T = {ti["project_lifetime"][t]} yr.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">§7. Applicable MBM Mechanisms</div>', unsafe_allow_html=True)
    mechs = [("ets","ETS"),("ctax","Carbon Tax"),("fuel","Fuel Mandate"),("cfd","CfD/CCfD"),
             ("cbam","CBAM"),("corsia","CORSIA"),("imo","IMO Levy"),("vcm","VCM/CDM"),
             ("amc","AMC"),("feebate","Feebate")]
    badges = "".join([f'<span class="mech-badge {"mech-on" if DEFAULTS[m][t] else "mech-off"}">{lbl}</span>' for m,lbl in mechs])
    st.markdown(badges, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB III
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">§8. Carbon Price Sensitivity Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="abstract-box" style="font-size:0.82rem">The following analysis holds all non-ETS parameters constant at their current sidebar values and varies the ETS carbon price across the range USD 10–300/tCO₂e. The dashed gold vertical line marks the current ETS parameter setting.</div>', unsafe_allow_html=True)

    base = dict(st.session_state.prices)
    ets_range = list(range(10, 310, 10))
    t_revs, m_revs, n_cfs = [], [], []
    for ep in ets_range:
        tp = dict(base); tp["ets"] = ep
        res = [compute_revenues(tp, i, st.session_state.tech_inputs) for i in range(14)]
        t_revs.append(sum(r["total_rev"] for r in res)/1e6)
        m_revs.append(sum(r["mbm_total"] for r in res)/1e6)
        n_cfs.append(sum(r["net_cf"]     for r in res)/1e6)

    fig_s = make_subplots(rows=1, cols=2,
        subplot_titles=["Total Revenue & Net Cash Flow","MBM Revenue Contribution"],
        horizontal_spacing=0.12)
    fig_s.add_trace(go.Scatter(x=ets_range, y=t_revs, name="Total Revenue",
        line=dict(color="#1b4f72", width=2)), row=1, col=1)
    fig_s.add_trace(go.Scatter(x=ets_range, y=n_cfs, name="Net Cash Flow",
        line=dict(color="#c0392b", width=1.5, dash="dash")), row=1, col=1)
    fig_s.add_trace(go.Scatter(x=ets_range, y=m_revs, name="MBM Revenue",
        fill="tozeroy", fillcolor="rgba(27,79,114,0.1)",
        line=dict(color="#1b4f72", width=1.5)), row=1, col=2)
    for col in [1,2]:
        fig_s.add_vline(x=base["ets"], line_color="#b7860b", line_dash="dot", line_width=1, row=1, col=col)
    fig_s.update_layout(**PLOT_LAYOUT, height=360, showlegend=True,
        legend=dict(orientation="h", y=-0.22, x=0,
            bgcolor="rgba(250,248,244,0.9)", bordercolor="#d4c9b0", borderwidth=1,
            font=dict(size=10, family="Source Serif 4, serif")))
    fig_s.update_xaxes(title_text="ETS Price (USD/tCO₂e)",
        tickfont=dict(size=9, family="JetBrains Mono, monospace"),
        showgrid=True, gridcolor="#e8e4dc")
    fig_s.update_yaxes(title_text="USD Million",
        tickfont=dict(size=9, family="JetBrains Mono, monospace"),
        showgrid=True, gridcolor="#e8e4dc")
    st.plotly_chart(fig_s, use_container_width=True)
    st.markdown('<div class="fig-caption"><span class="fig-label">Figure 6.</span> Sensitivity of portfolio revenues to ETS carbon price. Dashed gold line indicates current parameter value.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">§9. Discrete Scenario Comparison</div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        lo_ets = st.slider("ETS — Conservative Scenario (USD/tCO₂e)", 10, 150, 40, 5)
        hi_ets = st.slider("ETS — Optimistic Scenario (USD/tCO₂e)", 100, 500, 200, 10)
    with sc2:
        lo_vcm = st.slider("VCM — Conservative Scenario (USD/tCO₂e)", 5, 100, 25, 5)
        hi_vcm = st.slider("VCM — Optimistic Scenario (USD/tCO₂e)", 50, 500, 180, 5)

    scenarios = {
        "Conservative": {**base,"ets":lo_ets,"vcm":lo_vcm},
        "Base Case":    {**base},
        "Optimistic":   {**base,"ets":hi_ets,"vcm":hi_vcm},
    }
    sc_results = {}
    for sn, sp in scenarios.items():
        res = [compute_revenues(sp, i, st.session_state.tech_inputs) for i in range(14)]
        sc_results[sn] = {
            "total_rev":sum(r["total_rev"] for r in res),
            "mbm_total":sum(r["mbm_total"] for r in res),
            "net_cf":   sum(r["net_cf"]    for r in res),
        }

    cols = st.columns(3)
    labels_s = ["Conservative","Base Case","Optimistic"]
    colors_s  = ["#6b6b8a","#1b4f72","#1d6a3e"]
    for col, sn, clr in zip(cols, labels_s, colors_s):
        v = sc_results[sn]
        with col:
            st.markdown(f"""
            <div style="border:1px solid var(--rule);padding:1.2rem;background:var(--paper-2)">
                <div class="journal-meta" style="color:{clr}">{sn}</div>
                <div style="margin:0.6rem 0">
                    <div class="kpi-label">Total Revenue</div>
                    <div class="kpi-value" style="font-size:1.25rem">{fmt_m(v["total_rev"])}</div>
                </div>
                <div style="margin:0.4rem 0">
                    <div class="kpi-label">MBM Revenue</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.92rem">{fmt_m(v["mbm_total"])}</div>
                </div>
                <div>
                    <div class="kpi-label">Net Cash Flow</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.92rem;color:{'#1d6a3e' if v['net_cf']>=0 else '#c0392b'}">{fmt_m(v["net_cf"])}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    fig_sc = go.Figure()
    for key, lbl, clr in [("total_rev","Total Revenue","#1b4f72"),("mbm_total","MBM Revenue","#b7860b"),("net_cf","Net Cash Flow","#1d6a3e")]:
        fig_sc.add_trace(go.Bar(name=lbl, x=list(sc_results.keys()),
            y=[sc_results[s][key]/1e6 for s in sc_results],
            marker_color=clr, marker_line_width=0))
    fig_sc.update_layout(**PLOT_LAYOUT, barmode="group", height=300, yaxis_title="USD Million")
    st.plotly_chart(fig_sc, use_container_width=True)
    st.markdown('<div class="fig-caption"><span class="fig-label">Figure 7.</span> Discrete scenario comparison across three carbon price regimes. All non-ETS/VCM parameters held at base case values.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TAB IV
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">§10. Portfolio Revenue Summary</div>', unsafe_allow_html=True)
    all_r2 = [compute_revenues(st.session_state.prices, i, st.session_state.tech_inputs) for i in range(14)]

    rows = []
    for i, r in enumerate(all_r2):
        rows.append({
            "Technology":         TECHNOLOGIES[i],
            "Direct Rev. ($M)":   round(r["direct_rev"]/1e6, 2),
            "MBM Rev. ($M)":      round(r["mbm_total"]/1e6, 2),
            "Total Rev. ($M)":    round(r["total_rev"]/1e6, 2),
            "Total Cost ($M)":    round(r["total_cost"]/1e6, 2),
            "Net CF ($M)":        round(r["net_cf"]/1e6, 2),
            "R/C Ratio":          round(r["rev_cost_ratio"], 2),
            "CO₂ Abated (kt/yr)": round(r["co2_abated"]/1e3, 1),
            "Lifetime Rev. ($M)": round(r["lifetime_rev"]/1e6, 1),
        })

    df = pd.DataFrame(rows)
    def style_netcf(val):
        if isinstance(val, (int,float)):
            if val>0:  return "color: #1d6a3e; font-weight: 500"
            elif val<0: return "color: #c0392b; font-weight: 500"
        return ""

    styled = df.style.map(style_netcf, subset=["Net CF ($M)"])
    st.dataframe(styled, use_container_width=True, height=500)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("↓  Export as CSV", csv, "mbm_revenue_results.csv", "text/csv")

    st.markdown('<div class="section-title">§11. MBM Mechanism Breakdown</div>', unsafe_allow_html=True)
    mbm_rows = []
    for i, r in enumerate(all_r2):
        row = {"Technology": TECH_SHORT[i]}
        for mech, val in r["mbm_breakdown"].items():
            row[f"{mech} ($M)"] = round(val/1e6, 2)
        row["Total MBM ($M)"] = round(r["mbm_total"]/1e6, 2)
        mbm_rows.append(row)

    df_mbm = pd.DataFrame(mbm_rows)
    st.dataframe(df_mbm, use_container_width=True, height=500)
    csv2 = df_mbm.to_csv(index=False).encode("utf-8")
    st.download_button("↓  Export MBM Breakdown as CSV", csv2, "mbm_mechanism_breakdown.csv", "text/csv")

    st.markdown("""
    <div class="footnote">
    Table 1 reports annual revenue, cost, and cash flow figures in USD millions. Revenue/Cost (R/C) Ratio indicates financial viability relative to total operating and capital expenditure.
    Table 2 disaggregates market-based mechanism revenue by instrument type; zero values indicate inapplicable mechanisms for the given technology category.
    All values are computed under current sidebar parameter assumptions and update dynamically upon parameter adjustment.
    </div>
    """, unsafe_allow_html=True)
