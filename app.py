import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="MBM Revenue Model",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────
# CSS — JobEntry-inspired Light Green
# Fix 1: block-container padding so header is NOT cut off
# Fix 2: sidebar only highlights active nav button
# Fix 3: chart wrappers via CSS [data-testid] instead of raw HTML divs
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── GLOBAL ── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #f5f7fa !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    min-width: 240px !important;
    max-width: 240px !important;
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    box-shadow: 2px 0 16px rgba(0,0,0,0.05) !important;
}
[data-testid="stSidebarContent"] { padding: 0 !important; }
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* ── FIX MAIN AREA — no cut-off ── */
.block-container {
    padding: 1.5rem 1.75rem 2rem 1.75rem !important;
    max-width: 100% !important;
    background: #f5f7fa !important;
}

/* ── PAGE HEADER ── */
.page-header {
    background: linear-gradient(135deg, #065f46 0%, #059669 55%, #34d399 100%);
    border-radius: 14px;
    padding: 26px 30px 24px 30px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
}
.page-header::after {
    content: '';
    position: absolute; right: -50px; top: -50px;
    width: 200px; height: 200px; border-radius: 50%;
    background: rgba(255,255,255,0.07);
    pointer-events: none;
}
.page-header-badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 99px;
    padding: 3px 12px;
    font-size: 0.65rem;
    font-weight: 700;
    color: rgba(255,255,255,0.9);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
}
.page-header-title {
    font-size: 1.45rem; font-weight: 800;
    color: #ffffff; letter-spacing: -0.02em;
    margin: 0 0 5px 0; line-height: 1.2;
}
.page-header-sub {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.72);
    margin: 0; font-weight: 400;
}

