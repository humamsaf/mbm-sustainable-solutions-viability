import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="MBM Revenue Model",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# DESIGN SYSTEM — Middic-inspired dark navy
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── GLOBAL ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    min-width: 230px !important;
    max-width: 230px !important;
    background: #070d1a !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebarContent"] { padding: 0 !important; }

/* ── MAIN CONTENT ── */
.block-container {
    padding: 0 2rem 2rem 2rem !important;
    max-width: 100% !important;
}

/* ── NAV RADIO (hidden default, we use HTML buttons) ── */
div[data-testid="stRadio"] { display: none; }

/* ── PAGE TITLE ── */
.page-title {
    font-size: 1.45rem; font-weight: 700;
    color: #f0f6ff;
    padding: 28px 0 4px 0;
    letter-spacing: -0.02em;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 22px;
}
.page-sub {
    font-size: 0.8rem; color: #4d7aaa;
    margin-top: -18px; margin-bottom: 20px;
    font-weight: 400;
}

/* ── METRIC CARDS ── */
.card {
    background: #0d1b2e;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 20px 22px;
}
.card-value {
    font-size: 1.55rem; font-weight: 700;
    color: #e8f3ff; line-height: 1;
    margin-bottom: 6px; font-variant-numeric: tabular-nums;
}
.card-label {
    font-size: 0.68rem; font-weight: 600;
    color: #3d6a9e; text-transform: uppercase;
    letter-spacing: 0.08em;
}
.card-sub {
    font-size: 0.74rem; color: #1e6aba;
    margin-top: 4px;
}

/* ── SECTION HEADING ── */
.sec-head {
    font-size: 0.72rem; font-weight: 700;
    color: #2a7dd4; text-transform: uppercase;
    letter-spacing: 0.1em; margin: 24px 0 12px 0;
    display: flex; align-items: center; gap: 8px;
}
.sec-head::after {
    content: ''; flex: 1; height: 1px;
    background: rgba(255,255,255,0.06);
}

/* ── CHART CARD ── */
.chart-card {
    background: #0d1b2e;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px; padding: 20px 22px;
    margin-bottom: 12px;
}
.chart-title {
    font-size: 0.82rem; font-weight: 600;
    color: #c8dff4; margin-bottom: 2px;
}
.chart-sub {
    font-size: 0.72rem; color: #4d7aaa;
    margin-bottom: 12px;
}

/* ── MECHANISM CHIP ── */
.chip { display:inline-flex; align-items:center; gap:4px;
    padding:4px 11px; border-radius:99px; font-size:0.71rem;
    font-weight:600; margin:3px; }
