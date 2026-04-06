import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Technology Innovation Revenue Model",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# BLUE MONOCHROME DESIGN SYSTEM
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg:         #020b18;
    --surface:    #041526;
    --surface2:   #071e35;
    --surface3:   #0a2744;
    --border:     rgba(56,147,255,0.15);
    --border2:    rgba(56,147,255,0.30);
    --text:       #e8f4ff;
    --text-muted: #7baed4;
    --text-faint: #3d6a9e;
    --blue-50:    #ebf5ff;
    --blue-100:   #c3deff;
    --blue-200:   #90c2ff;
    --blue-300:   #5ca5ff;
    --blue-400:   #3893ff;
    --blue-500:   #1a78f5;
    --blue-600:   #1260d4;
    --blue-700:   #0d4cac;
    --blue-800:   #083780;
    --blue-900:   #041e50;
    --glow:       0 0 40px rgba(56,147,255,0.12);
    --glow-sm:    0 0 16px rgba(56,147,255,0.20);
    --radius:     12px;
    --radius-lg:  18px;
}

/* === BASE === */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.main, .block-container {
    background: var(--bg) !important;
    color: var(--text) !important;
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* === SIDEBAR === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--surface) 0%, var(--bg) 100%) !important;
    border-right: 1px solid var(--border2) !important;
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] p {
    color: var(--text) !important;
}
[data-testid="stSidebar"] .stSlider [data-testid="stSliderThumb"] {
    background: var(--blue-400) !important;
}

/* === HERO BANNER === */
.hero-banner {
    background: linear-gradient(135deg, #020b18 0%, #041e50 40%, #0a2744 70%, #020b18 100%);
    border: 1px solid var(--border2);
    border-radius: var(--radius-lg);
    padding: 40px 48px;
    margin-bottom: 8px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(56,147,255,0.14) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute; bottom: -80px; left: 30%;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(26,120,245,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem; font-weight: 700;
    color: var(--blue-50);
    margin: 0 0 6px 0; line-height: 1.2;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-size: 0.92rem; color: var(--blue-200);
    font-weight: 400; letter-spacing: 0.02em;
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: rgba(56,147,255,0.15);
    border: 1px solid rgba(56,147,255,0.35);
    color: var(--blue-300);
    font-size: 0.72rem; font-weight: 600;
    padding: 4px 12px; border-radius: 20px;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 14px;
}

/* === SLIDE NAV === */
.slide-nav {
    display: flex; gap: 6px;
    padding: 8px; margin-bottom: 0;
    border-bottom: 1px solid var(--border);
}
.slide-nav-btn {
    background: none; border: none;
    color: var(--text-muted); font-size: 0.82rem;
    padding: 8px 18px; border-radius: 8px;
    cursor: pointer; font-family: 'Inter', sans-serif;
    font-weight: 500; transition: all 0.2s;
    white-space: nowrap;
}
.slide-nav-btn:hover { background: var(--surface2); color: var(--blue-300); }
.slide-nav-btn.active {
    background: rgba(56,147,255,0.12);
    color: var(--blue-300);
    border: 1px solid rgba(56,147,255,0.25);
}

/* === SLIDE WRAPPER === */
.slide {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 32px 36px;
    margin-top: 8px;
    min-height: 70vh;
}
.slide-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.35rem; font-weight: 700;
    color: var(--blue-100); margin: 0 0 4px 0;
}
.slide-sub {
    font-size: 0.82rem; color: var(--text-muted);
    margin-bottom: 24px;
}

/* === KPI CARDS === */
.kpi-row { display: flex; gap: 14px; margin-bottom: 24px; flex-wrap: wrap; }
.kpi-card {
    flex: 1; min-width: 160px;
    background: linear-gradient(135deg, var(--surface2), var(--surface3));
    border: 1px solid var(--border2);
    border-radius: var(--radius);
    padding: 18px 20px;
    position: relative; overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute; top: 0; right: 0;
    width: 60px; height: 60px;
    background: radial-gradient(circle, rgba(56,147,255,0.10) 0%, transparent 70%);
}
.kpi-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.7rem; font-weight: 700;
    color: var(--blue-200); line-height: 1;
    margin-bottom: 4px;
}
.kpi-label {
    font-size: 0.72rem; color: var(--text-muted);
    font-weight: 500; text-transform: uppercase;
    letter-spacing: 0.06em;
}
.kpi-delta {
    font-size: 0.75rem; color: var(--blue-400);
    margin-top: 6px; font-weight: 500;
}

/* === SECTION LABEL === */
.section-label {
    font-size: 0.7rem; font-weight: 700;
    color: var(--blue-400); text-transform: uppercase;
    letter-spacing: 0.1em; margin: 20px 0 10px 0;
    display: flex; align-items: center; gap: 8px;
}
.section-label::after {
    content: ''; flex: 1;
    height: 1px; background: var(--border);
}

/* === DATA TABLE === */
.stDataFrame { background: var(--surface2) !important; border-radius: var(--radius) !important; }
.stDataFrame table { color: var(--text) !important; }
[data-testid="stDataFrameResizable"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden;
}

/* === STREAMLIT METRICS OVERRIDE === */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--surface2), var(--surface3));
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 14px 18px !important;
}
[data-testid="stMetricValue"] { color: var(--blue-200) !important; font-size: 1.4rem !important; }
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; }
[data-testid="stMetricDelta"] { color: var(--blue-400) !important; }

/* === TABS (now used as mini-nav inside slides) === */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface2) !important;
    border-radius: 10px !important; gap: 4px;
    border-bottom: none !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    padding: 6px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(56,147,255,0.18) !important;
    color: var(--blue-300) !important;
    font-weight: 600 !important;
}