/* ── KPI CARDS ── */
.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px 16px 20px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    position: relative;
    overflow: hidden;
    height: 100%;
}
.kpi-card::before {
    content: '';
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 4px; border-radius: 12px 0 0 12px;
    background: linear-gradient(180deg, #059669, #34d399);
}
.kpi-value {
    font-size: 1.55rem; font-weight: 800;
    color: #064e3b; line-height: 1;
    margin-bottom: 6px; font-variant-numeric: tabular-nums;
}
.kpi-label {
    font-size: 0.66rem; font-weight: 700;
    color: #9ca3af; text-transform: uppercase; letter-spacing: 0.09em;
    margin-bottom: 4px;
}
.kpi-sub { font-size: 0.73rem; color: #059669; font-weight: 500; }

/* ── SECTION HEADING ── */
.sec-head {
    font-size: 0.68rem; font-weight: 700;
    color: #059669; text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 20px 0 12px 0;
    display: flex; align-items: center; gap: 8px;
}
.sec-head::after {
    content: ''; flex: 1; height: 1.5px;
    background: linear-gradient(90deg, #d1fae5, transparent);
}

/* ── CHART CONTAINERS — wrap plotly natively ── */
[data-testid="stPlotlyChart"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 14px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04) !important;
    overflow: hidden !important;
}

/* ── SIDEBAR NAV BUTTONS — ONLY active is green ── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #374151 !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 10px 14px !important;
    box-shadow: none !important;
    transition: background 0.15s, color 0.15s !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #f0fdf4 !important;
    color: #059669 !important;
}
/* Active nav button override via key prefix — handled in Python with active_style */

/* ── RESET BUTTON — distinct style ── */
.reset-btn > button {
    background: #fff7ed !important;
    color: #c2410c !important;
    border: 1px solid #fed7aa !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
}

/* ── PROGRESS BARS ── */
.prog-wrap { margin-bottom: 9px; }
.prog-row {
    display: flex; justify-content: space-between;
    font-size: 0.73rem; color: #6b7280; margin-bottom: 3px;
}
.prog-row b { color: #1f2937; font-weight: 600; }
.prog-bg { background: #f0fdf4; border-radius: 6px; height: 5px; }
.prog-fill {
    height: 5px; border-radius: 6px;
    background: linear-gradient(90deg, #059669, #34d399);
}

/* ── MBM CHIPS ── */
.chip {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 4px 11px; border-radius: 99px;
    font-size: 0.7rem; font-weight: 600; margin: 2px;
}
.chip-on  { background: #d1fae5; border: 1px solid #6ee7b7; color: #065f46; }
.chip-off { background: #f9fafb; border: 1px solid #e5e7eb; color: #d1d5db; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0; background: transparent !important;
    border-bottom: 2px solid #e2e8f0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    font-size: 0.79rem !important;
    color: #9ca3af !important;
    padding: 9px 20px !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
    color: #059669 !important;
    border-bottom: 2px solid #059669 !important;
    font-weight: 700 !important;
}

/* ── SLIDERS ── */
[data-testid="stSlider"] [data-testid="stSliderThumb"] { background: #059669 !important; }

/* ── SELECTBOX ── */
[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrameResizable"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

hr { border-color: #e2e8f0 !important; margin: 12px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────
TECHNOLOGIES = [
    "Solar PV & Wind Energy","Green Hydrogen","SAF (Sust. Aviation Fuel)","CCUS",
    "Battery Storage & EVs","Low-carbon Steel & Cement","Ammonia (green/blue)",
    "Methanol (green/e-methanol)","Reforestation / REDD+ / NBS","Blue Carbon (mangroves)",
    "Direct Air Capture (DAC)","Building Energy Efficiency",
    "Carbon Offsetting / MRV Tech","Energy Mgmt & Analytics",
]
TECH_SHORT = ["Solar/Wind","Green H₂","SAF","CCUS","Battery/EV","Steel/Cement",
              "Ammonia","Methanol","Reforest.","Blue Carbon","DAC","Bldg Eff.","MRV Tech","Energy Mgmt"]
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
    "ets":("ETS / Carbon Market","USD/tCO₂e"),"ctax":("Carbon Tax","USD/tCO₂e"),
    "fuel":("Fuel Mandate","USD/MWh"),"cfd":("CfD / CCfD","USD/MWh"),
    "cbam":("CBAM Import","USD/tCO₂e"),"corsia":("CORSIA Credit","USD/tCO₂e"),
    "imo":("IMO Levy","USD/tCO₂e"),"vcm":("VCM / CDM Credit","USD/tCO₂e"),
    "amc":("AMC","USD/unit"),"feebate":("Feebate","USD/tCO₂e"),
}
DEFAULT_PRICES = {
    "ets":100,"ctax":50,"fuel":240,"cfd_strike":120,"cfd_ref":80,
    "cbam":55,"corsia":22.25,"imo":380,"vcm":100,"amc":100,
    "feebate":50,"electricity":60,"gas":8,"biomass":40
}

GREENS = ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399","#6ee7b7","#a7f3d0"]
PBG = "rgba(0,0,0,0)"
FC  = "#374151"
GC  = "rgba(5,150,105,0.07)"

def pl(h=380, ml=20, mr=20, mt=20, mb=30):
    return dict(
        paper_bgcolor=PBG, plot_bgcolor=PBG,
        font=dict(family="Inter", color=FC, size=10),
        height=h, margin=dict(l=ml, r=mr, t=mt, b=mb),
        legend=dict(orientation="h", y=-0.22, font=dict(size=9)),
        xaxis=dict(gridcolor=GC, linecolor="#e2e8f0", zeroline=False,
                   tickfont=dict(size=9)),
        yaxis=dict(gridcolor=GC, linecolor="#e2e8f0", zeroline=False,
                   tickfont=dict(size=9)),
    )

def calc_crf(w,l): return 1/l if w==0 else (w*(1+w)**l)/((1+w)**l-1)

def compute(prices, t, ti):
    o=ti["annual_output"][t]; ck=ti["installed_capacity"][t]*1000
    lt=ti["project_lifetime"][t]; w=ti["wacc"][t]
    cap=ck*ti["capex_per_kw"][t]; crf=calc_crf(w,lt)
    ac=cap*crf; fo=cap*ti["opex_pct"][t]
    tc=ac+fo+ti["feedstock_cost"][t]+ti["other_opex"][t]
    co2=o*ti["co2_abated_factor"][t]
    dr=(ti["clients"][t]*ti["market_price"][t]) if t in [12,13] else o*ti["market_price"][t]
    e=co2*prices["ets"]    if DEFAULTS["ets"][t]    else 0
    cx=co2*prices["ctax"]  if DEFAULTS["ctax"][t]   else 0
    v=co2*prices["vcm"]    if DEFAULTS["vcm"][t]    else 0
    fu=o*ti["capacity_factor"][t]*prices["fuel"]*0.85 if DEFAULTS["fuel"][t] and o>0 else 0
    cf=o*max(0,prices["cfd_strike"]-prices["cfd_ref"])*0.5 if DEFAULTS["cfd"][t] and o>0 else 0
    cb=co2*prices["cbam"]*0.85    if DEFAULTS["cbam"][t]    else 0
    co=co2*prices["corsia"]*1.05  if DEFAULTS["corsia"][t]  else 0
    im=co2*prices["imo"]*0.95     if DEFAULTS["imo"][t]     else 0
    am=(o/1000)*prices["amc"]*0.5 if DEFAULTS["amc"][t]     else 0
    fb=co2*prices["feebate"]*0.5  if DEFAULTS["feebate"][t] else 0
    mb=e+cx+fu+cf+cb+co+im+v+am+fb; tr=mb+dr
    return {"tc":tc,"ac":ac,"fo":fo,"co2":co2,"dr":dr,"mb":mb,"tr":tr,
            "nc":tr-tc,"lr":tr*lt,"rc":tr/tc if tc>0 else 0,
            "bd":{"ETS":e,"Carbon Tax":cx,"Fuel Mandate":fu,"CfD":cf,
                  "CBAM":cb,"CORSIA":co,"IMO Levy":im,"VCM/CDM":v,"AMC":am,"Feebate":fb}}

def fm(v): return f"${v/1e6:.1f}M"

def kpi(val, label, sub=""):
    s = (f'<div class="kpi-sub">{sub}</div>' if sub else "")
    return (f'<div class="kpi-card">' +
            f'<div class="kpi-label">{label}</div>' +
            f'<div class="kpi-value">{val}</div>{s}</div>')

# ── SESSION STATE ──
if "ti"   not in st.session_state: st.session_state.ti = {k:list(v) for k,v in DEFAULTS.items()}
if "p"    not in st.session_state: st.session_state.p  = dict(DEFAULT_PRICES)
if "page" not in st.session_state: st.session_state.page = "Portfolio Overview"

# ═════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════
NAV = [
    ("Portfolio Overview",  "📊"),
    ("Technology Detail",   "🔬"),
    ("Scenario Analysis",   "📈"),
    ("NPV Analysis",        "💰"),
    ("Tech Calculations",   "🧮"),
    ("Spatial Viability",   "🌍"),
    ("Data Table",          "🗂️"),
    ("MBM Price Controls",  "⚙️"),
]

with st.sidebar:
    # Logo block
    st.markdown("""
    <div style="padding:22px 18px 16px 18px;border-bottom:1px solid #f1f5f9;">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:38px;height:38px;border-radius:10px;flex-shrink:0;
                        background:linear-gradient(135deg,#059669,#34d399);
                        display:flex;align-items:center;justify-content:center;
                        font-size:18px;box-shadow:0 3px 10px rgba(5,150,105,0.28);">🌿</div>
            <div>
                <div style="font-size:0.88rem;font-weight:800;color:#064e3b;
                            letter-spacing:-0.01em;line-height:1.1;">MBM Revenue</div>
                <div style="font-size:0.65rem;color:#9ca3af;margin-top:2px;">Model Dashboard</div>
            </div>
        </div>
    </div>
    <div style="padding:14px 18px 5px;font-size:0.6rem;color:#cbd5e1;
                font-weight:700;text-transform:uppercase;letter-spacing:0.12em;">
        Main Menu
    </div>
    """, unsafe_allow_html=True)

    for label, icon in NAV:
        active = (st.session_state.page == label)
        # Inject inline style for active button via a container trick
        if active:
            st.markdown(f"""
            <style>
            [data-testid="stSidebar"] div[data-testid="stButton"]:has(button[kind="secondary"][title="{label}"]) button,
            div[key="nav_{label}"] button {{
                background: linear-gradient(90deg,#059669,#10b981) !important;
                color: #ffffff !important;
                font-weight: 700 !important;
            }}
            </style>""", unsafe_allow_html=True)
            # Use a unique container per button
            active_container = st.container()
            with active_container:
                if st.button(f"{icon}  {label}", key=f"nav_{label}",
                             use_container_width=True,
                             help=label):
                    st.session_state.page = label
                    st.rerun()
            # Apply active style after rendering
            st.markdown(f"""
            <script>
            var btns = window.parent.document.querySelectorAll('button');
            btns.forEach(b => {{
                if(b.innerText.trim().startsWith('{icon}')) {{
                    b.style.background = 'linear-gradient(90deg,#059669,#10b981)';
                    b.style.color = '#fff';
                    b.style.fontWeight = '700';
                }}
            }});
            </script>""", unsafe_allow_html=True)
        else:
            if st.button(f"{icon}  {label}", key=f"nav_{label}",
                         use_container_width=True):
                st.session_state.page = label
                st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown('<hr style="margin:0 0 10px 0;">', unsafe_allow_html=True)

    # Reset button with orange/red tint
    with st.container():
        st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
        if st.button("↺  Reset Defaults", use_container_width=True, key="rst"):
            st.session_state.p  = dict(DEFAULT_PRICES)
            st.session_state.ti = {k:list(v) for k,v in DEFAULTS.items()}
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── PRE-COMPUTE ──
AR  = [compute(st.session_state.p, i, st.session_state.ti) for i in range(14)]
TR  = sum(r["tr"] for r in AR);  TM = sum(r["mb"] for r in AR)
TD  = sum(r["dr"] for r in AR);  TC = sum(r["tc"] for r in AR)
TN  = sum(r["nc"] for r in AR);  TCO= sum(r["co2"] for r in AR)
page = st.session_state.page

# ═════════════════════════════════════════════
# PAGE 1 — PORTFOLIO OVERVIEW
# ═════════════════════════════════════════════
if page == "Portfolio Overview":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Carbon Market Intelligence</div>
        <div class="page-header-title">📊 Portfolio Overview</div>
        <div class="page-header-sub">Annual revenue performance across all 14 clean technology verticals</div>
    </div>''', unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(kpi(fm(TR), "Total Annual Revenue", "Portfolio-wide"),         unsafe_allow_html=True)
    c2.markdown(kpi(fm(TM), "MBM Revenue",          f"{TM/TR*100:.1f}% of total"), unsafe_allow_html=True)
    c3.markdown(kpi(fm(TD), "Direct Revenue",        f"{TD/TR*100:.1f}% of total"), unsafe_allow_html=True)
    c4.markdown(kpi(fm(TN), "Net Cash Flow",         f"R/C {TR/TC:.2f}×"),          unsafe_allow_html=True)
    c5.markdown(kpi(f"{TCO/1e6:.2f}M tCO₂e", "CO₂ Abated", "per year"),       unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Revenue by Technology</div>', unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2])

    with col_l:
        srt = sorted(range(14), key=lambda i: AR[i]["tr"], reverse=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="MBM Revenue",
            x=[TECH_SHORT[i] for i in srt],
            y=[AR[i]["mb"]/1e6 for i in srt],
            marker_color="#059669"))
        fig.add_trace(go.Bar(name="Direct Revenue",
            x=[TECH_SHORT[i] for i in srt],
            y=[AR[i]["dr"]/1e6 for i in srt],
            marker_color="#34d399"))
        fig.add_trace(go.Bar(name="Cost",
            x=[TECH_SHORT[i] for i in srt],
            y=[-AR[i]["tc"]/1e6 for i in srt],
            marker_color="#dcfce7"))
        fig.update_layout(**pl(400))
        fig.update_layout(barmode="relative",
            xaxis=dict(tickangle=-38),
            yaxis_title="USD Million")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        agg = {}
        for r in AR:
            for k, v in r["bd"].items(): agg[k] = agg.get(k, 0) + v
        mf = {k: v for k, v in agg.items() if v > 0}
        fig2 = go.Figure(go.Pie(
            labels=list(mf.keys()), values=list(mf.values()),
            hole=0.52, textinfo="label+percent",
            marker=dict(colors=GREENS[:len(mf)]),
            textfont=dict(size=8.5, color=FC),
        ))
        fig2.update_layout(**pl(400, ml=10, mr=10, mt=30, mb=30))
        fig2.update_layout(showlegend=False,
            title=dict(text="MBM Revenue Mix", font=dict(size=11, color=FC), y=0.98))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="sec-head">Net Annual Cash Flow</div>', unsafe_allow_html=True)
    nv = [AR[i]["nc"]/1e6 for i in range(14)]
    fig3 = go.Figure(go.Bar(x=TECH_SHORT, y=nv,
        marker_color=["#059669" if v >= 0 else "#fca5a5" for v in nv],
        text=[f"${v:.1f}M" for v in nv],
        textposition="outside",
        textfont=dict(size=9, color=FC)))
    fig3.update_layout(**pl(290, mb=60))
    fig3.update_layout(xaxis=dict(tickangle=-38), yaxis_title="USD Million")
    st.plotly_chart(fig3, use_container_width=True)

    # ── Stacked MBM Revenue + Comparison charts (side by side) ──
    st.markdown('<div class="sec-head">MBM Policy Intervention — Stacked Revenue & Direct vs MBM Comparison</div>', unsafe_allow_html=True)
    ch_l, ch_r = st.columns(2)

    with ch_l:
        mbm_keys  = ["ETS","Carbon Tax","Fuel Mandate","CfD","CBAM","CORSIA","IMO Levy","VCM/CDM","AMC","Feebate"]
        mbm_colors = ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399",
                      "#6ee7b7","#a7f3d0","#d1fae5","#ecfdf5"]
        srt_stk = sorted(range(14), key=lambda i: AR[i]["mb"], reverse=True)
        fig_stk = go.Figure()
        for mkey, mcol in zip(mbm_keys, mbm_colors):
            vals = [AR[i]["bd"].get(mkey, 0) / 1e6 for i in srt_stk]
            fig_stk.add_trace(go.Bar(
                name=mkey,
                x=[TECH_SHORT[i] for i in srt_stk],
                y=vals,
                marker_color=mcol,
                text=[f"${v:.1f}M" if v > 2 else "" for v in vals],
                textposition="inside",
                textfont=dict(size=7.5, color="#ffffff"),
            ))
        fig_stk.update_layout(**pl(420, mb=80))
        fig_stk.update_layout(
            barmode="stack",
            xaxis=dict(tickangle=-42),
            yaxis_title="USD Million",
            legend=dict(orientation="h", y=-0.32, font=dict(size=8)),
            title=dict(text="Revenue from MBM Policy Intervention",
                       font=dict(size=11, color=FC), y=0.98))
        st.plotly_chart(fig_stk, use_container_width=True)

    with ch_r:
        srt_cmp = sorted(range(14), key=lambda i: AR[i]["tr"], reverse=True)
        fig_cmp = go.Figure()
        fig_cmp.add_trace(go.Bar(
            name="Direct Product/Service Revenue",
            x=[AR[i]["dr"] / 1e6 for i in srt_cmp],
            y=[TECH_SHORT[i] for i in srt_cmp],
            orientation="h",
            marker_color="#dc2626",
            text=[f"${AR[i]['dr']/1e6:.0f}M" if AR[i]["dr"] > 1e6 else "" for i in srt_cmp],
            textposition="inside",
            textfont=dict(size=8, color="#ffffff"),
        ))
        fig_cmp.add_trace(go.Bar(
            name="MBM Revenue",
            x=[AR[i]["mb"] / 1e6 for i in srt_cmp],
            y=[TECH_SHORT[i] for i in srt_cmp],
            orientation="h",
            marker_color="#059669",
            text=[f"${AR[i]['mb']/1e6:.0f}M" if AR[i]["mb"] > 1e6 else "" for i in srt_cmp],
            textposition="inside",
            textfont=dict(size=8, color="#ffffff"),
        ))
        fig_cmp.update_layout(**pl(420, ml=90, mb=40))
        fig_cmp.update_layout(
            barmode="group",
            xaxis_title="USD Million",
            legend=dict(orientation="h", y=-0.12, font=dict(size=8)),
            title=dict(text="Comparison of Revenue from MBM and Direct Revenue",
                       font=dict(size=11, color=FC), y=0.98))
        st.plotly_chart(fig_cmp, use_container_width=True)

    st.markdown('<div class="sec-head">Technology Ranking</div>', unsafe_allow_html=True)
    srt2 = sorted(range(14), key=lambda i: AR[i]["tr"], reverse=True)
    mx = AR[srt2[0]]["tr"]
    r1, r2 = st.columns(2)
    for rank, i in enumerate(srt2):
        col = r1 if rank % 2 == 0 else r2
        pct = AR[i]["tr"] / mx * 100
        col.markdown(f'''<div class="prog-wrap">
            <div class="prog-row"><span>{TECH_SHORT[i]}</span><b>{fm(AR[i]["tr"])}</b></div>
            <div class="prog-bg"><div class="prog-fill" style="width:{pct:.1f}%"></div></div>
        </div>''', unsafe_allow_html=True)

# ═════════════════════════════════════════════
# PAGE 2 — TECHNOLOGY DETAIL
# ═════════════════════════════════════════════
elif page == "Technology Detail":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Technology Analysis</div>
        <div class="page-header-title">🔬 Technology Detail</div>
        <div class="page-header-sub">Configure individual technology parameters and view granular revenue breakdown</div>
    </div>''', unsafe_allow_html=True)

    ti = st.session_state.ti
    sel = st.selectbox("Select Technology", TECHNOLOGIES, index=0)
    t = TECHNOLOGIES.index(sel)

    st.markdown('<div class="sec-head">Technology Inputs</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Scale & Output**")
        ti["annual_output"][t]      = st.number_input("Annual Output (MWh/yr)", 0, 10_000_000, int(ti["annual_output"][t]),      10000, key=f"ao{t}")
        ti["installed_capacity"][t] = st.number_input("Installed Capacity (MW)", 0, 5000,      int(ti["installed_capacity"][t]), 10,    key=f"ic{t}")
        ti["capacity_factor"][t]    = st.slider("Capacity Factor",     0.0, 1.0, ti["capacity_factor"][t],  0.01, key=f"cf{t}")
        ti["project_lifetime"][t]   = st.slider("Project Lifetime (yr)", 5, 50,  int(ti["project_lifetime"][t]), 1, key=f"pl{t}")
    with c2:
        st.markdown("**Cost Structure**")
        ti["capex_per_kw"][t]   = st.number_input("CAPEX/kW (USD/kW)", 0, 20000,     int(ti["capex_per_kw"][t]),   100,    key=f"ck{t}")
        ti["opex_pct"][t]       = st.slider("OPEX (% CAPEX p.a.)", 0.0, 0.20, ti["opex_pct"][t],      0.005, format="%.3f", key=f"op{t}")
        ti["feedstock_cost"][t] = st.number_input("Feedstock (USD/yr)", 0, 50_000_000, int(ti["feedstock_cost"][t]), 100000, key=f"fc{t}")
        ti["other_opex"][t]     = st.number_input("Other OPEX (USD/yr)", 0, 20_000_000, int(ti["other_opex"][t]),    100000, key=f"ov{t}")
        ti["wacc"][t]           = st.slider("WACC", 0.01, 0.25, ti["wacc"][t], 0.005, format="%.3f", key=f"wc{t}")
    with c3:
        st.markdown("**Revenue Drivers**")
        ti["market_price"][t]      = st.number_input("Market Price (USD/unit)", 0, 100000, int(ti["market_price"][t]),     10, key=f"mp{t}")
        ti["co2_abated_factor"][t] = st.slider("CO₂ Abated / Unit", 0.0, 2.0, ti["co2_abated_factor"][t], 0.01, key=f"ca{t}")
        if t in [12, 13]:
            ti["clients"][t] = st.number_input("Clients", 0, 10000, int(ti["clients"][t]), 1, key=f"cl{t}")

    r = compute(st.session_state.p, t, ti)
    st.markdown('<div class="sec-head">Results</div>', unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.markdown(kpi(fm(r["tr"]), "Total Revenue"),                     unsafe_allow_html=True)
    m2.markdown(kpi(fm(r["mb"]), "MBM Revenue"),                       unsafe_allow_html=True)
    m3.markdown(kpi(fm(r["dr"]), "Direct Revenue"),                    unsafe_allow_html=True)
    m4.markdown(kpi(fm(r["tc"]), "Total Cost"),                        unsafe_allow_html=True)
    m5.markdown(kpi(fm(r["nc"]), "Net Cash Flow", f"R/C {r['rc']:.2f}×"), unsafe_allow_html=True)

    ca, cb = st.columns(2)
    with ca:
        st.markdown('<div class="sec-head">MBM Breakdown</div>', unsafe_allow_html=True)
        bd = {k: v for k, v in r["bd"].items() if v > 0}
        if bd:
            sb = sorted(bd.items(), key=lambda x: x[1], reverse=True)
            fb = go.Figure(go.Bar(
                x=[x[0] for x in sb], y=[x[1]/1e6 for x in sb],
                marker=dict(color=list(range(len(sb))),
                    colorscale=[[0,"#a7f3d0"],[0.5,"#059669"],[1,"#064e3b"]]),
                text=[f"${x[1]/1e6:.2f}M" for x in sb],
                textposition="outside", textfont=dict(size=9, color=FC)))
            fb.update_layout(**pl(310))
            fb.update_yaxes(title_text="USD Million")
            st.plotly_chart(fb, use_container_width=True)
        else:
            st.info("No active MBM mechanisms for this technology.")

    with cb:
        st.markdown('<div class="sec-head">Cost vs Revenue</div>', unsafe_allow_html=True)
        cats = ["Direct Rev","MBM Rev","CAPEX ann.","Fixed OPEX","Feedstock","Other OPEX"]
        vals = [r["dr"]/1e6, r["mb"]/1e6, -r["ac"]/1e6, -r["fo"]/1e6,
                -ti["feedstock_cost"][t]/1e6, -ti["other_opex"][t]/1e6]
        fw = go.Figure(go.Bar(x=cats, y=vals,
            marker_color=["#059669" if v >= 0 else "#fca5a5" for v in vals],
            text=[f"${abs(v):.2f}M" for v in vals],
            textposition="outside", textfont=dict(size=9, color=FC)))
        fw.add_hline(y=0, line_color="#e2e8f0", line_width=1.5)
        fw.update_layout(**pl(310))
        fw.update_layout(xaxis=dict(tickangle=-30))
        fw.update_yaxes(title_text="USD Million")
        st.plotly_chart(fw, use_container_width=True)

    st.markdown('<div class="sec-head">Active MBM Mechanisms</div>', unsafe_allow_html=True)
    mechs = ["ets","ctax","fuel","cfd","cbam","corsia","imo","vcm","amc","feebate"]
    html = ""
    for m in mechs:
        on = DEFAULTS[m][t]; lbl = MBM_LABELS[m][0]
        html += f'<span class="chip {"chip-on" if on else "chip-off"}">{"✓" if on else "✕"} {lbl}</span>'
    st.markdown(html, unsafe_allow_html=True)

# ═════════════════════════════════════════════
# PAGE 3 — SCENARIO ANALYSIS
# ═════════════════════════════════════════════
elif page == "Scenario Analysis":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">What-If Analysis</div>
        <div class="page-header-title">📈 Scenario Analysis</div>
        <div class="page-header-sub">Stress-test portfolio revenue under varying carbon price assumptions</div>
    </div>''', unsafe_allow_html=True)

    bp = dict(st.session_state.p)
    er = list(range(10, 310, 10))
    tvs, mvs, nvs = [], [], []
    for ep in er:
        tp = {**bp, "ets": ep}
        res = [compute(tp, i, st.session_state.ti) for i in range(14)]
        tvs.append(sum(r["tr"] for r in res)/1e6)
        mvs.append(sum(r["mb"] for r in res)/1e6)
        nvs.append(sum(r["nc"] for r in res)/1e6)

    st.markdown('<div class="sec-head">ETS Carbon Price Sensitivity</div>', unsafe_allow_html=True)
    fs = make_subplots(rows=1, cols=2, subplot_titles=("Total Revenue & Net CF", "MBM Revenue"))
    fs.add_trace(go.Scatter(x=er, y=tvs, name="Total Revenue",  line=dict(color="#059669",  width=2.5)), row=1, col=1)
    fs.add_trace(go.Scatter(x=er, y=nvs, name="Net Cash Flow",  line=dict(color="#34d399",  width=2, dash="dot")), row=1, col=1)
    fs.add_trace(go.Scatter(x=er, y=mvs, name="MBM Revenue",
        fill="tozeroy", fillcolor="rgba(5,150,105,0.08)",
        line=dict(color="#059669", width=2)), row=1, col=2)
    for ci in [1, 2]:
        fs.add_vline(x=bp["ets"], line_color="#d1fae5", line_dash="dash", row=1, col=ci)
    fs.update_layout(
        paper_bgcolor=PBG, plot_bgcolor=PBG,
        font=dict(family="Inter", color=FC, size=10),
        height=380, margin=dict(l=20, r=20, t=38, b=20),
        legend=dict(orientation="h", y=-0.15, font=dict(size=9)))
    for ax in ["xaxis","xaxis2"]:
        fs.update_layout(**{ax: dict(gridcolor=GC, title_text="ETS Price (USD/tCO₂e)",
                                     title_font=dict(size=9), tickfont=dict(size=9))})
    for ax in ["yaxis","yaxis2"]:
        fs.update_layout(**{ax: dict(gridcolor=GC, title_text="USD Million",
                                     title_font=dict(size=9), tickfont=dict(size=9))})
    st.plotly_chart(fs, use_container_width=True)

    st.markdown('<div class="sec-head">Multi-Scenario Comparison</div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        el = st.slider("ETS Low",   10, 200, 50,        10)
        eb = st.slider("ETS Base",  10, 300, bp["ets"],  10)
        eh = st.slider("ETS High",  50, 500, 200,        10)
    with sc2:
        vl = st.slider("VCM Low",   5, 100, 30,          5)
        vb = st.slider("VCM Base",  5, 300, bp["vcm"],   5)
        vh = st.slider("VCM High",  50, 500, 200,         5)

    scens = {"Low":  {**bp,"ets":el,"vcm":vl},
             "Base": {**bp,"ets":eb,"vcm":vb},
             "High": {**bp,"ets":eh,"vcm":vh}}
    sr = {}
    for sn, sp in scens.items():
        res = [compute(sp, i, st.session_state.ti) for i in range(14)]
        sr[sn] = {"tr": sum(r["tr"] for r in res),
                  "mb": sum(r["mb"] for r in res),
                  "nc": sum(r["nc"] for r in res)}

    km1, km2, km3 = st.columns(3)
    for col, sn in zip([km1, km2, km3], sr):
        col.markdown(kpi(fm(sr[sn]["tr"]), f"{sn} Scenario",
                         f"MBM {fm(sr[sn]['mb'])}  ·  Net CF {fm(sr[sn]['nc'])}"),
                     unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    fsc = go.Figure()
    colors = {"Total Revenue":"#059669","MBM Revenue":"#064e3b","Net Cash Flow":"#34d399"}
    for m, lbl in [("tr","Total Revenue"),("mb","MBM Revenue"),("nc","Net Cash Flow")]:
        fsc.add_trace(go.Bar(name=lbl, x=list(sr.keys()),
                             y=[sr[s][m]/1e6 for s in sr],
                             marker_color=colors[lbl]))
    fsc.update_layout(**pl(320))
    fsc.update_layout(barmode="group")
    fsc.update_yaxes(title_text="USD Million")
    st.plotly_chart(fsc, use_container_width=True)

# ═════════════════════════════════════════════
# PAGE 4 — DATA TABLE
# ═════════════════════════════════════════════
elif page == "Data Table":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Full Dataset</div>
        <div class="page-header-title">🗂️ Data Table</div>
        <div class="page-header-sub">Complete revenue summary and MBM breakdown across all technologies</div>
    </div>''', unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["  Revenue Summary  ", "  MBM Breakdown  ", "  Applicability Heatmap  "])

    with t1:
        rows = []
        for i, r in enumerate(AR):
            rows.append({"Technology": TECHNOLOGIES[i],
                "Direct Rev ($M)":   round(r["dr"]/1e6, 2),
                "MBM Rev ($M)":      round(r["mb"]/1e6, 2),
                "Total Rev ($M)":    round(r["tr"]/1e6, 2),
                "Total Cost ($M)":   round(r["tc"]/1e6, 2),
                "Net CF ($M)":       round(r["nc"]/1e6, 2),
                "R/C Ratio":         round(r["rc"], 2),
                "CO₂ Abated (Mt)":   round(r["co2"]/1e6, 3),
                "Lifetime Rev ($M)": round(r["lr"]/1e6, 1),
            })
        df = pd.DataFrame(rows)
        st.dataframe(df.style.bar(
            subset=["Total Rev ($M)", "Net CF ($M)"], color="#bbf7d0"),
            use_container_width=True, height=500)
        st.download_button("⬇ Download CSV", df.to_csv(index=False).encode(),
                           "revenue_summary.csv", "text/csv")

    with t2:
        mbrows = []
        for i, r in enumerate(AR):
            row = {"Technology": TECH_SHORT[i]}
            for k, v in r["bd"].items(): row[f"{k} ($M)"] = round(v/1e6, 2)
            row["Total MBM ($M)"] = round(r["mb"]/1e6, 2)
            mbrows.append(row)
        dfm = pd.DataFrame(mbrows)
        st.dataframe(dfm.style.bar(
            subset=["Total MBM ($M)"], color="#bbf7d0"),
            use_container_width=True, height=500)
        st.download_button("⬇ Download CSV", dfm.to_csv(index=False).encode(),
                           "mbm_breakdown.csv", "text/csv")

    with t3:
        mechs = ["ets","ctax","fuel","cfd","cbam","corsia","imo","vcm","amc","feebate"]
        mlbl  = [MBM_LABELS[m][0] for m in mechs]
        z     = [[DEFAULTS[m][i] for m in mechs] for i in range(14)]
        fhm   = go.Figure(go.Heatmap(
            z=z, x=mlbl, y=TECH_SHORT,
            colorscale=[[0,"#f9fafb"],[0.01,"#d1fae5"],[1,"#059669"]],
            showscale=True,
            colorbar=dict(title=dict(text="Active", font=dict(size=9)),
                tickvals=[0,1], ticktext=["No","Yes"],
                tickfont=dict(size=9),
                bgcolor="rgba(0,0,0,0)"),
            hovertemplate="<b>%{y}</b> × <b>%{x}</b><br>Active: %{z}<extra></extra>",
        ))
        for i in range(14):
            for j, m in enumerate(mechs):
                if z[i][j]:
                    fhm.add_annotation(x=mlbl[j], y=TECH_SHORT[i], text="✓",
                        showarrow=False, font=dict(size=11, color="#065f46"))
        fhm.update_layout(**pl(520, ml=100, mr=40, mt=20, mb=110))
        fhm.update_layout(xaxis=dict(tickangle=-42, side="bottom"))
        st.plotly_chart(fhm, use_container_width=True)

# ═════════════════════════════════════════════
# PAGE 5 — MBM PRICE CONTROLS
# ═════════════════════════════════════════════
elif page == "MBM Price Controls":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Global Parameters</div>
        <div class="page-header-title">⚙️ MBM Price Controls</div>
        <div class="page-header-sub">Adjust all market-based mechanism parameters — changes propagate instantly to all pages</div>
    </div>''', unsafe_allow_html=True)

    p = st.session_state.p

    st.markdown('<div class="sec-head">Carbon Pricing</div>', unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        p["ets"]     = st.slider("ETS / Carbon Market (USD/tCO₂e)",  10,  300, p["ets"],      5, key="mb_ets")
        p["ctax"]    = st.slider("Carbon Tax (USD/tCO₂e)",            0,  200, p["ctax"],      5, key="mb_ctax")
        p["corsia"]  = st.slider("CORSIA Credit (USD/tCO₂e)",         3,  100, int(p["corsia"]),1, key="mb_corsia")
    with pc2:
        p["vcm"]     = st.slider("VCM / CDM Credit (USD/tCO₂e)",      5,  300, p["vcm"],       5, key="mb_vcm")
        p["cbam"]    = st.slider("CBAM Import Cost (USD/tCO₂e)",      10,  150, p["cbam"],      5, key="mb_cbam")
        p["imo"]     = st.slider("IMO Levy (USD/tCO₂e)",              50,  800, p["imo"],      10, key="mb_imo")
    with pc3:
        p["feebate"] = st.slider("Feebate Rate (USD/tCO₂e)",           0,  150, p["feebate"],   5, key="mb_feebate")
        p["amc"]     = st.slider("AMC Price (USD/unit)",               50,  300, p["amc"],      10, key="mb_amc")

    st.markdown('<div class="sec-head">Energy & Policy Prices</div>', unsafe_allow_html=True)
    pe1, pe2, _ = st.columns(3)
    with pe1:
        p["cfd_strike"] = st.slider("CfD Strike Price (USD/MWh)",     50, 300, p["cfd_strike"],  5, key="mb_cfd_s")
        p["cfd_ref"]    = st.slider("CfD Market Reference (USD/MWh)", 30, 200, p["cfd_ref"],     5, key="mb_cfd_r")
    with pe2:
        p["fuel"]       = st.slider("Fuel Mandate Offtake (USD/MWh)", 100, 600, p["fuel"],      10, key="mb_fuel")

    st.markdown('<div class="sec-head">Commodity Prices</div>', unsafe_allow_html=True)
    pco1, pco2, pco3 = st.columns(3)
    with pco1: p["electricity"] = st.slider("Grid Electricity (USD/MWh)",    20, 200, p["electricity"], 5, key="mb_elec")
    with pco2: p["gas"]         = st.slider("Natural Gas (USD/MMBtu)",         2,  30, p["gas"],         1, key="mb_gas")
    with pco3: p["biomass"]     = st.slider("Biomass / Feedstock (USD/MWh)",  10, 120, p["biomass"],     5, key="mb_bio")

    st.session_state.p = p

    st.markdown('<div class="sec-head">Current Price Summary</div>', unsafe_allow_html=True)
    items = [
        ("ETS / Carbon Market", p["ets"],         "USD/tCO₂e"),
        ("Carbon Tax",          p["ctax"],         "USD/tCO₂e"),
        ("VCM / CDM Credit",    p["vcm"],          "USD/tCO₂e"),
        ("CBAM Import",         p["cbam"],         "USD/tCO₂e"),
        ("CORSIA Credit",       p["corsia"],       "USD/tCO₂e"),
        ("IMO Levy",            p["imo"],          "USD/tCO₂e"),
        ("Feebate",             p["feebate"],      "USD/tCO₂e"),
        ("CfD Strike",          p["cfd_strike"],   "USD/MWh"),
        ("CfD Reference",       p["cfd_ref"],      "USD/MWh"),
        ("Fuel Mandate",        p["fuel"],         "USD/MWh"),
        ("AMC Price",           p["amc"],          "USD/unit"),
        ("Grid Electricity",    p["electricity"],  "USD/MWh"),
        ("Natural Gas",         p["gas"],          "USD/MMBtu"),
        ("Biomass/Feedstock",   p["biomass"],      "USD/MWh"),
    ]
    cols = st.columns(4)
    for idx, (lbl, val, unit) in enumerate(items):
        cols[idx%4].markdown(kpi(val, lbl, unit), unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    rb1, _, _ = st.columns([1,1,4])
    with rb1:
        if st.button("↺  Reset to Defaults", use_container_width=True, key="rst_mbm"):
            st.session_state.p  = dict(DEFAULT_PRICES)
            st.session_state.ti = {k:list(v) for k,v in DEFAULTS.items()}
            st.rerun()

# ═════════════════════════════════════════════
# PAGE 6 — NPV ANALYSIS (with MBM)
# ═════════════════════════════════════════════
elif page == "NPV Analysis":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Investment Valuation</div>
        <div class="page-header-title">💰 NPV Analysis</div>
        <div class="page-header-sub">Net Present Value incorporating MBM revenue streams and forecast assumptions</div>
    </div>''', unsafe_allow_html=True)

    # ── NPV Theory Card ──
    st.markdown("""
    <div style="background:#f0fdf4;border:1px solid #6ee7b7;border-radius:10px;padding:14px 18px;margin-bottom:18px;">
    <div style="font-size:0.75rem;font-weight:700;color:#065f46;margin-bottom:6px;">NPV EQUATION WITH MBM</div>
    <div style="font-size:0.82rem;color:#1f2937;font-family:monospace;">
    NPV = −CAPEX  +  Σ<sub>t=1..T</sub>  [ (Direct_Rev<sub>t</sub> + MBM_Rev<sub>t</sub> − OPEX<sub>t</sub>) / (1 + WACC)<sup>t</sup> ]
    </div>
    <div style="font-size:0.72rem;color:#6b7280;margin-top:6px;">
    MBM_Rev<sub>t</sub> = ETS<sub>t</sub> + Carbon Tax<sub>t</sub> + VCM<sub>t</sub> + CfD<sub>t</sub> + CBAM<sub>t</sub> + CORSIA<sub>t</sub> + IMO<sub>t</sub> + AMC<sub>t</sub> + Feebate<sub>t</sub>
    &nbsp;|&nbsp; Carbon prices grow at user-defined annual rate
    </div>
    </div>""", unsafe_allow_html=True)

    # ── Controls ──
    st.markdown('<div class="sec-head">NPV Assumptions</div>', unsafe_allow_html=True)
    nc1, nc2, nc3 = st.columns(3)
    with nc1:
        sel_npv = st.selectbox("Technology", TECHNOLOGIES, index=0, key="npv_sel")
        t_npv = TECHNOLOGIES.index(sel_npv)
        discount_rate = st.slider("Discount Rate (WACC override %)", 2.0, 25.0,
                                   st.session_state.ti["wacc"][t_npv]*100, 0.5, key="npv_dr") / 100
    with nc2:
        mbm_growth = st.slider("Annual MBM Price Growth (%/yr)", -5.0, 20.0, 5.0, 0.5, key="npv_mg") / 100
        direct_growth = st.slider("Annual Direct Revenue Growth (%/yr)", -5.0, 15.0, 2.0, 0.5, key="npv_dg") / 100
    with nc3:
        opex_inflation = st.slider("OPEX Inflation (%/yr)", 0.0, 10.0, 2.5, 0.5, key="npv_oi") / 100
        show_mbm_toggle = st.radio("Include MBM in NPV?", ["Yes — with MBM", "No — without MBM"], key="npv_mbm")

    include_mbm = (show_mbm_toggle == "Yes — with MBM")

    # ── Compute year-by-year cash flows ──
    ti = st.session_state.ti
    p  = st.session_state.p
    lt = ti["project_lifetime"][t_npv]
    ck = ti["installed_capacity"][t_npv] * 1000
    capex_total = ck * ti["capex_per_kw"][t_npv]

    base_result = compute(p, t_npv, ti)
    base_dr   = base_result["dr"]
    base_mb   = base_result["mb"]
    base_opex = base_result["tc"] - base_result["ac"]   # exclude annualised CAPEX from annual opex

    years, cfs_mbm, cfs_no_mbm, disc_cfs_mbm, disc_cfs_no_mbm = [], [], [], [], []
    cumulative_mbm, cumulative_no = [], []
    cum_m = -capex_total
    cum_n = -capex_total

    for yr in range(1, lt + 1):
        dr_t    = base_dr   * (1 + direct_growth) ** (yr - 1)
        mb_t    = base_mb   * (1 + mbm_growth)    ** (yr - 1)
        opex_t  = base_opex * (1 + opex_inflation) ** (yr - 1)

        cf_mbm  = dr_t + mb_t - opex_t
        cf_no   = dr_t - opex_t

        dcf_mbm = cf_mbm / (1 + discount_rate) ** yr
        dcf_no  = cf_no  / (1 + discount_rate) ** yr

        years.append(yr)
        cfs_mbm.append(cf_mbm / 1e6)
        cfs_no_mbm.append(cf_no / 1e6)
        disc_cfs_mbm.append(dcf_mbm / 1e6)
        disc_cfs_no_mbm.append(dcf_no / 1e6)

        cum_m += dcf_mbm
        cum_n += dcf_no
        cumulative_mbm.append(cum_m / 1e6)
        cumulative_no.append(cum_n / 1e6)

    npv_with_mbm  = sum(disc_cfs_mbm)    - capex_total / 1e6
    npv_no_mbm    = sum(disc_cfs_no_mbm) - capex_total / 1e6
    mbm_npv_delta = npv_with_mbm - npv_no_mbm

    # ── KPIs ──
    n1, n2, n3, n4 = st.columns(4)
    npv_disp = npv_with_mbm if include_mbm else npv_no_mbm
    color_npv = "#059669" if npv_disp >= 0 else "#dc2626"
    n1.markdown(kpi(f"${npv_disp:.1f}M",
                    "NPV" + (" (with MBM)" if include_mbm else " (no MBM)"),
                    "✅ Positive" if npv_disp >= 0 else "❌ Negative"), unsafe_allow_html=True)
    n2.markdown(kpi(f"${npv_with_mbm:.1f}M",  "NPV with MBM",  f"CAPEX {capex_total/1e6:.1f}M"), unsafe_allow_html=True)
    n3.markdown(kpi(f"${npv_no_mbm:.1f}M",    "NPV without MBM", f"Δ ${mbm_npv_delta:.1f}M"), unsafe_allow_html=True)
    n4.markdown(kpi(f"${mbm_npv_delta:.1f}M", "MBM NPV Uplift",
                    "Value added by MBM"), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Discounted Cash Flow Profile</div>', unsafe_allow_html=True)
    fn1, fn2 = st.columns(2)

    with fn1:
        fig_cf = go.Figure()
        fig_cf.add_trace(go.Bar(name="Annual CF (with MBM)", x=years, y=cfs_mbm,
                                marker_color="#059669", opacity=0.85))
        fig_cf.add_trace(go.Bar(name="Annual CF (no MBM)", x=years, y=cfs_no_mbm,
                                marker_color="#a7f3d0"))
        fig_cf.add_hline(y=0, line_color="#e2e8f0", line_width=1.5)
        fig_cf.update_layout(**pl(340))
        fig_cf.update_layout(barmode="overlay", xaxis_title="Year", yaxis_title="USD Million",
                              title=dict(text="Annual Cash Flows", font=dict(size=11, color=FC), y=0.98))
        st.plotly_chart(fig_cf, use_container_width=True)

    with fn2:
        fig_cum = go.Figure()
        fig_cum.add_trace(go.Scatter(name="Cumulative NPV (with MBM)", x=years, y=cumulative_mbm,
                                     line=dict(color="#059669", width=2.5), fill="tozeroy",
                                     fillcolor="rgba(5,150,105,0.08)"))
        fig_cum.add_trace(go.Scatter(name="Cumulative NPV (no MBM)", x=years, y=cumulative_no,
                                     line=dict(color="#6ee7b7", width=2, dash="dot")))
        fig_cum.add_hline(y=0, line_color="#dc2626", line_width=1.5, line_dash="dash",
                          annotation_text="Break-even", annotation_font_color="#dc2626",
                          annotation_font_size=9)
        fig_cum.update_layout(**pl(340))
        fig_cum.update_layout(xaxis_title="Year", yaxis_title="USD Million (NPV)",
                               title=dict(text="Cumulative NPV (incl. CAPEX)", font=dict(size=11, color=FC), y=0.98))
        st.plotly_chart(fig_cum, use_container_width=True)

    # ── MBM Forecast curves ──
    st.markdown('<div class="sec-head">MBM Price Forecast Assumptions</div>', unsafe_allow_html=True)
    mechs_active = ["ETS","Carbon Tax","VCM/CDM","CfD","CBAM","CORSIA","IMO Levy","AMC","Feebate"]
    mbm_base_vals = [p["ets"], p["ctax"], p["vcm"], p["cfd_strike"]-p["cfd_ref"],
                     p["cbam"], p["corsia"], p["imo"], p["amc"], p["feebate"]]

    fig_mbm_fcast = go.Figure()
    for mname, mbase in zip(mechs_active, mbm_base_vals):
        if mbase > 0:
            fcast_vals = [mbase * (1 + mbm_growth) ** yr for yr in range(1, lt + 1)]
            fig_mbm_fcast.add_trace(go.Scatter(
                name=mname, x=years, y=fcast_vals,
                mode="lines", line=dict(width=2)))
    fig_mbm_fcast.update_layout(**pl(300))
    fig_mbm_fcast.update_layout(xaxis_title="Year", yaxis_title="USD/tCO₂e or USD/MWh",
                                  title=dict(text=f"MBM Price Trajectories (growth: {mbm_growth*100:.1f}%/yr)",
                                             font=dict(size=11, color=FC), y=0.98))
    st.plotly_chart(fig_mbm_fcast, use_container_width=True)

    # ── Portfolio NPV table ──
    st.markdown('<div class="sec-head">Portfolio NPV Summary (All Technologies)</div>', unsafe_allow_html=True)
    npv_rows = []
    for i in range(14):
        lt_i  = ti["project_lifetime"][i]
        ck_i  = ti["installed_capacity"][i] * 1000
        cap_i = ck_i * ti["capex_per_kw"][i]
        dr_i  = AR[i]["dr"]
        mb_i  = AR[i]["mb"]
        op_i  = AR[i]["tc"] - AR[i]["ac"]
        w_i   = ti["wacc"][i]
        npv_m_i = -cap_i + sum((dr_i*(1+direct_growth)**(y-1) + mb_i*(1+mbm_growth)**(y-1)
                                 - op_i*(1+opex_inflation)**(y-1)) / (1+w_i)**y
                                for y in range(1, lt_i+1))
        npv_n_i = -cap_i + sum((dr_i*(1+direct_growth)**(y-1)
                                 - op_i*(1+opex_inflation)**(y-1)) / (1+w_i)**y
                                for y in range(1, lt_i+1))
        npv_rows.append({
            "Technology":       TECHNOLOGIES[i],
            "CAPEX ($M)":       round(cap_i/1e6, 1),
            "Lifetime (yr)":    lt_i,
            "WACC (%)":         round(w_i*100, 1),
            "NPV with MBM ($M)":round(npv_m_i/1e6, 1),
            "NPV no MBM ($M)":  round(npv_n_i/1e6, 1),
            "MBM Uplift ($M)":  round((npv_m_i - npv_n_i)/1e6, 1),
            "Viable (MBM)?":    "✅ Yes" if npv_m_i >= 0 else "❌ No",
            "Viable (no MBM)?": "✅ Yes" if npv_n_i >= 0 else "❌ No",
        })
    df_npv = pd.DataFrame(npv_rows)
    st.dataframe(df_npv.style.bar(
        subset=["NPV with MBM ($M)","NPV no MBM ($M)","MBM Uplift ($M)"], color="#bbf7d0", align="mid"),
        use_container_width=True, height=540)
    st.download_button("⬇ Download NPV CSV", df_npv.to_csv(index=False).encode(),
                       "npv_analysis.csv", "text/csv")


# ═════════════════════════════════════════════
# PAGE 7 — TECHNOLOGY CALCULATIONS
# ═════════════════════════════════════════════
elif page == "Tech Calculations":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Engineering Economics</div>
        <div class="page-header-title">🧮 Technology Calculations</div>
        <div class="page-header-sub">Core engineering and financial equations per technology — select a technology to explore</div>
    </div>''', unsafe_allow_html=True)

    sel_tc = st.selectbox("Select Technology", TECHNOLOGIES, index=0, key="tc_sel")
    t_tc   = TECHNOLOGIES.index(sel_tc)
    ti     = st.session_state.ti
    p      = st.session_state.p

    # ── Pull tech parameters ──
    o    = ti["annual_output"][t_tc]
    ck   = ti["installed_capacity"][t_tc] * 1000   # kW
    lt   = ti["project_lifetime"][t_tc]
    w    = ti["wacc"][t_tc]
    cap  = ck * ti["capex_per_kw"][t_tc]
    cf   = ti["capacity_factor"][t_tc]
    crf  = calc_crf(w, lt)
    ann_cap = cap * crf
    fo   = cap * ti["opex_pct"][t_tc]
    feedstock = ti["feedstock_cost"][t_tc]
    other_op  = ti["other_opex"][t_tc]
    co2  = o * ti["co2_abated_factor"][t_tc]
    lr   = ti["learning_rate"][t_tc]
    cum_now  = ti["cum_cap_now"][t_tc]
    cum_2035 = ti["cum_cap_2035"][t_tc]

    r_tc = compute(p, t_tc, ti)

    st.markdown('<div class="sec-head">📐 1. Capacity & Output Metrics</div>', unsafe_allow_html=True)
    tc1, tc2, tc3, tc4 = st.columns(4)
    tc1.markdown(kpi(f"{ck/1000:.1f} MW", "Installed Capacity", "Nameplate"), unsafe_allow_html=True)
    tc2.markdown(kpi(f"{cf*100:.1f}%", "Capacity Factor", "Utilisation"), unsafe_allow_html=True)
    theoretical_max = ck * 8760 / 1000  # MWh
    actual_out_mwh  = ck * cf * 8760 / 1000
    tc3.markdown(kpi(f"{actual_out_mwh:,.0f} MWh", "Theoretical Output/yr", f"CF × {theoretical_max:,.0f} MWh max"), unsafe_allow_html=True)
    tc4.markdown(kpi(f"{o:,.0f}", "Configured Output/yr", "MWh or units"), unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#f0fdf4;border:1px solid #d1fae5;border-radius:8px;padding:10px 14px;font-size:0.78rem;color:#374151;font-family:monospace;margin-bottom:8px;">
    Theoretical Annual Output = Installed Capacity (kW) × Capacity Factor × 8760 hrs<br>
    = {:.0f} kW × {:.2f} × 8,760  =  <b>{:,.0f} MWh/yr</b>
    </div>""".format(ck, cf, actual_out_mwh), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🏗️ 2. CAPEX & Annualisation</div>', unsafe_allow_html=True)
    cc1, cc2, cc3, cc4 = st.columns(4)
    cc1.markdown(kpi(f"${cap/1e6:.1f}M",     "Total CAPEX",        f"${ti['capex_per_kw'][t_tc]:,}/kW × {ck/1000:.0f} MW"), unsafe_allow_html=True)
    cc2.markdown(kpi(f"{w*100:.1f}%",         "WACC",               "Discount rate"), unsafe_allow_html=True)
    cc3.markdown(kpi(f"{crf:.4f}",            "Capital Recovery Factor", f"CRF = WACC(1+WACC)ᴺ / ((1+WACC)ᴺ−1)"), unsafe_allow_html=True)
    cc4.markdown(kpi(f"${ann_cap/1e6:.2f}M",  "Annualised CAPEX",   f"CAPEX × CRF"), unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#f0fdf4;border:1px solid #d1fae5;border-radius:8px;padding:10px 14px;font-size:0.78rem;color:#374151;font-family:monospace;margin-bottom:8px;">
    CRF = WACC × (1+WACC)ᴺ / [(1+WACC)ᴺ − 1]<br>
    = {:.3f} × (1+{:.3f})^{} / [(1+{:.3f})^{} − 1]  =  <b>{:.4f}</b><br><br>
    Annual CAPEX Charge = ${:.1f}M × {:.4f} = <b>${:.2f}M/yr</b>
    </div>""".format(w, w, lt, w, lt, crf, cap/1e6, crf, ann_cap/1e6), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">💸 3. Annual OPEX Breakdown</div>', unsafe_allow_html=True)
    op1, op2, op3, op4 = st.columns(4)
    total_opex = fo + feedstock + other_op
    op1.markdown(kpi(f"${fo/1e6:.2f}M",       "Fixed O&M",          f"{ti['opex_pct'][t_tc]*100:.1f}% of CAPEX/yr"), unsafe_allow_html=True)
    op2.markdown(kpi(f"${feedstock/1e6:.2f}M", "Feedstock Cost",     "Annual"), unsafe_allow_html=True)
    op3.markdown(kpi(f"${other_op/1e6:.2f}M",  "Other OPEX",         "Overheads etc."), unsafe_allow_html=True)
    op4.markdown(kpi(f"${total_opex/1e6:.2f}M","Total Annual OPEX",  "Excl. CAPEX charge"), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🌿 4. CO₂ Abatement & Carbon Value</div>', unsafe_allow_html=True)
    cv1, cv2, cv3, cv4 = st.columns(4)
    cv1.markdown(kpi(f"{co2/1e6:.3f} MtCO₂", "Annual Abatement",   f"{ti['co2_abated_factor'][t_tc]} tCO₂/unit"), unsafe_allow_html=True)
    cv2.markdown(kpi(f"${r_tc['bd'].get('ETS',0)/1e6:.2f}M",    "ETS Value",          f"@${p['ets']}/tCO₂e"), unsafe_allow_html=True)
    cv3.markdown(kpi(f"${r_tc['bd'].get('VCM/CDM',0)/1e6:.2f}M","VCM Value",          f"@${p['vcm']}/tCO₂e"), unsafe_allow_html=True)
    mac = (r_tc["tc"] - r_tc["dr"]) / co2 if co2 > 0 else 0
    cv4.markdown(kpi(f"${mac:.1f}/tCO₂",     "Marginal Abatement Cost", "Total cost net of direct rev"), unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#f0fdf4;border:1px solid #d1fae5;border-radius:8px;padding:10px 14px;font-size:0.78rem;color:#374151;font-family:monospace;margin-bottom:8px;">
    CO₂ Abated = Annual Output × CO₂ Factor  =  {:,.0f} × {:.2f}  =  <b>{:,.0f} tCO₂e/yr</b><br>
    Marginal Abatement Cost = (Total Cost − Direct Revenue) / CO₂ Abated<br>
    = (${:.1f}M − ${:.1f}M) / {:,.0f}t  =  <b>${:.1f}/tCO₂e</b>
    </div>""".format(o, ti["co2_abated_factor"][t_tc], co2,
                     r_tc["tc"]/1e6, r_tc["dr"]/1e6, co2, mac), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">📉 5. Learning Curve (Technology Cost Reduction)</div>', unsafe_allow_html=True)
    lcol1, lcol2 = st.columns([2, 1])
    with lcol1:
        cum_vals = np.logspace(np.log10(max(cum_now, 0.001)), np.log10(max(cum_2035, 0.01)), 50)
        lcost    = [ti["capex_per_kw"][t_tc] * (c / cum_now) ** (-lr / np.log2(2)) for c in cum_vals]
        fig_lc   = go.Figure()
        fig_lc.add_trace(go.Scatter(x=cum_vals, y=lcost, mode="lines",
                                    line=dict(color="#059669", width=2.5), name="CAPEX/kW"))
        fig_lc.add_vline(x=cum_now,  line_dash="dot", line_color="#6ee7b7",
                         annotation_text="Today", annotation_font_size=9)
        fig_lc.add_vline(x=cum_2035, line_dash="dot", line_color="#059669",
                         annotation_text="2035", annotation_font_size=9)
        fig_lc.update_layout(**pl(280))
        fig_lc.update_layout(xaxis_title="Cumulative Capacity (GW)", xaxis_type="log",
                              yaxis_title="CAPEX (USD/kW)",
                              title=dict(text=f"Wright's Law: Learning Rate {lr*100:.0f}%", font=dict(size=11, color=FC), y=0.98))
        st.plotly_chart(fig_lc, use_container_width=True)
    with lcol2:
        cost_2035 = ti["capex_per_kw"][t_tc] * (cum_2035 / max(cum_now, 0.001)) ** (-lr / np.log2(2))
        reduction = (1 - cost_2035 / ti["capex_per_kw"][t_tc]) * 100
        st.markdown(kpi(f"${ti['capex_per_kw'][t_tc]:,}/kW", "CAPEX Today"), unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(kpi(f"${cost_2035:,.0f}/kW", "CAPEX 2035 Est.", f"−{reduction:.0f}% reduction"), unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(kpi(f"{lr*100:.0f}%", "Learning Rate", "Per doubling of capacity"), unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#f0fdf4;border:1px solid #d1fae5;border-radius:8px;padding:10px 14px;font-size:0.78rem;color:#374151;font-family:monospace;">
    Wright's Law: Cost(C) = Cost(C₀) × (C / C₀)^(−b)   where b = Learning Rate / log(2)<br>
    CAPEX 2035 = ${:,}/kW × ({:.1f} / {:.3f})^(−{:.3f})  =  <b>${:,.0f}/kW</b>  (−{:.0f}%)
    </div>""".format(ti["capex_per_kw"][t_tc], cum_2035, max(cum_now, 0.001),
                     lr / np.log2(2), cost_2035, reduction), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">📊 6. Levelised Cost (LCOE / LCOX)</div>', unsafe_allow_html=True)
    lco1, lco2, lco3 = st.columns(3)
    total_annual_cost = ann_cap + fo + feedstock + other_op
    lcoe = total_annual_cost / o if o > 0 else 0
    lco_per_tco2 = total_annual_cost / co2 if co2 > 0 else 0
    lco1.markdown(kpi(f"${lcoe:.3f}/unit", "LCOE / Unit Cost", "Total cost / annual output"), unsafe_allow_html=True)
    lco2.markdown(kpi(f"${lco_per_tco2:.1f}/tCO₂", "LCOX (Cost/tCO₂)", "Total cost / CO₂ abated"), unsafe_allow_html=True)
    lco3.markdown(kpi(f"${r_tc['rc']:.2f}×", "Revenue / Cost Ratio", "R/C > 1 = viable"), unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#f0fdf4;border:1px solid #d1fae5;border-radius:8px;padding:10px 14px;font-size:0.78rem;color:#374151;font-family:monospace;">
    LCOE = (Ann. CAPEX + Fixed O&M + Feedstock + Other OPEX) / Annual Output<br>
    = (${:.2f}M + ${:.2f}M + ${:.2f}M + ${:.2f}M) / {:,.0f}  =  <b>${:.3f}/unit</b><br><br>
    LCOX (Abatement cost) = Total Cost / CO₂ Abated  =  ${:.1f}M / {:,.0f} t  =  <b>${:.1f}/tCO₂e</b>
    </div>""".format(ann_cap/1e6, fo/1e6, feedstock/1e6, other_op/1e6, o if o > 0 else 1,
                     lcoe, total_annual_cost/1e6, co2 if co2 > 0 else 1, lco_per_tco2), unsafe_allow_html=True)


# ═════════════════════════════════════════════
# PAGE 8 — SPATIAL VIABILITY
# ═════════════════════════════════════════════
elif page == "Spatial Viability":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Geospatial Analysis</div>
        <div class="page-header-title">🌍 Spatial Viability</div>
        <div class="page-header-sub">Technology viability across countries with jurisdiction-specific MBM regimes</div>
    </div>''', unsafe_allow_html=True)

    # ── Country MBM profiles (ETS price, Carbon Tax, VCM, CBAM applicability, IMO) ──
    # Columns: country, region, ets_price, ctax_price, vcm_price, cbam_applicable, imo_applicable, corsia_credit, feebate
    COUNTRY_MBM = {
        "EU":          {"region":"Europe",      "ets":85,  "ctax":0,   "vcm":80,  "cbam":1,"imo":1,"corsia":1,"feebate":0,"fuel":200},
        "UK":          {"region":"Europe",      "ets":75,  "ctax":20,  "vcm":75,  "cbam":0,"imo":1,"corsia":1,"feebate":0,"fuel":220},
        "Germany":     {"region":"Europe",      "ets":85,  "ctax":35,  "vcm":80,  "cbam":1,"imo":1,"corsia":1,"feebate":0,"fuel":240},
        "Norway":      {"region":"Europe",      "ets":85,  "ctax":60,  "vcm":90,  "cbam":1,"imo":1,"corsia":1,"feebate":0,"fuel":200},
        "Sweden":      {"region":"Europe",      "ets":85,  "ctax":130, "vcm":90,  "cbam":1,"imo":1,"corsia":1,"feebate":0,"fuel":200},
        "USA":         {"region":"Americas",    "ets":20,  "ctax":0,   "vcm":15,  "cbam":0,"imo":0,"corsia":0,"feebate":15,"fuel":180},
        "Canada":      {"region":"Americas",    "ets":50,  "ctax":65,  "vcm":20,  "cbam":0,"imo":0,"corsia":1,"feebate":5,"fuel":150},
        "Brazil":      {"region":"Americas",    "ets":0,   "ctax":10,  "vcm":8,   "cbam":0,"imo":0,"corsia":1,"feebate":0,"fuel":100},
        "Chile":       {"region":"Americas",    "ets":5,   "ctax":5,   "vcm":8,   "cbam":0,"imo":0,"corsia":0,"feebate":0,"fuel":80},
        "China":       {"region":"Asia-Pacific","ets":12,  "ctax":0,   "vcm":5,   "cbam":0,"imo":1,"corsia":0,"feebate":0,"fuel":100},
        "Japan":       {"region":"Asia-Pacific","ets":10,  "ctax":3,   "vcm":30,  "cbam":0,"imo":1,"corsia":1,"feebate":0,"fuel":250},
        "South Korea": {"region":"Asia-Pacific","ets":18,  "ctax":0,   "vcm":15,  "cbam":0,"imo":1,"corsia":1,"feebate":0,"fuel":200},
        "Australia":   {"region":"Asia-Pacific","ets":30,  "ctax":0,   "vcm":25,  "cbam":0,"imo":0,"corsia":1,"feebate":0,"fuel":160},
        "India":       {"region":"Asia-Pacific","ets":0,   "ctax":0,   "vcm":5,   "cbam":0,"imo":0,"corsia":1,"feebate":0,"fuel":80},
        "Indonesia":   {"region":"Asia-Pacific","ets":2,   "ctax":2,   "vcm":5,   "cbam":0,"imo":0,"corsia":1,"feebate":0,"fuel":60},
        "Singapore":   {"region":"Asia-Pacific","ets":25,  "ctax":25,  "vcm":20,  "cbam":0,"imo":1,"corsia":1,"feebate":0,"fuel":150},
        "Saudi Arabia":{"region":"Middle East", "ets":0,   "ctax":0,   "vcm":5,   "cbam":0,"imo":1,"corsia":0,"feebate":0,"fuel":50},
        "UAE":         {"region":"Middle East", "ets":0,   "ctax":0,   "vcm":8,   "cbam":0,"imo":1,"corsia":1,"feebate":0,"fuel":60},
        "South Africa":{"region":"Africa",      "ets":10,  "ctax":10,  "vcm":8,   "cbam":0,"imo":0,"corsia":1,"feebate":0,"fuel":70},
        "Kenya":       {"region":"Africa",      "ets":0,   "ctax":0,   "vcm":10,  "cbam":0,"imo":0,"corsia":1,"feebate":0,"fuel":50},
    }

    st.markdown('<div class="sec-head">Configuration</div>', unsafe_allow_html=True)
    sv1, sv2, sv3 = st.columns(3)
    with sv1:
        sel_sv  = st.selectbox("Technology to Deploy", TECHNOLOGIES, index=0, key="sv_sel")
        t_sv    = TECHNOLOGIES.index(sel_sv)
    with sv2:
        viab_metric = st.radio("Viability Metric", ["NPV ($M)", "Net CF ($M)", "R/C Ratio"], key="sv_metric")
    with sv3:
        mbm_growth_sv = st.slider("MBM Growth Rate (%/yr)", 0.0, 15.0, 5.0, 0.5, key="sv_mg") / 100
        show_regions  = st.multiselect("Filter Regions", ["Europe","Americas","Asia-Pacific","Middle East","Africa"],
                                        default=["Europe","Americas","Asia-Pacific","Middle East","Africa"], key="sv_region")

    ti = st.session_state.ti
    base_result_sv = compute(st.session_state.p, t_sv, ti)

    # ── Compute per-country ──
    sv_rows = []
    for country, cmbm in COUNTRY_MBM.items():
        if cmbm["region"] not in show_regions:
            continue

        # Build a country-specific price dict
        cp = dict(st.session_state.p)
        cp["ets"]  = cmbm["ets"]
        cp["ctax"] = cmbm["ctax"]
        cp["vcm"]  = cmbm["vcm"]
        cp["imo"]  = cmbm["imo"] * cp["imo"]
        cp["corsia"] = cmbm["corsia"] * cp["corsia"]
        cp["feebate"] = cmbm["feebate"] if cmbm["feebate"] > 0 else cp["feebate"]
        cp["fuel"] = cmbm["fuel"]

        # Override CBAM: only applicable in EU
        cbam_factor = cmbm["cbam"]
        ets_factor  = 1 if cmbm["ets"] > 0 else 0

        r_sv = compute(cp, t_sv, ti)

        # NPV for this country
        lt_sv = ti["project_lifetime"][t_sv]
        ck_sv = ti["installed_capacity"][t_sv] * 1000
        cap_sv = ck_sv * ti["capex_per_kw"][t_sv]
        w_sv   = ti["wacc"][t_sv]
        dr_sv  = r_sv["dr"]
        mb_sv  = r_sv["mb"]
        op_sv  = r_sv["tc"] - r_sv["ac"]
        npv_sv = -cap_sv + sum(
            (dr_sv + mb_sv * (1 + mbm_growth_sv)**(y-1) - op_sv) / (1 + w_sv)**y
            for y in range(1, lt_sv + 1))

        sv_rows.append({
            "Country":         country,
            "Region":          cmbm["region"],
            "ETS ($/tCO₂e)":   cmbm["ets"],
            "Carbon Tax":      cmbm["ctax"],
            "VCM ($/tCO₂e)":   cmbm["vcm"],
            "MBM Rev ($M)":    round(r_sv["mb"]/1e6, 2),
            "Direct Rev ($M)": round(r_sv["dr"]/1e6, 2),
            "Total Rev ($M)":  round(r_sv["tr"]/1e6, 2),
            "Total Cost ($M)": round(r_sv["tc"]/1e6, 2),
            "Net CF ($M)":     round(r_sv["nc"]/1e6, 2),
            "R/C Ratio":       round(r_sv["rc"], 2),
            "NPV ($M)":        round(npv_sv/1e6, 1),
            "Viable?":         "✅ Yes" if npv_sv >= 0 else "❌ No",
        })

    # Map radio label to exact DataFrame column
    _metric_col_map = {"NPV ($M)": "NPV ($M)", "Net CF ($M)": "Net CF ($M)", "R/C Ratio": "R/C Ratio"}
    _sort_col = _metric_col_map.get(viab_metric, "NPV ($M)")
    df_sv = pd.DataFrame(sv_rows).sort_values(_sort_col, ascending=False).reset_index(drop=True)

    # ── KPIs ──
    viable_count   = (df_sv["Viable?"] == "✅ Yes").sum()
    total_count    = len(df_sv)
    best_country   = df_sv.iloc[0]["Country"] if total_count > 0 else "N/A"
    best_val       = df_sv.iloc[0][viab_metric] if total_count > 0 else 0
    worst_country  = df_sv.iloc[-1]["Country"] if total_count > 0 else "N/A"
    worst_val      = df_sv.iloc[-1][viab_metric] if total_count > 0 else 0

    sv_k1, sv_k2, sv_k3, sv_k4 = st.columns(4)
    sv_k1.markdown(kpi(f"{viable_count}/{total_count}", "Viable Markets",
                        "NPV ≥ 0"), unsafe_allow_html=True)
    sv_k2.markdown(kpi(best_country, "Best Market",
                        f"{viab_metric}: {best_val}"), unsafe_allow_html=True)
    sv_k3.markdown(kpi(worst_country, "Weakest Market",
                        f"{viab_metric}: {worst_val}"), unsafe_allow_html=True)
    sv_k4.markdown(kpi(f"{viable_count/total_count*100:.0f}%" if total_count>0 else "N/A",
                        "Viability Rate", "Across analysed countries"), unsafe_allow_html=True)

    # ── Bar chart — metric by country ──
    st.markdown('<div class="sec-head">Country Viability Comparison</div>', unsafe_allow_html=True)
    metric_col = viab_metric
    colors_sv  = ["#059669" if v >= 0 else "#fca5a5" for v in df_sv[metric_col]]
    fig_sv = go.Figure(go.Bar(
        x=df_sv["Country"], y=df_sv[metric_col],
        marker_color=colors_sv,
        text=[f"{v:.1f}" for v in df_sv[metric_col]],
        textposition="outside", textfont=dict(size=8.5, color=FC),
    ))
    fig_sv.add_hline(y=0, line_color="#e2e8f0", line_width=1.5)
    fig_sv.update_layout(**pl(360, mb=80))
    fig_sv.update_layout(xaxis=dict(tickangle=-45), yaxis_title=viab_metric,
                          title=dict(text=f"{sel_sv} — {viab_metric} by Country",
                                     font=dict(size=11, color=FC), y=0.98))
    st.plotly_chart(fig_sv, use_container_width=True)

    # ── MBM revenue by country and mechanism ──
    st.markdown('<div class="sec-head">MBM Revenue Decomposition by Country</div>', unsafe_allow_html=True)
    countries_list = df_sv["Country"].tolist()
    mbm_rev_list   = df_sv["MBM Rev ($M)"].tolist()
    ets_vals, ctax_vals, vcm_vals, other_vals = [], [], [], []
    for country in countries_list:
        cmbm = COUNTRY_MBM[country]
        cp2  = dict(st.session_state.p)
        cp2["ets"] = cmbm["ets"]; cp2["ctax"] = cmbm["ctax"]; cp2["vcm"] = cmbm["vcm"]
        r2 = compute(cp2, t_sv, ti)
        ets_vals.append(r2["bd"].get("ETS", 0)/1e6)
        ctax_vals.append(r2["bd"].get("Carbon Tax", 0)/1e6)
        vcm_vals.append(r2["bd"].get("VCM/CDM", 0)/1e6)
        other_vals.append(max(0, r2["mb"]/1e6 - r2["bd"].get("ETS",0)/1e6
                               - r2["bd"].get("Carbon Tax",0)/1e6 - r2["bd"].get("VCM/CDM",0)/1e6))

    fig_mbm_country = go.Figure()
    fig_mbm_country.add_trace(go.Bar(name="ETS",        x=countries_list, y=ets_vals,  marker_color="#065f46"))
    fig_mbm_country.add_trace(go.Bar(name="Carbon Tax", x=countries_list, y=ctax_vals, marker_color="#059669"))
    fig_mbm_country.add_trace(go.Bar(name="VCM/CDM",    x=countries_list, y=vcm_vals,  marker_color="#34d399"))
    fig_mbm_country.add_trace(go.Bar(name="Other MBMs", x=countries_list, y=other_vals,marker_color="#a7f3d0"))
    fig_mbm_country.update_layout(**pl(340, mb=80))
    fig_mbm_country.update_layout(barmode="stack", xaxis=dict(tickangle=-45),
                                   yaxis_title="USD Million",
                                   title=dict(text="MBM Revenue Stack by Country",
                                              font=dict(size=11, color=FC), y=0.98))
    st.plotly_chart(fig_mbm_country, use_container_width=True)

    # ── Region heatmap ──
    st.markdown('<div class="sec-head">Carbon Price Heatmap by Country</div>', unsafe_allow_html=True)
    fig_heat = go.Figure(go.Heatmap(
        z=[[COUNTRY_MBM[c]["ets"], COUNTRY_MBM[c]["ctax"], COUNTRY_MBM[c]["vcm"]]
           for c in df_sv["Country"]],
        x=["ETS ($/tCO₂e)", "Carbon Tax ($/tCO₂e)", "VCM ($/tCO₂e)"],
        y=df_sv["Country"].tolist(),
        colorscale=[[0,"#f9fafb"],[0.01,"#d1fae5"],[1,"#059669"]],
        showscale=True,
        colorbar=dict(title=dict(text="USD/tCO₂e", font=dict(size=9)), tickfont=dict(size=9)),
        hovertemplate="<b>%{y}</b><br>%{x}: <b>$%{z}</b><extra></extra>",
    ))
    fig_heat.update_layout(**pl(480, ml=120, mr=60, mt=20, mb=30))
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Full data table ──
    st.markdown('<div class="sec-head">Full Country Data Table</div>', unsafe_allow_html=True)
    st.dataframe(df_sv.style.bar(
        subset=["NPV ($M)", "Net CF ($M)", "MBM Rev ($M)"], color="#bbf7d0", align="mid"),
        use_container_width=True, height=600)
    st.download_button("⬇ Download Spatial Viability CSV",
                       df_sv.to_csv(index=False).encode(),
                       "spatial_viability.csv", "text/csv")