.chip-on  { background:rgba(30,106,186,0.18); border:1px solid rgba(30,106,186,0.4); color:#5aaaee; }
.chip-off { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07); color:#2a4060; }

/* ── PROGRESS ── */
.prog-wrap { margin-bottom:8px; }
.prog-row { display:flex; justify-content:space-between;
    font-size:0.73rem; color:#4d7aaa; margin-bottom:3px; }
.prog-row b { color:#c8dff4; font-weight:600; }
.prog-bg { background:rgba(255,255,255,0.05); border-radius:4px; height:5px; }
.prog-fill { height:5px; border-radius:4px;
    background: linear-gradient(90deg,#0d4cac,#2a7dd4); }

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.06) !important; margin:16px 0 !important; }

/* ── SLIDERS / INPUTS ── */
.stSlider > div > div { padding-bottom:0 !important; }
.stSlider [data-testid="stSliderThumbValue"] { font-size:0.72rem !important; }
[data-testid="stMetric"] { 
    border-radius:10px !important;
    padding:16px 18px !important;
}

/* ── STREAMLIT TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap:0; border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    background:transparent !important;
}
.stTabs [data-baseweb="tab"] {
    background:transparent !important; font-size:0.8rem !important;
    color:#4d7aaa !important; padding:8px 18px !important;
    border-bottom:2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color:#c8dff4 !important;
    border-bottom:2px solid #2a7dd4 !important;
    font-weight:600 !important;
}

/* ── DATA TABLE ── */
[data-testid="stDataFrameResizable"] {
    border:1px solid rgba(255,255,255,0.07) !important;
    border-radius:10px !important;
}

/* ── SELECT / INPUT ── */
.stSelectbox [data-baseweb="select"] > div,
.stNumberInput > div > div > input {
    border-radius:8px !important;
    border-color:rgba(255,255,255,0.12) !important;
    font-size:0.82rem !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: #0d3d7a !important;
    color: #c8dff4 !important;
    border: 1px solid rgba(42,125,212,0.4) !important;
    border-radius:8px !important; font-size:0.8rem !important;
    font-weight:600 !important;
}
.stButton > button:hover {
    background: #1256a8 !important;
    border-color:rgba(42,125,212,0.7) !important;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS + DEFAULTS (unchanged)
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# PLOT THEME
# ─────────────────────────────────────────────
PBG  = "rgba(0,0,0,0)"
FC   = "#8ab4d4"
GC   = "rgba(255,255,255,0.05)"
BLUES= ["#0b2d54","#0d3d7a","#1256a8","#1a78f5","#2a9df4","#5bb8ff","#a0d4ff","#d0eaff"]

def pl_base(h=380, ml=24, mr=20, mt=16, mb=16):
    return dict(
        paper_bgcolor=PBG, plot_bgcolor=PBG,
        font=dict(family="Inter", color=FC, size=10),
        height=h, margin=dict(l=ml,r=mr,t=mt,b=mb),
        legend=dict(orientation="h", y=-0.18, font=dict(size=9)),
        xaxis=dict(gridcolor=GC, linecolor="rgba(255,255,255,0.05)", zeroline=False),
        yaxis=dict(gridcolor=GC, linecolor="rgba(255,255,255,0.05)", zeroline=False),
    )

# ─────────────────────────────────────────────
# CALCULATIONS
# ─────────────────────────────────────────────
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
    cb=co2*prices["cbam"]*0.85   if DEFAULTS["cbam"][t]   else 0
    co=co2*prices["corsia"]*1.05 if DEFAULTS["corsia"][t] else 0
    im=co2*prices["imo"]*0.95    if DEFAULTS["imo"][t]    else 0
    am=(o/1000)*prices["amc"]*0.5 if DEFAULTS["amc"][t]   else 0
    fb=co2*prices["feebate"]*0.5  if DEFAULTS["feebate"][t] else 0
    mb=e+cx+fu+cf+cb+co+im+v+am+fb
    tr=mb+dr
    return {"tc":tc,"ac":ac,"fo":fo,"co2":co2,"dr":dr,"mb":mb,"tr":tr,
            "nc":tr-tc,"lr":tr*lt,"rc":tr/tc if tc>0 else 0,
            "bd":{"ETS":e,"Carbon Tax":cx,"Fuel Mandate":fu,"CfD":cf,
                  "CBAM":cb,"CORSIA":co,"IMO Levy":im,"VCM/CDM":v,"AMC":am,"Feebate":fb}}

def fm(v): return f"${v/1e6:.1f}M"

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "ti"  not in st.session_state: st.session_state.ti = {k:list(v) for k,v in DEFAULTS.items()}
if "p"   not in st.session_state: st.session_state.p  = dict(DEFAULT_PRICES)
if "page" not in st.session_state: st.session_state.page = "Portfolio Overview"

# ─────────────────────────────────────────────
# SIDEBAR — Middic-style navigation
# ─────────────────────────────────────────────
NAV = [
    ("Portfolio Overview",  "📊"),
    ("Technology Detail",   "🔬"),
    ("Scenario Analysis",   "📈"),
    ("Data Table",          "🗂"),
    ("MBM Price Controls",  "⚙️"),
]

with st.sidebar:
    # Logo area
    st.markdown("""
    <div style="padding:22px 20px 16px 20px; border-bottom:1px solid rgba(255,255,255,0.06)">
        <div style="display:flex;align-items:center;gap:10px">
            <div style="width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,#0d3d7a,#1a78f5);
                        display:flex;align-items:center;justify-content:center;font-size:14px">⚡</div>
            <div>
                <div style="font-size:0.85rem;font-weight:700;color:#e8f3ff;letter-spacing:-0.01em">MBM Revenue</div>
                <div style="font-size:0.65rem;color:#2a5a8a;margin-top:1px">Model Dashboard</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:12px 12px 4px 12px; font-size:0.62rem;color:#1e4a6e;font-weight:700;text-transform:uppercase;letter-spacing:0.1em">Navigation</div>',
                unsafe_allow_html=True)

    for label, icon in NAV:
        active = st.session_state.page == label
        bg     = "rgba(26,120,245,0.12)" if active else "transparent"
        color  = "#5aaaee" if active else "#6a8fb0"
        border = "rgba(26,120,245,0.35)" if active else "transparent"
        lw     = "600" if active else "400"
        if st.sidebar.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.page = label
            st.rerun()

    # Divider + Reset
    st.markdown('<div style="position:absolute;bottom:20px;left:0;right:0;padding:0 12px">', unsafe_allow_html=True)
    st.markdown("---")
    if st.button("↺  Reset Defaults", use_container_width=True, key="reset_side"):
        st.session_state.p  = dict(DEFAULT_PRICES)
        st.session_state.ti = {k:list(v) for k,v in DEFAULTS.items()}
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PRE-COMPUTE
# ─────────────────────────────────────────────
AR  = [compute(st.session_state.p, i, st.session_state.ti) for i in range(14)]
TR  = sum(r["tr"] for r in AR)
TM  = sum(r["mb"] for r in AR)
TD  = sum(r["dr"] for r in AR)
TC  = sum(r["tc"] for r in AR)
TN  = sum(r["nc"] for r in AR)
TCO = sum(r["co2"] for r in AR)
page = st.session_state.page

# ─────────────────────────────────────────────
# helper: card html
# ─────────────────────────────────────────────
def card(val, label, sub=""):
    return f"""<div class="card">
        <div class="card-value">{val}</div>
        <div class="card-label">{label}</div>
        {"<div class='card-sub'>"+sub+"</div>" if sub else ""}
    </div>"""

def chart_card_open(title, sub=""):
    return f"""<div class="chart-card">
        <div class="chart-title">{title}</div>
        {"<div class='chart-sub'>"+sub+"</div>" if sub else ""}
    </div>"""

# ═══════════════════════════════════════════════
# PAGE 1 — PORTFOLIO OVERVIEW
# ═══════════════════════════════════════════════
if page == "Portfolio Overview":
    st.markdown('<div class="page-title">Portfolio Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Annual revenue performance across all 14 clean technology verticals</div>', unsafe_allow_html=True)

    # KPI row
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(card(fm(TR), "Total Annual Revenue", "Portfolio-wide"), unsafe_allow_html=True)
    c2.markdown(card(fm(TM), "MBM Revenue",          f"{TM/TR*100:.1f}% of total"), unsafe_allow_html=True)
    c3.markdown(card(fm(TD), "Direct Revenue",        f"{TD/TR*100:.1f}% of total"), unsafe_allow_html=True)
    c4.markdown(card(fm(TN), "Net Cash Flow",         f"R/C {TR/TC:.2f}×"), unsafe_allow_html=True)
    c5.markdown(card(f"{TCO/1e6:.2f}M tCO₂e", "CO₂ Abated", "per year"), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Revenue by Technology</div>', unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])

    with col_l:
        srt = sorted(range(14), key=lambda i: AR[i]["tr"], reverse=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="MBM Revenue", x=[TECH_SHORT[i] for i in srt],
            y=[AR[i]["mb"]/1e6 for i in srt], marker_color="#1256a8"))
        fig.add_trace(go.Bar(name="Direct Revenue", x=[TECH_SHORT[i] for i in srt],
            y=[AR[i]["dr"]/1e6 for i in srt], marker_color="#2a9df4"))
        fig.add_trace(go.Bar(name="Cost", x=[TECH_SHORT[i] for i in srt],
            y=[-AR[i]["tc"]/1e6 for i in srt], marker_color="#0b2d54"))
        fig.update_layout(**pl_base(380))
        fig.update_layout(barmode="relative",
            xaxis=dict(tickangle=-35,gridcolor=GC,linecolor="rgba(255,255,255,0.05)"),
            yaxis_title="USD Million")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        agg = {}
        for r in AR:
            for k,v in r["bd"].items(): agg[k]=agg.get(k,0)+v
        mf = {k:v for k,v in agg.items() if v>0}
        fig2 = go.Figure(go.Pie(
            labels=list(mf.keys()), values=list(mf.values()),
            hole=0.52, textinfo="label+percent",
            marker=dict(colors=BLUES[:len(mf)]),
            textfont=dict(size=9, color="#a0c8e8"),
        ))
        fig2.update_layout(**pl_base(380))
        fig2.update_layout(showlegend=False, title=dict(text="MBM Revenue Mix",
            font=dict(size=11,color="#8ab4d4"), y=0.97))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="sec-head">Net Annual Cash Flow</div>', unsafe_allow_html=True)
    nc_vals = [AR[i]["nc"]/1e6 for i in range(14)]
    fig3 = go.Figure(go.Bar(
        x=TECH_SHORT, y=nc_vals,
        marker_color=["#1a78f5" if v>=0 else "#0b2d54" for v in nc_vals],
        text=[f"${v:.1f}M" for v in nc_vals],
        textposition="outside", textfont=dict(size=9,color=FC),
    ))
    fig3.update_layout(**pl_base(280))
    fig3.update_layout(xaxis=dict(tickangle=-35,gridcolor=GC),yaxis_title="USD Million")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="sec-head">Technology Revenue Ranking</div>', unsafe_allow_html=True)
    srt2 = sorted(range(14), key=lambda i: AR[i]["tr"], reverse=True)
    mx   = AR[srt2[0]]["tr"]
    rc1, rc2 = st.columns(2)
    for rank, i in enumerate(srt2):
        pct = AR[i]["tr"]/mx*100
        col = rc1 if rank%2==0 else rc2
        col.markdown(f"""
        <div class="prog-wrap">
          <div class="prog-row"><span>{TECH_SHORT[i]}</span><b>{fm(AR[i]["tr"])}</b></div>
          <div class="prog-bg"><div class="prog-fill" style="width:{pct:.1f}%"></div></div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# PAGE 2 — TECHNOLOGY DETAIL
# ═══════════════════════════════════════════════
elif page == "Technology Detail":
    st.markdown('<div class="page-title">Technology Detail</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Configure individual technology parameters and view granular revenue breakdown</div>', unsafe_allow_html=True)

    sel = st.selectbox("Select Technology", TECHNOLOGIES, index=0)
    t   = TECHNOLOGIES.index(sel)
    ti  = st.session_state.ti

    st.markdown('<div class="sec-head">Technology Inputs</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("**Scale & Output**")
        ti["annual_output"][t]      = st.number_input("Annual Output (MWh/yr)", 0,10_000_000,int(ti["annual_output"][t]),10000, key=f"ao{t}")
        ti["installed_capacity"][t] = st.number_input("Installed Capacity (MW)", 0,5000,int(ti["installed_capacity"][t]),10, key=f"ic{t}")
        ti["capacity_factor"][t]    = st.slider("Capacity Factor",0.0,1.0,ti["capacity_factor"][t],0.01, key=f"cf{t}")
        ti["project_lifetime"][t]   = st.slider("Project Lifetime (yrs)",5,50,int(ti["project_lifetime"][t]),1, key=f"pl{t}")
    with c2:
        st.markdown("**Cost Structure**")
        ti["capex_per_kw"][t]   = st.number_input("CAPEX/kW (USD/kW)",0,20000,int(ti["capex_per_kw"][t]),100, key=f"ck{t}")
        ti["opex_pct"][t]       = st.slider("OPEX (% CAPEX p.a.)",0.0,0.20,ti["opex_pct"][t],0.005,format="%.3f", key=f"op{t}")
        ti["feedstock_cost"][t] = st.number_input("Feedstock Cost (USD/yr)",0,50_000_000,int(ti["feedstock_cost"][t]),100000, key=f"fc{t}")
        ti["other_opex"][t]     = st.number_input("Other OPEX (USD/yr)",0,20_000_000,int(ti["other_opex"][t]),100000, key=f"ov{t}")
        ti["wacc"][t]           = st.slider("WACC",0.01,0.25,ti["wacc"][t],0.005,format="%.3f", key=f"wc{t}")
    with c3:
        st.markdown("**Revenue Drivers**")
        ti["market_price"][t]      = st.number_input("Market Price (USD/unit)",0,100000,int(ti["market_price"][t]),10, key=f"mp{t}")
        ti["co2_abated_factor"][t] = st.slider("CO₂ Abated/Unit",0.0,2.0,ti["co2_abated_factor"][t],0.01, key=f"ca{t}")
        if t in [12,13]: ti["clients"][t] = st.number_input("Clients",0,10000,int(ti["clients"][t]),1, key=f"cl{t}")

    r = compute(st.session_state.p, t, ti)
    st.markdown('<div class="sec-head">Results</div>', unsafe_allow_html=True)
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.markdown(card(fm(r["tr"]),"Total Revenue"), unsafe_allow_html=True)
    m2.markdown(card(fm(r["mb"]),"MBM Revenue"), unsafe_allow_html=True)
    m3.markdown(card(fm(r["dr"]),"Direct Revenue"), unsafe_allow_html=True)
    m4.markdown(card(fm(r["tc"]),"Total Cost"), unsafe_allow_html=True)
    m5.markdown(card(fm(r["nc"]),"Net Cash Flow",f"R/C {r['rc']:.2f}×"), unsafe_allow_html=True)

    st.markdown("")
    ca,cb = st.columns(2)
    with ca:
        st.markdown('<div class="sec-head">MBM Revenue Breakdown</div>', unsafe_allow_html=True)
        bd = {k:v for k,v in r["bd"].items() if v>0}
        if bd:
            sb = sorted(bd.items(), key=lambda x:x[1], reverse=True)
            fig_b = go.Figure(go.Bar(
                x=[x[0] for x in sb], y=[x[1]/1e6 for x in sb],
                marker=dict(color=list(range(len(sb))),
                    colorscale=[[0,"#0b2d54"],[0.5,"#1256a8"],[1,"#5bb8ff"]]),
                text=[f"${x[1]/1e6:.2f}M" for x in sb],
                textposition="outside", textfont=dict(size=9,color=FC),
            ))
            fig_b.update_layout(**pl_base(300))
            fig_b.update_yaxes(title_text="USD Million")
            st.plotly_chart(fig_b, use_container_width=True)
        else:
            st.info("No active MBM mechanisms.")
    with cb:
        st.markdown('<div class="sec-head">Cost vs Revenue</div>', unsafe_allow_html=True)
        cats=["Direct Rev","MBM Rev","CAPEX ann.","Fixed OPEX","Feedstock","Other OPEX"]
        vals=[r["dr"]/1e6,r["mb"]/1e6,-r["ac"]/1e6,-r["fo"]/1e6,
              -ti["feedstock_cost"][t]/1e6,-ti["other_opex"][t]/1e6]
        fig_w=go.Figure(go.Bar(x=cats,y=vals,
            marker_color=["#2a9df4" if v>=0 else "#0b2d54" for v in vals],
            text=[f"${abs(v):.2f}M" for v in vals],
            textposition="outside",textfont=dict(size=9,color=FC)))
        fig_w.add_hline(y=0,line_color="rgba(255,255,255,0.15)",line_width=1)
        fig_w.update_layout(**pl_base(300))
        fig_w.update_layout(xaxis=dict(tickangle=-30))
        fig_w.update_yaxes(title_text="USD Million")
        st.plotly_chart(fig_w, use_container_width=True)

    st.markdown('<div class="sec-head">Active MBM Mechanisms</div>', unsafe_allow_html=True)
    mechs=["ets","ctax","fuel","cfd","cbam","corsia","imo","vcm","amc","feebate"]
    html=""
    for m in mechs:
        on=DEFAULTS[m][t]; lbl=MBM_LABELS[m][0]
        html+=f'<span class="chip {"chip-on" if on else "chip-off"}">{"✓" if on else "✕"} {lbl}</span>'
    st.markdown(html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# PAGE 3 — SCENARIO ANALYSIS
# ═══════════════════════════════════════════════
elif page == "Scenario Analysis":
    st.markdown('<div class="page-title">Scenario Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Stress-test portfolio revenue under varying carbon price assumptions</div>', unsafe_allow_html=True)

    bp = dict(st.session_state.p)
    er = list(range(10,310,10))
    tvs,mvs,nvs=[],[],[]
    for ep in er:
        tp={**bp,"ets":ep}
        res=[compute(tp,i,st.session_state.ti) for i in range(14)]
        tvs.append(sum(r["tr"] for r in res)/1e6)
        mvs.append(sum(r["mb"] for r in res)/1e6)
        nvs.append(sum(r["nc"] for r in res)/1e6)

    st.markdown('<div class="sec-head">ETS Carbon Price Sensitivity</div>', unsafe_allow_html=True)
    fs = make_subplots(rows=1,cols=2,subplot_titles=("Total Revenue & Net CF","MBM Revenue"))
    fs.add_trace(go.Scatter(x=er,y=tvs,name="Total Revenue",
        line=dict(color="#1a78f5",width=2.5)),row=1,col=1)
    fs.add_trace(go.Scatter(x=er,y=nvs,name="Net Cash Flow",
        line=dict(color="#5bb8ff",width=2,dash="dot")),row=1,col=1)
    fs.add_trace(go.Scatter(x=er,y=mvs,name="MBM Revenue",
        fill="tozeroy",fillcolor="rgba(18,86,168,0.15)",
        line=dict(color="#2a9df4",width=2)),row=1,col=2)
    for ci in [1,2]:
        fs.add_vline(x=bp["ets"],line_color="rgba(200,223,244,0.3)",line_dash="dash",row=1,col=ci)
    fs.update_layout(paper_bgcolor=PBG,plot_bgcolor=PBG,
        font=dict(family="Inter",color=FC,size=10),height=360,
        margin=dict(l=20,r=20,t=36,b=20),
        legend=dict(orientation="h",y=-0.15,font=dict(size=9)))
    for ax in ["xaxis","xaxis2"]:
        fs.update_layout(**{ax:dict(gridcolor=GC,title_text="ETS Price (USD/tCO₂e)",title_font=dict(size=9))})
    for ax in ["yaxis","yaxis2"]:
        fs.update_layout(**{ax:dict(gridcolor=GC,title_text="USD Million",title_font=dict(size=9))})
    st.plotly_chart(fs, use_container_width=True)

    st.markdown('<div class="sec-head">Multi-Scenario Comparison</div>', unsafe_allow_html=True)
    sc1,sc2 = st.columns(2)
    with sc1:
        el=st.slider("ETS Low",10,200,50,10); eb=st.slider("ETS Base",10,300,bp["ets"],10)
        eh=st.slider("ETS High",50,500,200,10)
    with sc2:
        vl=st.slider("VCM Low",5,100,30,5); vb=st.slider("VCM Base",5,300,bp["vcm"],5)
        vh=st.slider("VCM High",50,500,200,5)

    scens={"Low":{**bp,"ets":el,"vcm":vl},"Base":{**bp,"ets":eb,"vcm":vb},"High":{**bp,"ets":eh,"vcm":vh}}
    sr={}
    for sn,sp in scens.items():
        res=[compute(sp,i,st.session_state.ti) for i in range(14)]
        sr[sn]={"tr":sum(r["tr"] for r in res),"mb":sum(r["mb"] for r in res),"nc":sum(r["nc"] for r in res)}

    km1,km2,km3=st.columns(3)
    for col,sn in zip([km1,km2,km3],sr):
        col.markdown(card(fm(sr[sn]["tr"]),f"{sn} Scenario",
            f"MBM {fm(sr[sn]['mb'])}  ·  Net CF {fm(sr[sn]['nc'])}"), unsafe_allow_html=True)

    st.markdown("")
    fsc=go.Figure()
    for m,lbl,clr in [("tr","Total Revenue","#1a78f5"),("mb","MBM Revenue","#0d3d7a"),("nc","Net Cash Flow","#2a9df4")]:
        fsc.add_trace(go.Bar(name=lbl,x=list(sr.keys()),
            y=[sr[s][m]/1e6 for s in sr],marker_color=clr))
    fsc.update_layout(**pl_base(320))
    fsc.update_layout(barmode="group")
    fsc.update_yaxes(title_text="USD Million")
    st.plotly_chart(fsc, use_container_width=True)

# ═══════════════════════════════════════════════
# PAGE 4 — DATA TABLE
# ═══════════════════════════════════════════════
elif page == "Data Table":
    st.markdown('<div class="page-title">Data Table</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Full revenue summary and MBM mechanism applicability across all technologies</div>', unsafe_allow_html=True)

    t1,t2,t3 = st.tabs(["Revenue Summary","MBM Breakdown","Applicability Heatmap"])

    with t1:
        rows=[]
        for i,r in enumerate(AR):
            rows.append({"Technology":TECHNOLOGIES[i],
                "Direct Rev ($M)":round(r["dr"]/1e6,2),"MBM Rev ($M)":round(r["mb"]/1e6,2),
                "Total Rev ($M)":round(r["tr"]/1e6,2),"Total Cost ($M)":round(r["tc"]/1e6,2),
                "Net CF ($M)":round(r["nc"]/1e6,2),"R/C Ratio":round(r["rc"],2),
                "CO₂ Abated (Mt)":round(r["co2"]/1e6,3),"Lifetime Rev ($M)":round(r["lr"]/1e6,1)})
        df=pd.DataFrame(rows)
        st.dataframe(df.style.background_gradient(subset=["Total Rev ($M)","Net CF ($M)"],cmap="Blues"),
                     use_container_width=True, height=500)
        st.download_button("⬇ Download CSV", df.to_csv(index=False).encode(), "revenue.csv","text/csv")

    with t2:
        mbrows=[]
        for i,r in enumerate(AR):
            row={"Technology":TECH_SHORT[i]}
            for k,v in r["bd"].items(): row[f"{k} ($M)"]=round(v/1e6,2)
            row["Total MBM ($M)"]=round(r["mb"]/1e6,2)
            mbrows.append(row)
        dfm=pd.DataFrame(mbrows)
        st.dataframe(dfm.style.background_gradient(subset=["Total MBM ($M)"],cmap="Blues"),
                     use_container_width=True, height=500)
        st.download_button("⬇ Download CSV", dfm.to_csv(index=False).encode(),"mbm.csv","text/csv")

    with t3:
        mechs=["ets","ctax","fuel","cfd","cbam","corsia","imo","vcm","amc","feebate"]
        mlbl=[MBM_LABELS[m][0] for m in mechs]
        # Count per mechanism per tech (sum of relevant prices weighted by applicability)
        z_counts=[]
        for i in range(14):
            row=[]
            for m in mechs:
                if DEFAULTS[m][i]:
                    pkey=m if m in st.session_state.p else ("cfd_strike" if m=="cfd" else m)
                    row.append(st.session_state.p.get(pkey,0)/100)  # normalise
                else:
                    row.append(0)
            z_counts.append(row)

        z_bin=[[DEFAULTS[m][i] for m in mechs] for i in range(14)]
        fig_hm=go.Figure(go.Heatmap(
            z=z_bin, x=mlbl, y=TECH_SHORT,
            colorscale=[[0,"#070d1a"],[0.01,"#0b2d54"],[1,"#1a78f5"]],
            showscale=True,
            colorbar=dict(title="Active",tickvals=[0,1],ticktext=["No","Yes"],
                tickfont=dict(size=9,color=FC),titlefont=dict(size=9,color=FC),
                bgcolor="rgba(0,0,0,0)",bordercolor="rgba(255,255,255,0.1)"),
            hoverongaps=False,
            hovertemplate="<b>%{y}</b> × <b>%{x}</b><br>Active: %{z}<extra></extra>",
        ))
        # Add text annotations
        for i in range(14):
            for j,m in enumerate(mechs):
                if z_bin[i][j]:
                    fig_hm.add_annotation(x=mlbl[j],y=TECH_SHORT[i],text="✓",
                        showarrow=False,font=dict(size=12,color="#5bb8ff"))
        fig_hm.update_layout(**pl_base(520,ml=90,mr=40,mt=20,mb=100))
        fig_hm.update_layout(xaxis=dict(tickangle=-40,side="bottom"))
        st.markdown('<div class="chart-title">Technology × MBM Mechanism Applicability</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-sub">Which market-based mechanisms apply to each technology</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_hm, use_container_width=True)

# ═══════════════════════════════════════════════
# PAGE 5 — MBM PRICE CONTROLS
# ═══════════════════════════════════════════════
elif page == "MBM Price Controls":
    st.markdown('<div class="page-title">MBM Price Controls</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Adjust all market-based mechanism parameters — changes apply instantly across all pages</div>', unsafe_allow_html=True)

    p = st.session_state.p

    st.markdown('<div class="sec-head">Carbon Pricing</div>', unsafe_allow_html=True)
    pc1,pc2,pc3 = st.columns(3)
    with pc1:
        p["ets"]    = st.slider("ETS / Carbon Market (USD/tCO₂e)",10,300,p["ets"],5,key="mb_ets")
        p["ctax"]   = st.slider("Carbon Tax (USD/tCO₂e)",0,200,p["ctax"],5,key="mb_ctax")
        p["corsia"] = st.slider("CORSIA Credit (USD/tCO₂e)",3,100,int(p["corsia"]),1,key="mb_corsia")
    with pc2:
        p["vcm"]    = st.slider("VCM / CDM Credit (USD/tCO₂e)",5,300,p["vcm"],5,key="mb_vcm")
        p["cbam"]   = st.slider("CBAM Import Cost (USD/tCO₂e)",10,150,p["cbam"],5,key="mb_cbam")
        p["imo"]    = st.slider("IMO Levy (USD/tCO₂e)",50,800,p["imo"],10,key="mb_imo")
    with pc3:
        p["feebate"] = st.slider("Feebate Rate (USD/tCO₂e)",0,150,p["feebate"],5,key="mb_feebate")
        p["amc"]     = st.slider("AMC Price (USD/unit)",50,300,p["amc"],10,key="mb_amc")

    st.markdown('<div class="sec-head">Energy & Policy Prices</div>', unsafe_allow_html=True)
    pe1,pe2,pe3 = st.columns(3)
    with pe1:
        p["cfd_strike"] = st.slider("CfD Strike Price (USD/MWh)",50,300,p["cfd_strike"],5,key="mb_cfd_s")
        p["cfd_ref"]    = st.slider("CfD Market Reference (USD/MWh)",30,200,p["cfd_ref"],5,key="mb_cfd_r")
    with pe2:
        p["fuel"] = st.slider("Fuel Mandate Offtake (USD/MWh)",100,600,p["fuel"],10,key="mb_fuel")

    st.markdown('<div class="sec-head">Commodity Prices</div>', unsafe_allow_html=True)
    pco1,pco2,pco3 = st.columns(3)
    with pco1: p["electricity"]=st.slider("Grid Electricity (USD/MWh)",20,200,p["electricity"],5,key="mb_elec")
    with pco2: p["gas"]        =st.slider("Natural Gas (USD/MMBtu)",2,30,p["gas"],1,key="mb_gas")
    with pco3: p["biomass"]    =st.slider("Biomass / Feedstock (USD/MWh)",10,120,p["biomass"],5,key="mb_bio")

    st.session_state.p = p

    st.markdown('<div class="sec-head">Current Price Summary</div>', unsafe_allow_html=True)
    items=[
        ("ETS / Carbon Market",p["ets"],"USD/tCO₂e"),("Carbon Tax",p["ctax"],"USD/tCO₂e"),
        ("VCM / CDM Credit",p["vcm"],"USD/tCO₂e"),("CBAM Import",p["cbam"],"USD/tCO₂e"),
        ("CORSIA Credit",p["corsia"],"USD/tCO₂e"),("IMO Levy",p["imo"],"USD/tCO₂e"),
        ("Feebate",p["feebate"],"USD/tCO₂e"),("CfD Strike",p["cfd_strike"],"USD/MWh"),
        ("CfD Reference",p["cfd_ref"],"USD/MWh"),("Fuel Mandate",p["fuel"],"USD/MWh"),
        ("AMC Price",p["amc"],"USD/unit"),("Grid Electricity",p["electricity"],"USD/MWh"),
        ("Natural Gas",p["gas"],"USD/MMBtu"),("Biomass/Feedstock",p["biomass"],"USD/MWh"),
    ]
    cols=st.columns(4)
    for idx,(lbl,val,unit) in enumerate(items):
        cols[idx%4].markdown(card(val,lbl,unit), unsafe_allow_html=True)

    st.markdown("")
    rb1,_,_ = st.columns([1,1,4])
    with rb1:
        if st.button("↺  Reset to Defaults",use_container_width=True,key="rst_mbm"):
            st.session_state.p  = dict(DEFAULT_PRICES)
            st.session_state.ti = {k:list(v) for k,v in DEFAULTS.items()}
            st.rerun()