/* === SELECT/INPUT === */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* === BUTTONS === */
.stButton > button {
    background: linear-gradient(135deg, var(--blue-700), var(--blue-600)) !important;
    color: var(--blue-50) !important;
    border: 1px solid var(--blue-500) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--blue-600), var(--blue-500)) !important;
    box-shadow: var(--glow-sm) !important;
}

/* === DIVIDER === */
hr { border-color: var(--border) !important; margin: 16px 0 !important; }

/* === SIDEBAR CONTROLS === */
.sidebar-section {
    font-size: 0.7rem; font-weight: 700;
    color: var(--blue-400); text-transform: uppercase;
    letter-spacing: 0.1em; padding: 12px 0 6px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 10px;
}
.stSlider [data-testid="stSliderThumbValue"],
.stSlider .st-emotion-cache-1inwz65 {
    color: var(--blue-300) !important;
}

/* === SCROLL FIX === */
section[data-testid="stSidebar"] > div { overflow-y: auto; }

/* === PROGRESS BAR === */
.prog-bar-bg {
    background: var(--surface3);
    border-radius: 20px; height: 8px;
    margin: 6px 0;
}
.prog-bar-fill {
    height: 8px; border-radius: 20px;
    background: linear-gradient(90deg, var(--blue-700), var(--blue-400));
    transition: width 0.6s ease;
}
.prog-row {
    display: flex; justify-content: space-between;
    font-size: 0.75rem; color: var(--text-muted);
    margin-bottom: 2px; margin-top: 12px;
}
.prog-row span:last-child { color: var(--blue-300); font-weight: 600; }

