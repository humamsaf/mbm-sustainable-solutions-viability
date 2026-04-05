import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Technology Innovation Revenue Model",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 1.5rem; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252a3d);
        border: 1px solid #2d3555;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 6px 0;
    }
    .metric-value { font-size: 1.5rem; font-weight: 700; color: #4ade80; }
    .metric-label { font-size: 0.78rem; color: #9ca3af; margin-bottom: 2px; }
    .section-header {
        font-size: 1.05rem; font-weight: 700;
        color: #60a5fa; margin: 18px 0 8px 0;
        border-left: 3px solid #3b82f6; padding-left: 10px;
    }
    .stSlider > div { padding-bottom: 4px; }
    div[data-testid="stMetricValue"] { font-size: 1.4rem !important; }
    .tag-positive { background: #14532d; color: #4ade80; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; }
    .tag-negative { background: #7f1d1d; color: #f87171; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
TECHNOLOGIES = [
    "Solar PV & Wind Energy",
    "Green Hydrogen",
    "SAF (Sust. Aviation Fuel)",
    "CCUS",
    "Battery Storage & EVs",
    "Low-carbon Steel & Cement",
    "Ammonia (green/blue)",
    "Methanol (green/e-methanol)",
    "Reforestation / REDD+ / NBS",
    "Blue Carbon (mangroves)",
    "Direct Air Capture (DAC)",
    "Building Energy Efficiency",
    "Carbon Offsetting / MRV Tech",
    "Energy Mgmt & Analytics",
]

TECH_SHORT = [
    "Solar/Wind", "Green H₂", "SAF", "CCUS",
    "Battery/EV", "Steel/Cement", "Ammonia", "Methanol",
    "Reforestation", "Blue Carbon", "DAC", "Bldg Eff.",
    "MRV Tech", "Energy Mgmt"
]

# Default tech inputs (from Excel Sheet: 2. Tech Inputs)
DEFAULTS = {
    "annual_output":      [500000, 50000, 150000, 100000, 300000, 250000, 180000, 120000, 80000, 30000, 50000, 400000, 0, 0],
    "installed_capacity": [200, 100, 80, 50, 150, 50, 80, 60, 0, 0, 25, 0, 10, 5],
    "capacity_factor":    [0.30, 0.45, 0.85, 0.90, 0.25, 0.90, 0.90, 0.90, 1.0, 1.0, 0.95, 1.0, 0.90, 0.95],
    "project_lifetime":   [25, 20, 20, 30, 15, 25, 25, 20, 30, 30, 20, 20, 15, 10],
    "capex_per_kw":       [1200, 2500, 3000, 4000, 1800, 5000, 3500, 3200, 500, 300, 150, 800, 400, 200],
    "opex_pct":           [0.015, 0.025, 0.030, 0.035, 0.020, 0.040, 0.030, 0.030, 0.10, 0.12, 0.05, 0.05, 0.08, 0.10],
    "feedstock_cost":     [0, 8e6, 6e6, 2e6, 1e6, 5e6, 4e6, 3e6, 5e5, 2e5, 3e6, 0, 0, 0],
    "other_opex":         [5e5, 2e6, 1.5e6, 1e6, 8e5, 2e6, 1.5e6, 1.2e6, 3e5, 1e5, 2e6, 1e6, 5e5, 8e5],
    "wacc":               [0.07, 0.09, 0.10, 0.10, 0.08, 0.10, 0.09, 0.09, 0.06, 0.06, 0.10, 0.07, 0.08, 0.08],
    "market_price":       [70, 4500, 2800, 80, 90, 700, 950, 1300, 12, 30, 500, 100, 50000, 25000],
    "clients":            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 20],
    "co2_abated_factor":  [0.45, 0.90, 0.70, 0.85, 0.30, 0.80, 0.85, 0.75, 1.0, 1.0, 1.0, 0.40, 0.95, 0.35],
    "learning_rate":      [0.20, 0.18, 0.12, 0.08, 0.22, 0.06, 0.10, 0.10, 0.05, 0.04, 0.15, 0.08, 0.10, 0.12],
    "cum_cap_now":        [2000, 0.5, 0.05, 0.03, 1500, 0.1, 0.02, 0.01, 500, 10, 0.001, 5000, 100, 200],
    "cum_cap_2035":       [8000, 10, 0.5, 0.5, 5000, 2, 0.5, 0.2, 1000, 50, 1, 8000, 500, 1000],
    # MBM applicability (1=yes, 0=no)
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
    "ets":     ("ETS / Carbon Market", "USD/tCO₂e"),
    "ctax":    ("Carbon Tax", "USD/tCO₂e"),
    "fuel":    ("Fuel Mandate", "USD/MWh"),
    "cfd":     ("CfD / CCfD", "USD/MWh"),
    "cbam":    ("CBAM Import", "USD/tCO₂e"),
    "corsia":  ("CORSIA Credit", "USD/tCO₂e"),
    "imo":     ("IMO Levy", "USD/tCO₂e"),
    "vcm":     ("VCM / CDM Credit", "USD/tCO₂e"),
    "amc":     ("AMC", "USD/unit"),
    "feebate": ("Feebate", "USD/tCO₂e"),
}

DEFAULT_PRICES = {
    "ets": 100, "ctax": 50, "fuel": 240, "cfd_strike": 120, "cfd_ref": 80,
    "cbam": 55, "corsia": 22.25, "imo": 380, "vcm": 100, "amc": 100,
    "feebate": 50, "electricity": 60, "gas": 8, "biomass": 40
}

# ─────────────────────────────────────────────
# CALCULATION ENGINE
# ─────────────────────────────────────────────
def calc_crf(wacc, lifetime):
    if wacc == 0:
        return 1 / lifetime
    return (wacc * (1 + wacc)**lifetime) / ((1 + wacc)**lifetime - 1)

def compute_revenues(prices, tech_idx, tech_inputs):
    t = tech_idx
    output     = tech_inputs["annual_output"][t]
    cap_kw     = tech_inputs["installed_capacity"][t] * 1000  # MW → kW
    lifetime   = tech_inputs["project_lifetime"][t]
    wacc       = tech_inputs["wacc"][t]
    capex_kw   = tech_inputs["capex_per_kw"][t]
    opex_pct   = tech_inputs["opex_pct"][t]
    feedstock  = tech_inputs["feedstock_cost"][t]
    other_opex = tech_inputs["other_opex"][t]
    mkt_price  = tech_inputs["market_price"][t]
    co2_factor = tech_inputs["co2_abated_factor"][t]
    clients    = tech_inputs["clients"][t]

    # Costs
    capex_total = capex_kw * cap_kw
    crf = calc_crf(wacc, lifetime)
    ann_capex = capex_total * crf
    fixed_opex = capex_total * opex_pct
    total_cost = ann_capex + fixed_opex + feedstock + other_opex

    # CO₂ abated
    co2_abated = output * co2_factor

    # Direct product revenue
    if t in [12, 13]:  # MRV Tech and Energy Mgmt use client model
        direct_rev = clients * mkt_price
    else:
        direct_rev = output * mkt_price

    # MBM Revenues
    ets_rev    = co2_abated * prices["ets"]    if DEFAULTS["ets"][t]     else 0
    ctax_rev   = co2_abated * prices["ctax"]   if DEFAULTS["ctax"][t]    else 0
    vcm_rev    = co2_abated * prices["vcm"]    if DEFAULTS["vcm"][t]     else 0

    # Fuel mandate
    fuel_rev = 0
    if DEFAULTS["fuel"][t] and output > 0:
        blend = tech_inputs["capacity_factor"][t]
        fuel_rev = output * blend * prices["fuel"] * 0.85

    # CfD
    cfd_rev = 0
    if DEFAULTS["cfd"][t] and output > 0:
        cfd_diff = max(0, prices["cfd_strike"] - prices["cfd_ref"])
        cfd_rev = output * cfd_diff * 0.5

    # CBAM
    cbam_rev = 0
    if DEFAULTS["cbam"][t]:
        cbam_rev = co2_abated * prices["cbam"] * 0.85

    # CORSIA
    corsia_rev = 0
    if DEFAULTS["corsia"][t]:
        corsia_rev = co2_abated * prices["corsia"] * 1.05

    # IMO levy
    imo_rev = 0
    if DEFAULTS["imo"][t]:
        imo_rev = co2_abated * prices["imo"] * 0.95

    # AMC
    amc_rev = 0
    if DEFAULTS["amc"][t]:
        amc_rev = (output / 1000) * prices["amc"] * 0.5

    # Feebate
    feebate_rev = 0
    if DEFAULTS["feebate"][t]:
        feebate_rev = co2_abated * prices["feebate"] * 0.5

    mbm_total = ets_rev + ctax_rev + fuel_rev + cfd_rev + cbam_rev + corsia_rev + imo_rev + vcm_rev + amc_rev + feebate_rev
    total_rev = mbm_total + direct_rev
    net_cf = total_rev - total_cost
    lifetime_rev = total_rev * lifetime

    mbm_breakdown = {
        "ETS": ets_rev, "Carbon Tax": ctax_rev, "Fuel Mandate": fuel_rev,
        "CfD": cfd_rev, "CBAM": cbam_rev, "CORSIA": corsia_rev,
        "IMO Levy": imo_rev, "VCM/CDM": vcm_rev, "AMC": amc_rev, "Feebate": feebate_rev
    }

    return {
        "capex_total": capex_total, "ann_capex": ann_capex,
        "fixed_opex": fixed_opex, "total_cost": total_cost,
        "co2_abated": co2_abated, "direct_rev": direct_rev,
        "mbm_total": mbm_total, "total_rev": total_rev,
        "net_cf": net_cf, "lifetime_rev": lifetime_rev,
        "mbm_breakdown": mbm_breakdown,
        "rev_cost_ratio": total_rev / total_cost if total_cost > 0 else 0,
    }

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    if "tech_inputs" not in st.session_state:
        st.session_state.tech_inputs = {k: list(v) for k, v in DEFAULTS.items()}
    if "prices" not in st.session_state:
        st.session_state.prices = dict(DEFAULT_PRICES)

init_state()

# ─────────────────────────────────────────────
# SIDEBAR — Global MBM Prices
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌐 Global MBM Prices")
    st.caption("Market-Based Mechanism intervention parameters")

    p = st.session_state.prices

    st.markdown('<div class="section-header">Carbon Pricing</div>', unsafe_allow_html=True)
    p["ets"]    = st.slider("ETS / Carbon Market Price (USD/tCO₂e)", 10, 300, p["ets"], 5)
    p["ctax"]   = st.slider("Carbon Tax Rate (USD/tCO₂e)", 0, 200, p["ctax"], 5)
    p["vcm"]    = st.slider("VCM / CDM Credit Price (USD/tCO₂e)", 5, 300, p["vcm"], 5)
    p["cbam"]   = st.slider("CBAM Import Carbon Cost (USD/tCO₂e)", 10, 150, p["cbam"], 5)
    p["corsia"] = st.slider("CORSIA Credit Price (USD/tCO₂e)", 3, 100, int(p["corsia"]), 1)
    p["imo"]    = st.slider("IMO Levy Rate (USD/tCO₂e)", 50, 800, p["imo"], 10)
    p["feebate"]= st.slider("Feebate Rate (USD/tCO₂e)", 0, 150, p["feebate"], 5)

    st.markdown('<div class="section-header">Energy & Policy Prices</div>', unsafe_allow_html=True)
    p["cfd_strike"] = st.slider("CfD Strike Price (USD/MWh)", 50, 300, p["cfd_strike"], 5)
    p["cfd_ref"]    = st.slider("CfD Market Reference Price (USD/MWh)", 30, 200, p["cfd_ref"], 5)
    p["fuel"]       = st.slider("Fuel Mandate Offtake Price (USD/MWh)", 100, 600, p["fuel"], 10)
    p["amc"]        = st.slider("AMC Price (USD/unit)", 50, 300, p["amc"], 10)

    st.markdown('<div class="section-header">Commodity Prices</div>', unsafe_allow_html=True)
    p["electricity"] = st.slider("Grid Electricity Price (USD/MWh)", 20, 200, p["electricity"], 5)
    p["gas"]         = st.slider("Natural Gas Price (USD/MMBtu)", 2, 30, p["gas"], 1)
    p["biomass"]     = st.slider("Biomass / Feedstock Price (USD/MWh)", 10, 120, p["biomass"], 5)

    st.session_state.prices = p

    st.divider()
    if st.button("🔄 Reset All to Defaults", use_container_width=True):
        st.session_state.prices = dict(DEFAULT_PRICES)
        st.session_state.tech_inputs = {k: list(v) for k, v in DEFAULTS.items()}
        st.rerun()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("# 🌱 Technology Innovation Revenue Model")
st.markdown("**Market-Based Mechanism (MBM) Intervention — Revenue Estimation**")
st.divider()

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Portfolio Overview", "🔬 Technology Detail", "📈 Scenario Analysis", "🗂️ Data Table"])

# ─────────────────────────────────────────────
# TAB 1 — PORTFOLIO OVERVIEW
# ─────────────────────────────────────────────
with tab1:
    all_results = [compute_revenues(st.session_state.prices, i, st.session_state.tech_inputs) for i in range(14)]

    total_rev    = sum(r["total_rev"]    for r in all_results)
    total_mbm    = sum(r["mbm_total"]    for r in all_results)
    total_direct = sum(r["direct_rev"]   for r in all_results)
    total_cost   = sum(r["total_cost"]   for r in all_results)
    total_netcf  = sum(r["net_cf"]       for r in all_results)
    total_co2    = sum(r["co2_abated"]   for r in all_results)

    def fmt_m(v): return f"${v/1e6:.1f}M"
    def fmt_b(v): return f"${v/1e9:.2f}B"

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("Total Annual Revenue", fmt_m(total_rev))
    with c2: st.metric("MBM Revenue", fmt_m(total_mbm), f"{total_mbm/total_rev*100:.1f}%")
    with c3: st.metric("Net Cash Flow", fmt_m(total_netcf))
    with c4: st.metric("Total Annual Cost", fmt_m(total_cost))
    with c5: st.metric("CO₂ Abated", f"{total_co2/1e6:.2f}M tCO₂e/yr")

    st.divider()
    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown("#### Revenue by Technology (Annual)")
        techs_sorted = sorted(range(14), key=lambda i: all_results[i]["total_rev"], reverse=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="MBM Revenue",
            x=[TECH_SHORT[i] for i in techs_sorted],
            y=[all_results[i]["mbm_total"]/1e6 for i in techs_sorted],
            marker_color="#3b82f6",
        ))
        fig.add_trace(go.Bar(
            name="Direct Revenue",
            x=[TECH_SHORT[i] for i in techs_sorted],
            y=[all_results[i]["direct_rev"]/1e6 for i in techs_sorted],
            marker_color="#10b981",
        ))
        fig.add_trace(go.Bar(
            name="Total Cost",
            x=[TECH_SHORT[i] for i in techs_sorted],
            y=[-all_results[i]["total_cost"]/1e6 for i in techs_sorted],
            marker_color="#ef4444",
        ))
        fig.update_layout(
            barmode="relative", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e5e7eb"), legend=dict(orientation="h", y=-0.22),
            yaxis_title="USD Million", height=380,
            xaxis=dict(tickangle=-35),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### MBM Revenue Mix (Portfolio)")
        mbm_agg = {}
        for r in all_results:
            for k, v in r["mbm_breakdown"].items():
                mbm_agg[k] = mbm_agg.get(k, 0) + v
        mbm_filtered = {k: v for k, v in mbm_agg.items() if v > 0}
        fig2 = go.Figure(go.Pie(
            labels=list(mbm_filtered.keys()),
            values=list(mbm_filtered.values()),
            hole=0.45,
            textinfo="label+percent",
            marker=dict(colors=px.colors.qualitative.Set2),
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e5e7eb"),
            legend=dict(orientation="v", x=1.05), height=380, showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Net Cash Flow bars
    st.markdown("#### Net Annual Cash Flow by Technology")
    colors = ["#10b981" if all_results[i]["net_cf"] >= 0 else "#ef4444" for i in range(14)]
    fig3 = go.Figure(go.Bar(
        x=TECH_SHORT, y=[all_results[i]["net_cf"]/1e6 for i in range(14)],
        marker_color=colors, text=[f"${all_results[i]['net_cf']/1e6:.1f}M" for i in range(14)],
        textposition="outside",
    ))
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"), yaxis_title="USD Million", height=300,
        xaxis=dict(tickangle=-35),
    )
    st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 2 — TECHNOLOGY DETAIL
# ─────────────────────────────────────────────
with tab2:
    st.markdown("#### Select Technology to Configure & Analyze")
    selected = st.selectbox("Technology", TECHNOLOGIES, index=0)
    t = TECHNOLOGIES.index(selected)
    ti = st.session_state.tech_inputs

    st.divider()
    st.markdown("**⚙️ Technology-Specific Inputs**")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="section-header">Scale & Output</div>', unsafe_allow_html=True)
        ti["annual_output"][t]      = st.number_input("Annual Output (MWh/yr or t/yr)", 0, 10_000_000, int(ti["annual_output"][t]), 10000, key=f"ao_{t}")
        ti["installed_capacity"][t] = st.number_input("Installed Capacity (MW)", 0, 5000, int(ti["installed_capacity"][t]), 10, key=f"ic_{t}")
        ti["capacity_factor"][t]    = st.slider("Capacity Factor", 0.0, 1.0, ti["capacity_factor"][t], 0.01, key=f"cf_{t}")
        ti["project_lifetime"][t]   = st.slider("Project Lifetime (years)", 5, 50, int(ti["project_lifetime"][t]), 1, key=f"pl_{t}")

    with col2:
        st.markdown('<div class="section-header">Cost Structure</div>', unsafe_allow_html=True)
        ti["capex_per_kw"][t]  = st.number_input("CAPEX per kW (USD/kW)", 0, 20000, int(ti["capex_per_kw"][t]), 100, key=f"ck_{t}")
        ti["opex_pct"][t]      = st.slider("OPEX (% of CAPEX p.a.)", 0.0, 0.20, ti["opex_pct"][t], 0.005, format="%.3f", key=f"op_{t}")
        ti["feedstock_cost"][t]= st.number_input("Feedstock / Fuel Cost (USD/yr)", 0, 50_000_000, int(ti["feedstock_cost"][t]), 100000, key=f"fc_{t}")
        ti["other_opex"][t]    = st.number_input("Other Variable OPEX (USD/yr)", 0, 20_000_000, int(ti["other_opex"][t]), 100000, key=f"ov_{t}")
        ti["wacc"][t]          = st.slider("WACC / Discount Rate", 0.01, 0.25, ti["wacc"][t], 0.005, format="%.3f", key=f"wc_{t}")

    with col3:
        st.markdown('<div class="section-header">Revenue Drivers</div>', unsafe_allow_html=True)
        ti["market_price"][t]   = st.number_input("Market Selling Price (USD/MWh or USD/t)", 0, 100000, int(ti["market_price"][t]), 10, key=f"mp_{t}")
        ti["co2_abated_factor"][t] = st.slider("CO₂ Abated per Unit (tCO₂e/unit)", 0.0, 2.0, ti["co2_abated_factor"][t], 0.01, key=f"ca_{t}")
        if t in [12, 13]:
            ti["clients"][t] = st.number_input("Number of Clients", 0, 10000, int(ti["clients"][t]), 1, key=f"cl_{t}")

    # Results
    r = compute_revenues(st.session_state.prices, t, ti)
    st.divider()
    st.markdown("#### 📊 Revenue Estimation Results")

    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
    with mc1: st.metric("Total Annual Revenue", fmt_m(r["total_rev"]))
    with mc2: st.metric("MBM Revenue", fmt_m(r["mbm_total"]))
    with mc3: st.metric("Direct Revenue", fmt_m(r["direct_rev"]))
    with mc4: st.metric("Total Cost (OPEX)", fmt_m(r["total_cost"]))
    with mc5: st.metric("Net Cash Flow", fmt_m(r["net_cf"]), delta=f"R/C: {r['rev_cost_ratio']:.2f}x")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### MBM Revenue Breakdown")
        mbm_data = {k: v for k, v in r["mbm_breakdown"].items() if v > 0}
        if mbm_data:
            fig_mbm = go.Figure(go.Bar(
                x=list(mbm_data.keys()), y=[v/1e6 for v in mbm_data.values()],
                marker_color=px.colors.qualitative.Pastel,
                text=[f"${v/1e6:.2f}M" for v in mbm_data.values()],
                textposition="outside",
            ))
            fig_mbm.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e5e7eb"), yaxis_title="USD Million", height=320,
            )
            st.plotly_chart(fig_mbm, use_container_width=True)
        else:
            st.info("No active MBM mechanisms for this technology.")

    with col_b:
        st.markdown("#### Cost vs Revenue Structure")
        categories = ["Direct Revenue", "MBM Revenue", "CAPEX (ann.)", "Fixed OPEX", "Feedstock", "Other OPEX"]
        values = [
            r["direct_rev"]/1e6, r["mbm_total"]/1e6,
            -r["ann_capex"]/1e6, -r["fixed_opex"]/1e6,
            -st.session_state.tech_inputs["feedstock_cost"][t]/1e6,
            -st.session_state.tech_inputs["other_opex"][t]/1e6,
        ]
        colors_wf = ["#10b981" if v >= 0 else "#ef4444" for v in values]
        fig_wf = go.Figure(go.Bar(
            x=categories, y=values,
            marker_color=colors_wf,
            text=[f"${abs(v):.2f}M" for v in values], textposition="outside",
        ))
        fig_wf.add_hline(y=0, line_color="white", line_width=0.5)
        fig_wf.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e5e7eb"), yaxis_title="USD Million", height=320,
            xaxis=dict(tickangle=-30),
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    # Applicable mechanisms
    st.markdown("#### ✅ Active MBM Mechanisms for this Technology")
    mech_cols = st.columns(5)
    mechs = ["ets","ctax","fuel","cfd","cbam","corsia","imo","vcm","amc","feebate"]
    for idx, m in enumerate(mechs):
        applicable = DEFAULTS[m][t]
        label, unit = MBM_LABELS[m]
        price_key = m if m in st.session_state.prices else ("cfd_strike" if m=="cfd" else m)
        price_val = st.session_state.prices.get(price_key, "—")
        with mech_cols[idx % 5]:
            color = "#14532d" if applicable else "#1f2937"
            icon  = "✅" if applicable else "❌"
            st.markdown(f"""
            <div style="background:{color};border-radius:8px;padding:10px;margin:3px;text-align:center">
                <div style="font-size:1.1rem">{icon}</div>
                <div style="font-size:0.72rem;color:#d1d5db;font-weight:600">{label}</div>
                <div style="font-size:0.68rem;color:#9ca3af">{price_val} {unit}</div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 3 — SCENARIO ANALYSIS
# ─────────────────────────────────────────────
with tab3:
    st.markdown("#### 📈 Scenario: Carbon Price Sensitivity")
    st.caption("See how total portfolio revenue changes as ETS carbon price varies")

    base_prices = dict(st.session_state.prices)
    ets_range = list(range(10, 310, 10))
    total_revs, mbm_revs, net_cfs = [], [], []

    for ets_p in ets_range:
        test_prices = dict(base_prices)
        test_prices["ets"] = ets_p
        results = [compute_revenues(test_prices, i, st.session_state.tech_inputs) for i in range(14)]
        total_revs.append(sum(r["total_rev"] for r in results)/1e6)
        mbm_revs.append(sum(r["mbm_total"] for r in results)/1e6)
        net_cfs.append(sum(r["net_cf"] for r in results)/1e6)

    fig_sens = make_subplots(rows=1, cols=2, subplot_titles=("Total Revenue & Net CF vs ETS Price", "MBM Revenue vs ETS Price"))
    fig_sens.add_trace(go.Scatter(x=ets_range, y=total_revs, name="Total Revenue", line=dict(color="#3b82f6", width=2)), row=1, col=1)
    fig_sens.add_trace(go.Scatter(x=ets_range, y=net_cfs, name="Net Cash Flow", line=dict(color="#10b981", width=2, dash="dot")), row=1, col=1)
    fig_sens.add_trace(go.Scatter(x=ets_range, y=mbm_revs, name="MBM Revenue", fill="tozeroy", fillcolor="rgba(59,130,246,0.15)", line=dict(color="#60a5fa")), row=1, col=2)
    fig_sens.add_vline(x=base_prices["ets"], line_color="yellow", line_dash="dash", row=1, col=1)
    fig_sens.add_vline(x=base_prices["ets"], line_color="yellow", line_dash="dash", row=1, col=2)
    fig_sens.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"), height=380, showlegend=True,
    )
    fig_sens.update_xaxes(title_text="ETS Price (USD/tCO₂e)")
    fig_sens.update_yaxes(title_text="USD Million")
    st.plotly_chart(fig_sens, use_container_width=True)

    st.divider()
    st.markdown("#### 📊 Multi-Price Scenario Comparison")
    sc_col1, sc_col2 = st.columns(2)
    with sc_col1:
        sc_ets_low  = st.slider("ETS Low", 10, 200, 50, 10)
        sc_ets_base = st.slider("ETS Base", 10, 300, base_prices["ets"], 10)
        sc_ets_high = st.slider("ETS High", 50, 500, 200, 10)
    with sc_col2:
        sc_vcm_low  = st.slider("VCM Low", 5, 100, 30, 5)
        sc_vcm_base = st.slider("VCM Base", 5, 300, base_prices["vcm"], 5)
        sc_vcm_high = st.slider("VCM High", 50, 500, 200, 5)

    scenarios = {
        "Low": {**base_prices, "ets": sc_ets_low, "vcm": sc_vcm_low},
        "Base": {**base_prices, "ets": sc_ets_base, "vcm": sc_vcm_base},
        "High": {**base_prices, "ets": sc_ets_high, "vcm": sc_vcm_high},
    }

    scenario_results = {}
    for scen_name, scen_prices in scenarios.items():
        res = [compute_revenues(scen_prices, i, st.session_state.tech_inputs) for i in range(14)]
        scenario_results[scen_name] = {
            "total_rev": sum(r["total_rev"] for r in res),
            "mbm_total": sum(r["mbm_total"] for r in res),
            "net_cf":    sum(r["net_cf"]    for r in res),
            "total_cost":sum(r["total_cost"]for r in res),
        }

    sc1, sc2, sc3 = st.columns(3)
    for col, (scen, vals) in zip([sc1, sc2, sc3], scenario_results.items()):
        with col:
            st.markdown(f"**Scenario: {scen}**")
            st.metric("Total Revenue",  fmt_m(vals["total_rev"]))
            st.metric("MBM Revenue",    fmt_m(vals["mbm_total"]))
            st.metric("Net Cash Flow",  fmt_m(vals["net_cf"]))

    fig_sc = go.Figure()
    metrics = ["total_rev", "mbm_total", "net_cf"]
    labels  = ["Total Revenue", "MBM Revenue", "Net Cash Flow"]
    colors  = ["#3b82f6", "#10b981", "#f59e0b"]
    for m, lbl, clr in zip(metrics, labels, colors):
        fig_sc.add_trace(go.Bar(
            name=lbl,
            x=list(scenario_results.keys()),
            y=[scenario_results[s][m]/1e6 for s in scenario_results],
            marker_color=clr,
        ))
    fig_sc.update_layout(
        barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"), yaxis_title="USD Million", height=320,
    )
    st.plotly_chart(fig_sc, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 4 — DATA TABLE
# ─────────────────────────────────────────────
with tab4:
    st.markdown("#### 📋 Full Revenue Summary Table")
    all_results2 = [compute_revenues(st.session_state.prices, i, st.session_state.tech_inputs) for i in range(14)]

    table_data = []
    for i, r in enumerate(all_results2):
        table_data.append({
            "Technology":       TECHNOLOGIES[i],
            "Direct Rev ($M)":  round(r["direct_rev"]/1e6, 2),
            "MBM Rev ($M)":     round(r["mbm_total"]/1e6, 2),
            "Total Rev ($M)":   round(r["total_rev"]/1e6, 2),
            "Total Cost ($M)":  round(r["total_cost"]/1e6, 2),
            "Net CF ($M)":      round(r["net_cf"]/1e6, 2),
            "R/C Ratio":        round(r["rev_cost_ratio"], 2),
            "CO₂ Abated (tCO₂e/yr)": int(r["co2_abated"]),
            "Lifetime Rev ($M)":round(r["lifetime_rev"]/1e6, 1),
        })

    df_table = pd.DataFrame(table_data)

    def highlight_netcf(val):
        if isinstance(val, (int, float)):
            if val > 0: return "color: #4ade80"
            elif val < 0: return "color: #f87171"
        return ""

    styled = df_table.style.map(highlight_netcf, subset=["Net CF ($M)"])
    st.dataframe(styled, use_container_width=True, height=480)

    # Download
    csv = df_table.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download as CSV", csv, "revenue_model_results.csv", "text/csv")

    st.divider()
    st.markdown("#### MBM Breakdown per Technology")
    mbm_rows = []
    for i, r in enumerate(all_results2):
        row = {"Technology": TECH_SHORT[i]}
        for mech, val in r["mbm_breakdown"].items():
            row[f"{mech} ($M)"] = round(val/1e6, 2)
        row["Total MBM ($M)"] = round(r["mbm_total"]/1e6, 2)
        mbm_rows.append(row)

    df_mbm = pd.DataFrame(mbm_rows)
    st.dataframe(df_mbm, use_container_width=True, height=480)