/* === MECHANISM CHIP === */
.mech-chip {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 5px 12px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600;
    margin: 3px;
}
.mech-chip.active {
    background: rgba(56,147,255,0.15);
    border: 1px solid rgba(56,147,255,0.35);
    color: var(--blue-300);
}
.mech-chip.inactive {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    color: var(--text-faint);
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
TECHNOLOGIES = [
    "Solar PV & Wind Energy", "Green Hydrogen", "SAF (Sust. Aviation Fuel)", "CCUS",
    "Battery Storage & EVs", "Low-carbon Steel & Cement", "Ammonia (green/blue)",
    "Methanol (green/e-methanol)", "Reforestation / REDD+ / NBS", "Blue Carbon (mangroves)",
    "Direct Air Capture (DAC)", "Building Energy Efficiency",
    "Carbon Offsetting / MRV Tech", "Energy Mgmt & Analytics",
]
TECH_SHORT = [
    "Solar/Wind", "Green H₂", "SAF", "CCUS", "Battery/EV", "Steel/Cement",
    "Ammonia", "Methanol", "Reforestation", "Blue Carbon", "DAC",
    "Bldg Eff.", "MRV Tech", "Energy Mgmt"
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
    "learning_rate":      [0.20,0.18,0.12,0.08,0.22,0.06,0.10,0.10,0.05,0.04,0.15,0.08,0.10,0.12],
    "cum_cap_now":        [2000,0.5,0.05,0.03,1500,0.1,0.02,0.01,500,10,0.001,5000,100,200],
    "cum_cap_2035":       [8000,10,0.5,0.5,5000,2,0.5,0.2,1000,50,1,8000,500,1000],
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
MBM_LABELS = {
    "ets": ("ETS / Carbon Market","USD/tCO₂e"), "ctax": ("Carbon Tax","USD/tCO₂e"),
    "fuel": ("Fuel Mandate","USD/MWh"), "cfd": ("CfD / CCfD","USD/MWh"),
    "cbam": ("CBAM Import","USD/tCO₂e"), "corsia": ("CORSIA Credit","USD/tCO₂e"),
    "imo": ("IMO Levy","USD/tCO₂e"), "vcm": ("VCM / CDM Credit","USD/tCO₂e"),
    "amc": ("AMC","USD/unit"), "feebate": ("Feebate","USD/tCO₂e"),
}
DEFAULT_PRICES = {
    "ets":100,"ctax":50,"fuel":240,"cfd_strike":120,"cfd_ref":80,
    "cbam":55,"corsia":22.25,"imo":380,"vcm":100,"amc":100,
    "feebate":50,"electricity":60,"gas":8,"biomass":40
}

# ─────────────────────────────────────────────
# BLUE MONO PLOTLY THEME
# ─────────────────────────────────────────────
PLOT_BG    = "rgba(0,0,0,0)"
FONT_COLOR = "#c8dff4"
GRID_COLOR = "rgba(56,147,255,0.08)"
BLUE_SCALE = ["#083780","#0d4cac","#1260d4","#1a78f5","#3893ff","#5ca5ff","#90c2ff","#c3deff"]
BLUE_SHADES = ["#1a78f5","#1260d4","#0d4cac","#083780","#5ca5ff","#3893ff","#90c2ff","#0a2744","#3d6a9e","#041e50"]

def plotly_base(height=380, margin=None):
    m = margin or dict(l=20,r=20,t=30,b=20)
    return dict(
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        font=dict(family="Inter", color=FONT_COLOR, size=11),
        height=height, margin=m,
        legend=dict(orientation="h", y=-0.18, font=dict(size=10)),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor="rgba(56,147,255,0.15)", tickcolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor="rgba(56,147,255,0.15)", tickcolor=GRID_COLOR),
    )

# ─────────────────────────────────────────────
# CALCULATION ENGINE
# ─────────────────────────────────────────────
def calc_crf(wacc, lifetime):
    if wacc == 0: return 1 / lifetime
    return (wacc * (1+wacc)**lifetime) / ((1+wacc)**lifetime - 1)

def compute_revenues(prices, t, tech_inputs):
    output     = tech_inputs["annual_output"][t]
    cap_kw     = tech_inputs["installed_capacity"][t] * 1000
    lifetime   = tech_inputs["project_lifetime"][t]
    wacc       = tech_inputs["wacc"][t]
    capex_kw   = tech_inputs["capex_per_kw"][t]
    opex_pct   = tech_inputs["opex_pct"][t]
    feedstock  = tech_inputs["feedstock_cost"][t]
    other_opex = tech_inputs["other_opex"][t]
    mkt_price  = tech_inputs["market_price"][t]
    co2_factor = tech_inputs["co2_abated_factor"][t]
    clients    = tech_inputs["clients"][t]
    capex_total= capex_kw * cap_kw
    crf        = calc_crf(wacc, lifetime)
    ann_capex  = capex_total * crf
    fixed_opex = capex_total * opex_pct
    total_cost = ann_capex + fixed_opex + feedstock + other_opex
    co2_abated = output * co2_factor
    direct_rev = (clients * mkt_price) if t in [12,13] else (output * mkt_price)
    ets_rev    = co2_abated * prices["ets"]    if DEFAULTS["ets"][t]    else 0
    ctax_rev   = co2_abated * prices["ctax"]   if DEFAULTS["ctax"][t]   else 0
    vcm_rev    = co2_abated * prices["vcm"]    if DEFAULTS["vcm"][t]    else 0
    fuel_rev   = (output * tech_inputs["capacity_factor"][t] * prices["fuel"] * 0.85
                  if DEFAULTS["fuel"][t] and output > 0 else 0)
    cfd_diff   = max(0, prices["cfd_strike"] - prices["cfd_ref"])
    cfd_rev    = (output * cfd_diff * 0.5 if DEFAULTS["cfd"][t] and output > 0 else 0)
    cbam_rev   = (co2_abated * prices["cbam"] * 0.85 if DEFAULTS["cbam"][t]   else 0)
    corsia_rev = (co2_abated * prices["corsia"] * 1.05 if DEFAULTS["corsia"][t] else 0)
    imo_rev    = (co2_abated * prices["imo"] * 0.95 if DEFAULTS["imo"][t]    else 0)
    amc_rev    = ((output/1000) * prices["amc"] * 0.5 if DEFAULTS["amc"][t]  else 0)
    feebate_rev= (co2_abated * prices["feebate"] * 0.5 if DEFAULTS["feebate"][t] else 0)
    mbm_total  = ets_rev+ctax_rev+fuel_rev+cfd_rev+cbam_rev+corsia_rev+imo_rev+vcm_rev+amc_rev+feebate_rev
    total_rev  = mbm_total + direct_rev
    return {
        "capex_total":capex_total,"ann_capex":ann_capex,"fixed_opex":fixed_opex,
        "total_cost":total_cost,"co2_abated":co2_abated,"direct_rev":direct_rev,
        "mbm_total":mbm_total,"total_rev":total_rev,"net_cf":total_rev-total_cost,
        "lifetime_rev":total_rev*lifetime,
        "rev_cost_ratio":total_rev/total_cost if total_cost>0 else 0,
        "mbm_breakdown":{
            "ETS":ets_rev,"Carbon Tax":ctax_rev,"Fuel Mandate":fuel_rev,"CfD":cfd_rev,
            "CBAM":cbam_rev,"CORSIA":corsia_rev,"IMO Levy":imo_rev,"VCM/CDM":vcm_rev,
            "AMC":amc_rev,"Feebate":feebate_rev
        },
    }

def fmt_m(v): return f"${v/1e6:.1f}M"

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    if "tech_inputs" not in st.session_state:
        st.session_state.tech_inputs = {k: list(v) for k,v in DEFAULTS.items()}
    if "prices" not in st.session_state:
        st.session_state.prices = dict(DEFAULT_PRICES)
    if "slide" not in st.session_state:
        st.session_state.slide = 0

init_state()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 12px 0">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.05rem;font-weight:700;color:#c3deff;letter-spacing:-0.01em">
            ⚡ MBM Price Controls
        </div>
        <div style="font-size:0.72rem;color:#3d6a9e;margin-top:3px">
            Adjust market-based mechanism parameters
        </div>
    </div>
    """, unsafe_allow_html=True)

    p = st.session_state.prices

    st.markdown('<div class="sidebar-section">Carbon Pricing</div>', unsafe_allow_html=True)
    p["ets"]     = st.slider("ETS / Carbon Market (USD/tCO₂e)", 10, 300, p["ets"], 5)
    p["ctax"]    = st.slider("Carbon Tax (USD/tCO₂e)", 0, 200, p["ctax"], 5)
    p["vcm"]     = st.slider("VCM / CDM Credit (USD/tCO₂e)", 5, 300, p["vcm"], 5)
    p["cbam"]    = st.slider("CBAM Import Cost (USD/tCO₂e)", 10, 150, p["cbam"], 5)
    p["corsia"]  = st.slider("CORSIA Credit (USD/tCO₂e)", 3, 100, int(p["corsia"]), 1)
    p["imo"]     = st.slider("IMO Levy (USD/tCO₂e)", 50, 800, p["imo"], 10)
    p["feebate"] = st.slider("Feebate Rate (USD/tCO₂e)", 0, 150, p["feebate"], 5)

    st.markdown('<div class="sidebar-section">Energy & Policy</div>', unsafe_allow_html=True)
    p["cfd_strike"] = st.slider("CfD Strike Price (USD/MWh)", 50, 300, p["cfd_strike"], 5)
    p["cfd_ref"]    = st.slider("CfD Market Reference (USD/MWh)", 30, 200, p["cfd_ref"], 5)
    p["fuel"]       = st.slider("Fuel Mandate Offtake (USD/MWh)", 100, 600, p["fuel"], 10)
    p["amc"]        = st.slider("AMC Price (USD/unit)", 50, 300, p["amc"], 10)

    st.markdown('<div class="sidebar-section">Commodity Prices</div>', unsafe_allow_html=True)
    p["electricity"] = st.slider("Grid Electricity (USD/MWh)", 20, 200, p["electricity"], 5)
    p["gas"]         = st.slider("Natural Gas (USD/MMBtu)", 2, 30, p["gas"], 1)
    p["biomass"]     = st.slider("Biomass / Feedstock (USD/MWh)", 10, 120, p["biomass"], 5)

    st.session_state.prices = p
    st.markdown("---")
    if st.button("↺  Reset All Defaults", use_container_width=True):
        st.session_state.prices = dict(DEFAULT_PRICES)
        st.session_state.tech_inputs = {k: list(v) for k,v in DEFAULTS.items()}
        st.rerun()

# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">Carbon Market Intelligence</div>
    <h1 class="hero-title">Technology Innovation Revenue Model</h1>
    <p class="hero-sub">Market-Based Mechanism (MBM) Intervention — Multi-Technology Revenue Estimation & Scenario Analysis</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE NAVIGATION (in-page)
# ─────────────────────────────────────────────
SLIDES = ["📊  Portfolio Overview", "🔬  Technology Detail", "📈  Scenario Analysis", "📋  Data Table", "⚙️  MBM Price Controls"]

col_nav = st.columns(len(SLIDES))
for i, label in enumerate(SLIDES):
    with col_nav[i]:
        if st.button(label, key=f"nav_{i}", use_container_width=True,
                     type="primary" if st.session_state.slide == i else "secondary"):
            st.session_state.slide = i
            st.rerun()

st.markdown("---")
slide = st.session_state.slide

# ─────────────────────────────────────────────
# PRE-COMPUTE ALL RESULTS
# ─────────────────────────────────────────────
all_results = [compute_revenues(st.session_state.prices, i, st.session_state.tech_inputs) for i in range(14)]
total_rev   = sum(r["total_rev"]  for r in all_results)
total_mbm   = sum(r["mbm_total"]  for r in all_results)
total_direct= sum(r["direct_rev"] for r in all_results)
total_cost  = sum(r["total_cost"] for r in all_results)
total_netcf = sum(r["net_cf"]     for r in all_results)
total_co2   = sum(r["co2_abated"] for r in all_results)

# ═══════════════════════════════════════════
# SLIDE 0 — PORTFOLIO OVERVIEW
# ═══════════════════════════════════════════
if slide == 0:
    st.markdown("""
    <div class="slide-header">Portfolio Overview</div>
    <div class="slide-sub">Annual revenue performance across all 14 clean technology verticals</div>
    """, unsafe_allow_html=True)

    # KPI row via columns + custom HTML
    k1,k2,k3,k4,k5 = st.columns(5)
    kpis = [
        (k1, "Total Annual Revenue", fmt_m(total_rev), "Portfolio-wide"),
        (k2, "MBM Revenue", fmt_m(total_mbm), f"{total_mbm/total_rev*100:.1f}% of total"),
        (k3, "Direct Revenue", fmt_m(total_direct), f"{total_direct/total_rev*100:.1f}% of total"),
        (k4, "Net Cash Flow", fmt_m(total_netcf), f"R/C {total_rev/total_cost:.2f}×"),
        (k5, "CO₂ Abated", f"{total_co2/1e6:.2f}M tCO₂e", "per year"),
    ]
    for col, label, val, sub in kpis:
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-delta">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    c_left, c_right = st.columns([3, 2])

    with c_left:
        st.markdown('<div class="section-label">Revenue by Technology</div>', unsafe_allow_html=True)
        techs_sorted = sorted(range(14), key=lambda i: all_results[i]["total_rev"], reverse=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="MBM Revenue",
            x=[TECH_SHORT[i] for i in techs_sorted],
            y=[all_results[i]["mbm_total"]/1e6 for i in techs_sorted],
            marker=dict(color="#1a78f5", opacity=0.9),
        ))
        fig.add_trace(go.Bar(
            name="Direct Revenue",
            x=[TECH_SHORT[i] for i in techs_sorted],
            y=[all_results[i]["direct_rev"]/1e6 for i in techs_sorted],
            marker=dict(color="#5ca5ff", opacity=0.9),
        ))
        fig.add_trace(go.Bar(
            name="Total Cost",
            x=[TECH_SHORT[i] for i in techs_sorted],
            y=[-all_results[i]["total_cost"]/1e6 for i in techs_sorted],
            marker=dict(color="#083780", opacity=0.85),
        ))
        fig.update_layout(**plotly_base(400))
        fig.update_layout(barmode="relative", xaxis=dict(tickangle=-35))
        fig.update_yaxes(title_text="USD Million")
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        st.markdown('<div class="section-label">MBM Revenue Mix</div>', unsafe_allow_html=True)
        mbm_agg = {}
        for r in all_results:
            for k, v in r["mbm_breakdown"].items():
                mbm_agg[k] = mbm_agg.get(k,0) + v
        mbm_f = {k: v for k,v in mbm_agg.items() if v > 0}
        fig2 = go.Figure(go.Pie(
            labels=list(mbm_f.keys()),
            values=list(mbm_f.values()),
            hole=0.5,
            textinfo="label+percent",
            marker=dict(colors=BLUE_SHADES[:len(mbm_f)]),
            textfont=dict(size=10, color="#c8dff4"),
        ))
        fig2.update_layout(**plotly_base(400))
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-label">Net Annual Cash Flow by Technology</div>', unsafe_allow_html=True)
    colors_cf = ["#3893ff" if all_results[i]["net_cf"] >= 0 else "#0d4cac" for i in range(14)]
    fig3 = go.Figure(go.Bar(
        x=TECH_SHORT,
        y=[all_results[i]["net_cf"]/1e6 for i in range(14)],
        marker_color=colors_cf,
        text=[f"${all_results[i]['net_cf']/1e6:.1f}M" for i in range(14)],
        textposition="outside", textfont=dict(color="#90c2ff", size=10),
    ))
    fig3.update_layout(**plotly_base(300))
    fig3.update_layout(xaxis=dict(tickangle=-35))
    fig3.update_yaxes(title_text="USD Million")
    st.plotly_chart(fig3, use_container_width=True)

    # Technology Revenue Ranking (progress bars)
    st.markdown('<div class="section-label">Technology Revenue Ranking</div>', unsafe_allow_html=True)
    max_rev = max(r["total_rev"] for r in all_results)
    sorted_idx = sorted(range(14), key=lambda i: all_results[i]["total_rev"], reverse=True)
    cols_rank = st.columns(2)
    for rank, i in enumerate(sorted_idx):
        pct = all_results[i]["total_rev"] / max_rev * 100
        with cols_rank[rank % 2]:
            st.markdown(f"""
            <div class="prog-row">
                <span>{TECH_SHORT[i]}</span>
                <span>{fmt_m(all_results[i]["total_rev"])}</span>
            </div>
            <div class="prog-bar-bg">
                <div class="prog-bar-fill" style="width:{pct:.1f}%"></div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════
# SLIDE 1 — TECHNOLOGY DETAIL
# ═══════════════════════════════════════════
elif slide == 1:
    st.markdown("""
    <div class="slide-header">Technology Detail</div>
    <div class="slide-sub">Configure individual technology parameters and view granular revenue breakdown</div>
    """, unsafe_allow_html=True)

    selected = st.selectbox("Select Technology", TECHNOLOGIES, index=0)
    t  = TECHNOLOGIES.index(selected)
    ti = st.session_state.tech_inputs

    st.markdown('<div class="section-label">Technology-Specific Inputs</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Scale & Output**")
        ti["annual_output"][t]       = st.number_input("Annual Output (MWh or t/yr)", 0, 10_000_000, int(ti["annual_output"][t]), 10000, key=f"ao_{t}")
        ti["installed_capacity"][t]  = st.number_input("Installed Capacity (MW)", 0, 5000, int(ti["installed_capacity"][t]), 10, key=f"ic_{t}")
        ti["capacity_factor"][t]     = st.slider("Capacity Factor", 0.0, 1.0, ti["capacity_factor"][t], 0.01, key=f"cf_{t}")
        ti["project_lifetime"][t]    = st.slider("Project Lifetime (yrs)", 5, 50, int(ti["project_lifetime"][t]), 1, key=f"pl_{t}")

    with col2:
        st.markdown("**Cost Structure**")
        ti["capex_per_kw"][t]  = st.number_input("CAPEX/kW (USD/kW)", 0, 20000, int(ti["capex_per_kw"][t]), 100, key=f"ck_{t}")
        ti["opex_pct"][t]      = st.slider("OPEX (% of CAPEX p.a.)", 0.0, 0.20, ti["opex_pct"][t], 0.005, format="%.3f", key=f"op_{t}")
        ti["feedstock_cost"][t]= st.number_input("Feedstock Cost (USD/yr)", 0, 50_000_000, int(ti["feedstock_cost"][t]), 100000, key=f"fc_{t}")
        ti["other_opex"][t]    = st.number_input("Other Variable OPEX (USD/yr)", 0, 20_000_000, int(ti["other_opex"][t]), 100000, key=f"ov_{t}")
        ti["wacc"][t]          = st.slider("WACC / Discount Rate", 0.01, 0.25, ti["wacc"][t], 0.005, format="%.3f", key=f"wc_{t}")

    with col3:
        st.markdown("**Revenue Drivers**")
        ti["market_price"][t]      = st.number_input("Market Price (USD/MWh or USD/t)", 0, 100000, int(ti["market_price"][t]), 10, key=f"mp_{t}")
        ti["co2_abated_factor"][t] = st.slider("CO₂ Abated/Unit (tCO₂e/unit)", 0.0, 2.0, ti["co2_abated_factor"][t], 0.01, key=f"ca_{t}")
        if t in [12, 13]:
            ti["clients"][t] = st.number_input("Number of Clients", 0, 10000, int(ti["clients"][t]), 1, key=f"cl_{t}")

    r = compute_revenues(st.session_state.prices, t, ti)
    st.markdown('<div class="section-label">Revenue Estimation Results</div>', unsafe_allow_html=True)

    mc1,mc2,mc3,mc4,mc5 = st.columns(5)
    for col, val, label, sub in [
        (mc1, fmt_m(r["total_rev"]),  "Total Annual Revenue", ""),
        (mc2, fmt_m(r["mbm_total"]),  "MBM Revenue",          f"{r['mbm_total']/r['total_rev']*100:.0f}% of total" if r["total_rev"]>0 else ""),
        (mc3, fmt_m(r["direct_rev"]), "Direct Revenue",       ""),
        (mc4, fmt_m(r["total_cost"]), "Total Annual Cost",    ""),
        (mc5, fmt_m(r["net_cf"]),     "Net Cash Flow",        f"R/C {r['rev_cost_ratio']:.2f}×"),
    ]:
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-delta">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-label">MBM Revenue Breakdown</div>', unsafe_allow_html=True)
        mbm_data = {k:v for k,v in r["mbm_breakdown"].items() if v>0}
        if mbm_data:
            sorted_mbm = sorted(mbm_data.items(), key=lambda x: x[1], reverse=True)
            fig_mbm = go.Figure(go.Bar(
                x=[x[0] for x in sorted_mbm],
                y=[x[1]/1e6 for x in sorted_mbm],
                marker=dict(
                    color=list(range(len(sorted_mbm))),
                    colorscale=[[0,"#083780"],[0.5,"#1a78f5"],[1,"#90c2ff"]],
                ),
                text=[f"${x[1]/1e6:.2f}M" for x in sorted_mbm],
                textposition="outside", textfont=dict(color="#90c2ff",size=10),
            ))
            fig_mbm.update_layout(**plotly_base(330))
            fig_mbm.update_yaxes(title_text="USD Million")
            st.plotly_chart(fig_mbm, use_container_width=True)
        else:
            st.info("No active MBM mechanisms for this technology.")

    with col_b:
        st.markdown('<div class="section-label">Cost vs Revenue Structure</div>', unsafe_allow_html=True)
        cats   = ["Direct Rev", "MBM Rev", "CAPEX (ann.)", "Fixed OPEX", "Feedstock", "Other OPEX"]
        vals   = [r["direct_rev"]/1e6, r["mbm_total"]/1e6,
                  -r["ann_capex"]/1e6, -r["fixed_opex"]/1e6,
                  -ti["feedstock_cost"][t]/1e6, -ti["other_opex"][t]/1e6]
        c_wf   = ["#3893ff" if v>=0 else "#0d4cac" for v in vals]
        fig_wf = go.Figure(go.Bar(
            x=cats, y=vals, marker_color=c_wf,
            text=[f"${abs(v):.2f}M" for v in vals],
            textposition="outside", textfont=dict(color="#90c2ff",size=10),
        ))
        fig_wf.add_hline(y=0, line_color="rgba(56,147,255,0.4)", line_width=1)
        fig_wf.update_layout(**plotly_base(330))
        fig_wf.update_layout(xaxis=dict(tickangle=-30))
        fig_wf.update_yaxes(title_text="USD Million")
        st.plotly_chart(fig_wf, use_container_width=True)

    st.markdown('<div class="section-label">Active MBM Mechanisms</div>', unsafe_allow_html=True)
    mechs = ["ets","ctax","fuel","cfd","cbam","corsia","imo","vcm","amc","feebate"]
    chips_html = ""
    for m in mechs:
        applicable = DEFAULTS[m][t]
        label, unit = MBM_LABELS[m]
        price_val = st.session_state.prices.get(m, st.session_state.prices.get("cfd_strike","—"))
        icon = "✓" if applicable else "✕"
        cls = "active" if applicable else "inactive"
        chips_html += f'<span class="mech-chip {cls}">{icon} {label}</span>'
    st.markdown(chips_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════
# SLIDE 2 — SCENARIO ANALYSIS
# ═══════════════════════════════════════════
elif slide == 2:
    st.markdown("""
    <div class="slide-header">Scenario Analysis</div>
    <div class="slide-sub">Stress-test portfolio revenue under varying carbon price assumptions</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Carbon Price Sensitivity — ETS</div>', unsafe_allow_html=True)
    base_prices = dict(st.session_state.prices)
    ets_range = list(range(10, 310, 10))
    total_revs, mbm_revs, net_cfs = [], [], []
    for ets_p in ets_range:
        test_p = dict(base_prices); test_p["ets"] = ets_p
        res = [compute_revenues(test_p, i, st.session_state.tech_inputs) for i in range(14)]
        total_revs.append(sum(r["total_rev"] for r in res)/1e6)
        mbm_revs.append(sum(r["mbm_total"]  for r in res)/1e6)
        net_cfs.append(sum(r["net_cf"]      for r in res)/1e6)

    fig_sens = make_subplots(rows=1, cols=2,
        subplot_titles=("Total Revenue & Net CF vs ETS Price", "MBM Revenue vs ETS Price"))
    fig_sens.add_trace(go.Scatter(x=ets_range, y=total_revs, name="Total Revenue",
        line=dict(color="#3893ff", width=2.5)), row=1, col=1)
    fig_sens.add_trace(go.Scatter(x=ets_range, y=net_cfs, name="Net Cash Flow",
        line=dict(color="#90c2ff", width=2, dash="dot")), row=1, col=1)
    fig_sens.add_trace(go.Scatter(x=ets_range, y=mbm_revs, name="MBM Revenue",
        fill="tozeroy", fillcolor="rgba(26,120,245,0.12)",
        line=dict(color="#5ca5ff", width=2)), row=1, col=2)
    for col_i in [1, 2]:
        fig_sens.add_vline(x=base_prices["ets"], line_color="rgba(195,222,255,0.4)",
                           line_dash="dash", row=1, col=col_i)
    fig_sens.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        font=dict(family="Inter", color=FONT_COLOR, size=11), height=380,
        margin=dict(l=20,r=20,t=40,b=20),
        legend=dict(orientation="h", y=-0.15, font=dict(size=10)),
    )
    for ax in ["xaxis","xaxis2"]:
        fig_sens.update_layout(**{ax: dict(gridcolor=GRID_COLOR, title="ETS Price (USD/tCO₂e)")})
    for ax in ["yaxis","yaxis2"]:
        fig_sens.update_layout(**{ax: dict(gridcolor=GRID_COLOR, title="USD Million")})
    st.plotly_chart(fig_sens, use_container_width=True)

    st.markdown('<div class="section-label">Multi-Scenario Comparison</div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        sc_ets_low  = st.slider("ETS Low (USD/tCO₂e)",  10, 200, 50,  10)
        sc_ets_base = st.slider("ETS Base (USD/tCO₂e)", 10, 300, base_prices["ets"], 10)
        sc_ets_high = st.slider("ETS High (USD/tCO₂e)", 50, 500, 200, 10)
    with sc2:
        sc_vcm_low  = st.slider("VCM Low (USD/tCO₂e)",  5, 100, 30, 5)
        sc_vcm_base = st.slider("VCM Base (USD/tCO₂e)", 5, 300, base_prices["vcm"], 5)
        sc_vcm_high = st.slider("VCM High (USD/tCO₂e)", 50, 500, 200, 5)

    scenarios = {
        "🔵 Low":  {**base_prices, "ets": sc_ets_low,  "vcm": sc_vcm_low},
        "⚪ Base": {**base_prices, "ets": sc_ets_base, "vcm": sc_vcm_base},
        "🔷 High": {**base_prices, "ets": sc_ets_high, "vcm": sc_vcm_high},
    }
    sc_res = {}
    for sn, sp in scenarios.items():
        res = [compute_revenues(sp, i, st.session_state.tech_inputs) for i in range(14)]
        sc_res[sn] = {
            "total_rev": sum(r["total_rev"] for r in res),
            "mbm_total": sum(r["mbm_total"] for r in res),
            "net_cf":    sum(r["net_cf"]    for r in res),
        }

    # Scenario KPIs
    kc1, kc2, kc3 = st.columns(3)
    for col, sn in zip([kc1,kc2,kc3], sc_res):
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{fmt_m(sc_res[sn]["total_rev"])}</div>
            <div class="kpi-label">{sn.split()[-1]} Scenario Total Revenue</div>
            <div class="kpi-delta">Net CF: {fmt_m(sc_res[sn]["net_cf"])}  |  MBM: {fmt_m(sc_res[sn]["mbm_total"])}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    metrics = ["total_rev","mbm_total","net_cf"]
    labels  = ["Total Revenue","MBM Revenue","Net Cash Flow"]
    colors  = ["#1a78f5","#3893ff","#5ca5ff"]
    fig_sc  = go.Figure()
    for m, lbl, clr in zip(metrics, labels, colors):
        fig_sc.add_trace(go.Bar(
            name=lbl, x=list(sc_res.keys()),
            y=[sc_res[s][m]/1e6 for s in sc_res],
            marker=dict(color=clr, opacity=0.9),
        ))
    fig_sc.update_layout(**plotly_base(340))
    fig_sc.update_layout(barmode="group")
    fig_sc.update_yaxes(title_text="USD Million")
    st.plotly_chart(fig_sc, use_container_width=True)

# ═══════════════════════════════════════════
# SLIDE 3 — DATA TABLE
# ═══════════════════════════════════════════
elif slide == 3:
    st.markdown("""
    <div class="slide-header">Data Table</div>
    <div class="slide-sub">Full revenue summary and MBM breakdown across all technologies</div>
    """, unsafe_allow_html=True)

    t1, t2 = st.tabs(["Revenue Summary", "MBM Breakdown"])

    with t1:
        table_data = []
        for i, r in enumerate(all_results):
            table_data.append({
                "Technology":         TECHNOLOGIES[i],
                "Direct Rev ($M)":    round(r["direct_rev"]/1e6, 2),
                "MBM Rev ($M)":       round(r["mbm_total"]/1e6, 2),
                "Total Rev ($M)":     round(r["total_rev"]/1e6, 2),
                "Total Cost ($M)":    round(r["total_cost"]/1e6, 2),
                "Net CF ($M)":        round(r["net_cf"]/1e6, 2),
                "R/C Ratio":          round(r["rev_cost_ratio"], 2),
                "CO₂ Abated (Mt/yr)": round(r["co2_abated"]/1e6, 3),
                "Lifetime Rev ($M)":  round(r["lifetime_rev"]/1e6, 1),
            })
        df = pd.DataFrame(table_data)
        st.dataframe(df.style.background_gradient(
            subset=["Total Rev ($M)","Net CF ($M)"],
            cmap="Blues"
        ), use_container_width=True, height=500)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download CSV", csv, "revenue_model_results.csv", "text/csv")

    with t2:
        mbm_rows = []
        for i, r in enumerate(all_results):
            row = {"Technology": TECH_SHORT[i]}
            for mech, val in r["mbm_breakdown"].items():
                row[f"{mech} ($M)"] = round(val/1e6, 2)
            row["Total MBM ($M)"] = round(r["mbm_total"]/1e6, 2)
            mbm_rows.append(row)
        df_mbm = pd.DataFrame(mbm_rows)
        st.dataframe(df_mbm.style.background_gradient(
            subset=["Total MBM ($M)"], cmap="Blues"
        ), use_container_width=True, height=500)
        csv2 = df_mbm.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download MBM CSV", csv2, "mbm_breakdown.csv", "text/csv")

    # Heatmap
    st.markdown('<div class="section-label">MBM Mechanism Applicability Heatmap</div>', unsafe_allow_html=True)
    mechs = ["ets","ctax","fuel","cfd","cbam","corsia","imo","vcm","amc","feebate"]
    mech_labels = [MBM_LABELS[m][0] for m in mechs]
    z = [[DEFAULTS[m][i] for m in mechs] for i in range(14)]
    fig_hm = go.Figure(go.Heatmap(
        z=z, x=mech_labels, y=TECH_SHORT,
        colorscale=[[0,"#041526"],[0.5,"#0d4cac"],[1,"#3893ff"]],
        showscale=False,
        text=[[("✓" if v else "") for v in row] for row in z],
        texttemplate="%{text}",
        textfont=dict(color="#90c2ff", size=12),
    ))
    fig_hm.update_layout(**plotly_base(500, margin=dict(l=100,r=20,t=20,b=100)))
    fig_hm.update_layout(xaxis=dict(tickangle=-40))
    st.plotly_chart(fig_hm, use_container_width=True)

# ═══════════════════════════════════════════
# SLIDE 4 — MBM PRICE CONTROLS
# ═══════════════════════════════════════════
elif slide == 4:
    st.markdown("""
    <div class="slide-header">MBM Price Controls</div>
    <div class="slide-sub">Adjust all market-based mechanism parameters — changes apply instantly across all slides</div>
    """, unsafe_allow_html=True)

    p = st.session_state.prices

    st.markdown('<div class="section-label">Carbon Pricing</div>', unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        p["ets"]    = st.slider("ETS / Carbon Market (USD/tCO₂e)", 10, 300, p["ets"], 5, key="mb_ets")
        p["ctax"]   = st.slider("Carbon Tax (USD/tCO₂e)", 0, 200, p["ctax"], 5, key="mb_ctax")
        p["corsia"] = st.slider("CORSIA Credit (USD/tCO₂e)", 3, 100, int(p["corsia"]), 1, key="mb_corsia")
    with pc2:
        p["vcm"]    = st.slider("VCM / CDM Credit (USD/tCO₂e)", 5, 300, p["vcm"], 5, key="mb_vcm")
        p["cbam"]   = st.slider("CBAM Import Cost (USD/tCO₂e)", 10, 150, p["cbam"], 5, key="mb_cbam")
        p["imo"]    = st.slider("IMO Levy (USD/tCO₂e)", 50, 800, p["imo"], 10, key="mb_imo")
    with pc3:
        p["feebate"] = st.slider("Feebate Rate (USD/tCO₂e)", 0, 150, p["feebate"], 5, key="mb_feebate")
        p["amc"]     = st.slider("AMC Price (USD/unit)", 50, 300, p["amc"], 10, key="mb_amc")

    st.markdown('<div class="section-label">Energy & Policy Prices</div>', unsafe_allow_html=True)
    pe1, pe2, pe3 = st.columns(3)
    with pe1:
        p["cfd_strike"] = st.slider("CfD Strike Price (USD/MWh)", 50, 300, p["cfd_strike"], 5, key="mb_cfd_strike")
        p["cfd_ref"]    = st.slider("CfD Market Reference (USD/MWh)", 30, 200, p["cfd_ref"], 5, key="mb_cfd_ref")
    with pe2:
        p["fuel"] = st.slider("Fuel Mandate Offtake (USD/MWh)", 100, 600, p["fuel"], 10, key="mb_fuel")

    st.markdown('<div class="section-label">Commodity Prices</div>', unsafe_allow_html=True)
    pco1, pco2, pco3 = st.columns(3)
    with pco1:
        p["electricity"] = st.slider("Grid Electricity (USD/MWh)", 20, 200, p["electricity"], 5, key="mb_elec")
    with pco2:
        p["gas"] = st.slider("Natural Gas (USD/MMBtu)", 2, 30, p["gas"], 1, key="mb_gas")
    with pco3:
        p["biomass"] = st.slider("Biomass / Feedstock (USD/MWh)", 10, 120, p["biomass"], 5, key="mb_biomass")

    st.session_state.prices = p

    st.markdown('<div class="section-label">Current Price Summary</div>', unsafe_allow_html=True)
    price_items = [
        ("ETS / Carbon Market", p["ets"], "USD/tCO₂e"),
        ("Carbon Tax", p["ctax"], "USD/tCO₂e"),
        ("VCM / CDM Credit", p["vcm"], "USD/tCO₂e"),
        ("CBAM Import", p["cbam"], "USD/tCO₂e"),
        ("CORSIA Credit", p["corsia"], "USD/tCO₂e"),
        ("IMO Levy", p["imo"], "USD/tCO₂e"),
        ("Feebate", p["feebate"], "USD/tCO₂e"),
        ("CfD Strike", p["cfd_strike"], "USD/MWh"),
        ("CfD Reference", p["cfd_ref"], "USD/MWh"),
        ("Fuel Mandate", p["fuel"], "USD/MWh"),
        ("AMC", p["amc"], "USD/unit"),
        ("Grid Electricity", p["electricity"], "USD/MWh"),
        ("Natural Gas", p["gas"], "USD/MMBtu"),
        ("Biomass/Feedstock", p["biomass"], "USD/MWh"),
    ]
    cols_ps = st.columns(4)
    for idx, (label, val, unit) in enumerate(price_items):
        with cols_ps[idx % 4]:
            st.markdown(f"""
            <div class="kpi-card" style="padding:14px 16px;margin-bottom:8px">
                <div class="kpi-value" style="font-size:1.2rem">{val}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-delta">{unit}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")
    rb1, _rb2, _rb3 = st.columns([1,1,4])
    with rb1:
        if st.button("↺  Reset to Defaults", use_container_width=True, key="reset_mbm"):
            st.session_state.prices = dict(DEFAULT_PRICES)
            st.session_state.tech_inputs = {k: list(v) for k,v in DEFAULTS.items()}
            st.rerun()
