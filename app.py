"""
MIDDIC Viability Engine — Streamlit App (single file)
Port dari implementasi React/TypeScript:
  - Part 1: Overview (mekanisme & cakupan negara)
  - Part 2: Revenue Estimation (Monte Carlo GBM, 5000 sims)
  - Part 3: Viability Analytics (VI = (Y+X) / (GP × C_conv))

Run:
    pip install streamlit plotly numpy pandas
    streamlit run middic_app.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================================
# PAGE CONFIG & THEME
# ============================================================================
st.set_page_config(page_title="MIDDIC Viability Engine", page_icon="🌱", layout="wide")

MIDDIC_GREEN = "#064e3b"
MIDDIC_GREEN_LIGHT = "#10b981"
MIDDIC_BG = "#ecfdf5"

st.markdown(
    f"""
    <style>
      .block-container {{ padding-top: 1.5rem; }}
      h1, h2, h3 {{ color: {MIDDIC_GREEN}; }}
      .kpi-card {{
        background: white; border: 1px solid #d1fae5; border-radius: 12px;
        padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
      }}
      .kpi-label {{ color: #6b7280; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; }}
      .kpi-value {{ color: {MIDDIC_GREEN}; font-size: 26px; font-weight: 700; margin-top: 4px; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# DATA: 43 TECHNOLOGIES
# ============================================================================
TECH_NAMES = [
    ("Solar PV", "PV & Wind Energy"),
    ("Onshore Wind", "PV & Wind Energy"),
    ("Offshore Wind", "PV & Wind Energy"),
    ("Floating Offshore Wind", "PV & Wind Energy"),
    ("Concentrated Solar Power", "PV & Wind Energy"),
    ("Geothermal", "Renewables"),
    ("Hydropower", "Renewables"),
    ("Tidal & Wave", "Renewables"),
    ("Green Hydrogen (electrolysis)", "Hydrogen & Derivatives"),
    ("Battery Storage", "Storage & EVs"),
    ("Long-Duration Storage", "Storage & EVs"),
    ("EV Passenger Vehicles", "Storage & EVs"),
    ("EV Commercial Vehicles", "Storage & EVs"),
    ("EV Charging Infrastructure", "Storage & EVs"),
    ("Sustainable Aviation Fuel (SAF)", "Sustainable Fuels"),
    ("E-Kerosene", "Sustainable Fuels"),
    ("Green Methanol", "Sustainable Fuels"),
    ("Green Ammonia", "Sustainable Fuels"),
    ("Biofuels (Advanced)", "Sustainable Fuels"),
    ("Biogas / Biomethane", "Sustainable Fuels"),
    ("Heat Pumps", "Heat & Buildings"),
    ("Low-carbon Steel", "Industry Decarbonization"),
    ("Low-carbon Cement", "Industry Decarbonization"),
    ("Low-carbon Chemicals", "Industry Decarbonization"),
    ("Low-carbon Aluminum", "Industry Decarbonization"),
    ("Low-carbon Glass", "Industry Decarbonization"),
    ("Low-carbon Paper & Pulp", "Industry Decarbonization"),
    ("Industrial Heat Electrification", "Industry Decarbonization"),
    ("Industrial Heat Pumps", "Industry Decarbonization"),
    ("Building Energy Efficiency", "Heat & Buildings"),
    ("Smart Grids", "Grid & Digital"),
    ("Demand Response", "Grid & Digital"),
    ("Transmission Expansion", "Grid & Digital"),
    ("Carbon Capture & Storage (CCUS)", "CCUS & Removals"),
    ("Bioenergy with CCS (BECCS)", "CCUS & Removals"),
    ("Direct Air Capture (DAC)", "CCUS & Removals"),
    ("Enhanced Weathering", "CCUS & Removals"),
    ("Reforestation / REDD+", "Nature-Based Solutions"),
    ("Blue Carbon (mangroves, seagrass)", "Nature-Based Solutions"),
    ("Sustainable Agriculture", "Nature-Based Solutions"),
    ("Carbon Offset / MRV Platforms", "Digital & Markets"),
    ("Energy Management & Analytics", "Digital & Markets"),
    ("Nuclear (SMR)", "Other Clean Energy"),
]

# 43 × 14: annual_output, installed_capacity, capacity_factor, project_lifetime,
# capex_per_kw, opex_pct, feedstock_cost, other_opex, wacc, market_price,
# co2_abated_factor, learning_rate, cum_cap_now, cum_cap_2035
TECH_DEFAULTS = np.array([
    [500000,200,0.28,25,1100,0.015,0,500000,0.07,65,0.45,0.20,2000,8000],
    [450000,200,0.28,25,1400,0.015,0,600000,0.07,65,0.45,0.15,900,4000],
    [420000,200,0.40,25,3200,0.020,0,1000000,0.08,80,0.45,0.12,60,500],
    [380000,150,0.40,25,4500,0.025,0,1200000,0.09,85,0.45,0.10,1,50],
    [200000,100,0.40,30,5000,0.020,0,800000,0.08,90,0.45,0.08,5,80],
    [50000,30,0.35,25,8000,0.030,0,500000,0.09,100,0.45,0.05,0.2,5],
    [800000,300,0.90,60,8000,0.025,0,2000000,0.09,80,0.50,0.04,0.001,10],
    [150000,50,0.90,30,6000,0.030,0,700000,0.08,90,0.45,0.06,0.01,5],
    [50000,100,0.45,20,2500,0.025,8000000,2000000,0.09,4500,0.90,0.18,0.5,10],
    [300000,150,0.25,15,1800,0.020,0,800000,0.08,90,0.30,0.22,1500,5000],
    [100000,50,0.30,20,3500,0.025,0,600000,0.09,100,0.30,0.10,0.1,20],
    [0,0,1.0,20,0,0.050,0,2000000,0.08,0,0.15,0.08,500,2000],
    [0,0,1.0,30,0,0.020,0,3000000,0.08,0,0.10,0.05,10,100],
    [0,0,1.0,15,0,0.060,0,1500000,0.08,0,0.15,0.12,50,500],
    [250000,50,0.90,25,5000,0.040,5000000,2000000,0.10,700,0.80,0.06,0.1,2],
    [300000,60,0.90,25,4000,0.035,4000000,1800000,0.10,650,0.75,0.08,0.05,1],
    [150000,40,0.90,25,5500,0.040,3000000,1500000,0.10,2500,0.80,0.07,0.02,0.5],
    [200000,50,0.90,25,4500,0.040,4000000,1800000,0.10,600,0.75,0.07,0.05,1],
    [100000,80,0.90,20,3500,0.030,4000000,1500000,0.09,950,0.85,0.10,0.02,0.5],
    [80000,60,0.90,20,4000,0.030,3500000,1200000,0.09,1200,0.80,0.09,0.01,0.3],
    [200000,80,0.85,20,2000,0.025,1000000,800000,0.08,100,0.40,0.08,0.1,3],
    [150000,80,0.85,20,3000,0.030,6000000,1500000,0.10,2800,0.70,0.12,0.05,0.5],
    [100000,60,0.85,20,2500,0.028,5000000,1200000,0.09,1800,0.65,0.10,0.02,0.3],
    [80000,60,0.85,20,4500,0.035,7000000,1500000,0.10,3500,0.75,0.08,0.005,0.1],
    [60000,80,0.90,20,3500,0.030,4000000,1000000,0.09,950,0.85,0.10,0.01,0.2],
    [50000,60,0.90,20,3200,0.030,3500000,900000,0.09,1300,0.75,0.10,0.01,0.2],
    [60000,60,0.90,20,3000,0.028,3000000,900000,0.09,1100,0.70,0.10,0.01,0.2],
    [80000,30,0.85,20,2000,0.028,2000000,700000,0.08,80,0.60,0.08,10,100],
    [100000,40,0.85,20,2500,0.028,2500000,800000,0.08,90,0.60,0.08,5,50],
    [0,0,1.0,10,0,0.050,0,500000,0.08,0,0.30,0.22,100,1000],
    [0,0,1.0,15,0,0.060,1000000,800000,0.09,0,0.50,0.15,0.1,5],
    [0,0,1.0,15,0,0.050,0,500000,0.09,0,0.40,0.18,0.001,1],
    [0,0,1.0,40,0,0.020,0,2000000,0.07,0,0.35,0.05,50,200],
    [100000,50,0.90,30,4000,0.035,2000000,1000000,0.10,80,0.85,0.08,0.03,0.5],
    [120000,60,0.85,25,5000,0.040,3000000,1500000,0.09,150,0.90,0.07,0.01,0.2],
    [50000,25,0.95,20,15000,0.050,3000000,2000000,0.10,500,1.00,0.15,0.001,1],
    [80000,40,0.85,25,4500,0.040,2000000,1200000,0.09,100,0.80,0.07,0.01,0.2],
    [80000,0,1.0,30,500,0.100,500000,300000,0.06,12,1.00,0.05,500,1000],
    [30000,0,1.0,30,300,0.120,200000,100000,0.06,30,1.00,0.04,10,50],
    [400000,0,1.0,20,800,0.050,0,1000000,0.07,100,0.40,0.08,5000,8000],
    [100000,30,0.85,20,2000,0.040,2000000,800000,0.09,200,0.50,0.10,0.5,10],
    [50000,20,0.85,20,3000,0.035,1000000,600000,0.09,500,0.40,0.08,0.1,2],
    [200000,50,0.90,10,1500,0.050,0,1500000,0.08,80,0.20,0.10,50,500],
])

DEFAULT_FIELDS = [
    "annual_output","installed_capacity","capacity_factor","project_lifetime",
    "capex_per_kw","opex_pct","feedstock_cost","other_opex","wacc","market_price",
    "co2_abated_factor","learning_rate","cum_cap_now","cum_cap_2035",
]

TECHNOLOGIES = pd.DataFrame({
    "id": range(len(TECH_NAMES)),
    "name": [n[0] for n in TECH_NAMES],
    "category": [n[1] for n in TECH_NAMES],
    **{f: TECH_DEFAULTS[:, i] for i, f in enumerate(DEFAULT_FIELDS)},
})

# ============================================================================
# DATA: 11 MARKET-BASED MECHANISMS
# ============================================================================
MECH_ORDER = ["ets","ctax","fuel","cfd","ccfd","cbam","corsia","imo","vcm","amc","feebate"]
MECH_INDEX = {k: i for i, k in enumerate(MECH_ORDER)}

MECHANISMS = pd.DataFrame([
    {"id":"ets","short":"ETS","full":"ETS (Emission Trading Schemes)","unit":"USD/tCO₂e","type":"Direct","category":"Carbon Pricing","countries":68},
    {"id":"ctax","short":"Carbon Tax","full":"Carbon Tax","unit":"USD/tCO₂e","type":"Direct","category":"Carbon Pricing","countries":52},
    {"id":"cbam","short":"CBAM","full":"CBAM (Carbon Border Adjustment)","unit":"USD/tCO₂e","type":"Indirect","category":"Carbon Pricing","countries":31},
    {"id":"fuel","short":"Fuel Mandate","full":"Fuel Mandates / Standards","unit":"USD/MWh","type":"Indirect","category":"Regulatory Mandates","countries":28},
    {"id":"cfd","short":"CfD","full":"CfD / CCfD","unit":"USD/MWh","type":"Direct","category":"Market Mechanisms","countries":41},
    {"id":"ccfd","short":"CCfD","full":"Carbon CfD","unit":"USD/tCO₂e","type":"Direct","category":"Market Mechanisms","countries":18},
    {"id":"vcm","short":"VCM","full":"VCM / CDM","unit":"USD/tCO₂e","type":"Indirect","category":"Market Mechanisms","countries":47},
    {"id":"amc","short":"AMC","full":"AMC (Advanced Market Commitments)","unit":"USD/unit","type":"Indirect","category":"Incentives & Support","countries":15},
    {"id":"feebate","short":"Feebate","full":"Feebate Programs","unit":"USD/tCO₂e","type":"Indirect","category":"Others","countries":9},
    {"id":"imo","short":"IMO Levy","full":"IMO Levy (Maritime)","unit":"USD/tCO₂e","type":"Indirect","category":"Others","countries":22},
    {"id":"corsia","short":"CORSIA","full":"CORSIA (Aviation)","unit":"USD/tCO₂e","type":"Indirect","category":"Others","countries":50},
])

def _row(*keys):
    s = set(keys)
    return [k in s for k in MECH_ORDER]

MBM_MATRIX = np.array([
    _row("ets","ctax","cfd","vcm","feebate"),
    _row("ets","ctax","cfd","vcm","feebate"),
    _row("ets","ctax","cfd","vcm","feebate"),
    _row("ets","ctax","cfd","vcm","amc"),
    _row("ets","ctax","cfd","vcm"),
    _row("ets","ctax","cfd","vcm"),
    _row("ets","ctax","cfd","vcm"),
    _row("ets","ctax","cfd","vcm","amc"),
    _row("ets","ctax","fuel","ccfd","cbam","amc","imo"),
    _row("ets","ctax","cfd","vcm","feebate"),
    _row("ets","ctax","cfd","vcm","amc"),
    _row("ets","ctax","feebate","vcm"),
    _row("ets","ctax","feebate","vcm","imo"),
    _row("ets","ctax","feebate"),
    _row("fuel","corsia","vcm","amc","ccfd"),
    _row("fuel","corsia","vcm","amc","ccfd"),
    _row("fuel","imo","vcm","amc","ccfd"),
    _row("fuel","imo","vcm","amc","ccfd"),
    _row("fuel","vcm","feebate"),
    _row("fuel","vcm","feebate"),
    _row("ets","ctax","feebate"),
    _row("ets","ctax","cbam","ccfd","vcm"),
    _row("ets","ctax","cbam","ccfd","vcm"),
    _row("ets","ctax","cbam","ccfd","vcm"),
    _row("ets","ctax","cbam","ccfd","vcm"),
    _row("ets","ctax","cbam","ccfd"),
    _row("ets","ctax","ccfd"),
    _row("ets","ctax","ccfd","feebate"),
    _row("ets","ctax","ccfd","feebate"),
    _row("ets","ctax","feebate"),
    _row("cfd","feebate"),
    _row("cfd","feebate"),
    _row("cfd","amc"),
    _row("ets","ctax","cbam","ccfd","vcm","amc"),
    _row("ets","ctax","vcm","amc","ccfd"),
    _row("vcm","amc","ccfd"),
    _row("vcm","amc"),
    _row("vcm","amc"),
    _row("vcm","amc"),
    _row("vcm","amc","feebate"),
    _row("vcm","amc"),
    _row("feebate","vcm"),
    _row("ets","ctax","cfd","amc"),
])

# ============================================================================
# DATA: 184 COUNTRIES (name, iso3, region, gdp_weight_proxy)
# ============================================================================
COUNTRY_CARBON_PRICES = {
    "Albania":13.7,"Andorra":32.4,"Argentina":5.3,"Australia":21.8,"Austria":48.5,
    "Belgium":66.2,"Canada":66.2,"Chile":5.0,"China":11.8,"Colombia":6.5,
    "Denmark":108.4,"Estonia":27.0,"Finland":66.9,"France":48.1,"Germany":48.5,
    "Hungary":38.8,"Iceland":60.1,"Indonesia":0.7,"Ireland":68.5,"Israel":1.5,
    "Japan":1.9,"Kazakhstan":0.9,"Latvia":16.2,"Liechtenstein":136.0,"Luxembourg":58.5,
    "Mexico":3.9,"Montenegro":25.9,"Netherlands":94.8,"New Zealand":32.0,"Norway":133.9,
    "Poland":0.1,"Portugal":72.7,"Singapore":18.6,"Slovenia":33.3,"South Africa":12.8,
    "South Korea":6.5,"Spain":16.2,"Sweden":144.6,"Switzerland":136.0,"Ukraine":0.7,
    "United Kingdom":57.2,"United States":29.3,"Uruguay":158.8,
}

RAW_COUNTRIES = [
    ("United States","USA","North America",24.7),("China","CHN","Asia",17.7),("Japan","JPN","Asia",4.2),
    ("Germany","DEU","Europe",4.1),("India","IND","Asia",3.5),("United Kingdom","GBR","Europe",3.1),
    ("France","FRA","Europe",2.8),("Italy","ITA","Europe",2.0),("Canada","CAN","North America",2.0),
    ("Brazil","BRA","South America",1.9),("Russia","RUS","Europe",1.9),("South Korea","KOR","Asia",1.7),
    ("Australia","AUS","Oceania",1.5),("Spain","ESP","Europe",1.4),("Mexico","MEX","North America",1.4),
    ("Indonesia","IDN","Asia",1.3),("Netherlands","NLD","Europe",1.0),("Saudi Arabia","SAU","Asia",1.0),
    ("Turkey","TUR","Asia",0.9),("Switzerland","CHE","Europe",0.9),("Taiwan","TWN","Asia",0.8),
    ("Poland","POL","Europe",0.8),("Belgium","BEL","Europe",0.6),("Sweden","SWE","Europe",0.6),
    ("Argentina","ARG","South America",0.6),("Ireland","IRL","Europe",0.5),("Norway","NOR","Europe",0.5),
    ("Israel","ISR","Asia",0.5),("Thailand","THA","Asia",0.5),("Nigeria","NGA","Africa",0.5),
    ("Egypt","EGY","Africa",0.5),("Austria","AUT","Europe",0.5),("United Arab Emirates","ARE","Asia",0.5),
    ("Bangladesh","BGD","Asia",0.4),("Singapore","SGP","Asia",0.4),("Vietnam","VNM","Asia",0.4),
    ("Malaysia","MYS","Asia",0.4),("Philippines","PHL","Asia",0.4),("Denmark","DNK","Europe",0.4),
    ("South Africa","ZAF","Africa",0.4),("Hong Kong","HKG","Asia",0.4),("Pakistan","PAK","Asia",0.4),
    ("Colombia","COL","South America",0.3),("Chile","CHL","South America",0.3),("Romania","ROU","Europe",0.3),
    ("Czech Republic","CZE","Europe",0.3),("Finland","FIN","Europe",0.3),("Iraq","IRQ","Asia",0.3),
    ("Portugal","PRT","Europe",0.3),("Peru","PER","South America",0.2),("Greece","GRC","Europe",0.2),
    ("New Zealand","NZL","Oceania",0.2),("Qatar","QAT","Asia",0.2),("Kazakhstan","KAZ","Asia",0.2),
    ("Hungary","HUN","Europe",0.2),("Algeria","DZA","Africa",0.2),("Kuwait","KWT","Asia",0.2),
    ("Ukraine","UKR","Europe",0.2),("Morocco","MAR","Africa",0.2),("Ethiopia","ETH","Africa",0.1),
    ("Slovakia","SVK","Europe",0.1),("Ecuador","ECU","South America",0.1),("Dominican Republic","DOM","North America",0.1),
    ("Kenya","KEN","Africa",0.1),("Angola","AGO","Africa",0.1),("Oman","OMN","Asia",0.1),
    ("Guatemala","GTM","North America",0.1),("Bulgaria","BGR","Europe",0.1),("Venezuela","VEN","South America",0.1),
    ("Luxembourg","LUX","Europe",0.1),("Croatia","HRV","Europe",0.1),("Tanzania","TZA","Africa",0.1),
    ("Panama","PAN","North America",0.1),("Belarus","BLR","Europe",0.1),("Côte d'Ivoire","CIV","Africa",0.1),
    ("Ghana","GHA","Africa",0.1),("Costa Rica","CRI","North America",0.1),("Lithuania","LTU","Europe",0.1),
    ("Uruguay","URY","South America",0.1),("Tunisia","TUN","Africa",0.1),("Sri Lanka","LKA","Asia",0.1),
    ("Slovenia","SVN","Europe",0.1),("Serbia","SRB","Europe",0.1),("Myanmar","MMR","Asia",0.1),
    ("Azerbaijan","AZE","Asia",0.1),("Jordan","JOR","Asia",0.1),("Bahrain","BHR","Asia",0.1),
    ("Cameroon","CMR","Africa",0.05),("Bolivia","BOL","South America",0.05),("Paraguay","PRY","South America",0.05),
    ("Latvia","LVA","Europe",0.05),("Uganda","UGA","Africa",0.05),("Estonia","EST","Europe",0.05),
    ("Nepal","NPL","Asia",0.05),("Cyprus","CYP","Europe",0.05),("Honduras","HND","North America",0.05),
    ("El Salvador","SLV","North America",0.05),("Iceland","ISL","Europe",0.05),("Cambodia","KHM","Asia",0.05),
    ("Senegal","SEN","Africa",0.05),("Trinidad and Tobago","TTO","South America",0.05),("Papua New Guinea","PNG","Oceania",0.05),
    ("Bosnia and Herzegovina","BIH","Europe",0.05),("Zambia","ZMB","Africa",0.04),("Georgia","GEO","Asia",0.04),
    ("Mali","MLI","Africa",0.04),("Burkina Faso","BFA","Africa",0.04),("Botswana","BWA","Africa",0.04),
    ("Gabon","GAB","Africa",0.04),("Mozambique","MOZ","Africa",0.04),("Albania","ALB","Europe",0.04),
    ("Madagascar","MDG","Africa",0.04),("Mongolia","MNG","Asia",0.04),("Armenia","ARM","Asia",0.04),
    ("Brunei","BRN","Asia",0.04),("Jamaica","JAM","North America",0.04),("North Macedonia","MKD","Europe",0.04),
    ("Mauritius","MUS","Africa",0.04),("Malta","MLT","Europe",0.04),("Namibia","NAM","Africa",0.03),
    ("Moldova","MDA","Europe",0.03),("Niger","NER","Africa",0.03),("Equatorial Guinea","GNQ","Africa",0.03),
    ("Bahamas","BHS","North America",0.03),("Republic of the Congo","COG","Africa",0.03),("Rwanda","RWA","Africa",0.03),
    ("Tajikistan","TJK","Asia",0.03),("Kyrgyzstan","KGZ","Asia",0.03),("Iran","IRN","Asia",0.4),
    ("Syria","SYR","Asia",0.03),("Yemen","YEM","Asia",0.03),("Sudan","SDN","Africa",0.03),
    ("South Sudan","SSD","Africa",0.02),("Zimbabwe","ZWE","Africa",0.03),("Malawi","MWI","Africa",0.02),
    ("Afghanistan","AFG","Asia",0.02),("Haiti","HTI","North America",0.02),("Benin","BEN","Africa",0.02),
    ("Laos","LAO","Asia",0.02),("Nicaragua","NIC","North America",0.02),("Kosovo","XKX","Europe",0.02),
    ("Mauritania","MRT","Africa",0.02),("Togo","TGO","Africa",0.02),("Sierra Leone","SLE","Africa",0.02),
    ("Eswatini","SWZ","Africa",0.02),("Liechtenstein","LIE","Europe",0.02),("Andorra","AND","Europe",0.02),
    ("Monaco","MCO","Europe",0.02),("Liberia","LBR","Africa",0.02),("Burundi","BDI","Africa",0.02),
    ("Guyana","GUY","South America",0.02),("Maldives","MDV","Asia",0.02),("Lesotho","LSO","Africa",0.02),
    ("Suriname","SUR","South America",0.02),("Cape Verde","CPV","Africa",0.02),("Bhutan","BTN","Asia",0.02),
    ("Belize","BLZ","North America",0.02),("Djibouti","DJI","Africa",0.02),("Central African Republic","CAF","Africa",0.02),
    ("Eritrea","ERI","Africa",0.02),("Antigua and Barbuda","ATG","North America",0.01),("Seychelles","SYC","Africa",0.01),
    ("Saint Lucia","LCA","North America",0.01),("Timor-Leste","TLS","Asia",0.01),("Guinea-Bissau","GNB","Africa",0.01),
    ("Solomon Islands","SLB","Oceania",0.01),("Comoros","COM","Africa",0.01),("Grenada","GRD","North America",0.01),
    ("Vanuatu","VUT","Oceania",0.01),("Saint Kitts and Nevis","KNA","North America",0.01),("Samoa","WSM","Oceania",0.01),
    ("Saint Vincent and the Grenadines","VCT","North America",0.01),("Dominica","DMA","North America",0.01),
    ("Tonga","TON","Oceania",0.01),("São Tomé and Príncipe","STP","Africa",0.01),("Micronesia","FSM","Oceania",0.01),
    ("Palau","PLW","Oceania",0.01),("Marshall Islands","MHL","Oceania",0.01),("Kiribati","KIR","Oceania",0.01),
    ("Nauru","NRU","Oceania",0.01),("Tuvalu","TUV","Oceania",0.01),("San Marino","SMR","Europe",0.01),
    ("Vatican City","VAT","Europe",0.01),("Fiji","FJI","Oceania",0.02),("Cuba","CUB","North America",0.05),
    ("North Korea","PRK","Asia",0.05),("Lebanon","LBN","Asia",0.05),("Libya","LBY","Africa",0.1),
    ("Turkmenistan","TKM","Asia",0.1),("Uzbekistan","UZB","Asia",0.1),("DR Congo","COD","Africa",0.05),
    ("Chad","TCD","Africa",0.04),("Somalia","SOM","Africa",0.02),("Guinea","GIN","Africa",0.04),
]

def _elec(iso3: str) -> float:
    h = 0
    for ch in iso3:
        h = (h * 31 + ord(ch)) & 0xFFFF
    return 40 + (h % 90)

_total_w = sum(r[3] for r in RAW_COUNTRIES)
COUNTRIES = pd.DataFrame([
    {
        "name": n, "iso3": iso, "region": reg,
        "carbon_price": COUNTRY_CARBON_PRICES.get(n, 0.0),
        "weight": w / _total_w,
        "electricity_price": _elec(iso),
    }
    for (n, iso, reg, w) in RAW_COUNTRIES
])

# ============================================================================
# DATA: PRICING & SCENARIOS
# ============================================================================
DEFAULT_PRICES = {
    "ets":70,"ctax":50,"fuel":240,"cfd_strike":120,"cfd_ref":80,
    "ccfd_strike":100,"ccfd_ref":60,"cbam":55,"corsia":22,"imo":380,
    "vcm":100,"amc":100,"feebate":50,"electricity":60,"gas":8,"biomass":40,
    "cfd":120,"ccfd":100,
}

GBM_PARAMS = {
    "ets":    (0.04,0.22,10,250),"ctax":(0.05,0.18,5,200),"fuel":(0.03,0.15,50,800),
    "cfd":    (0.02,0.12,50,400),"ccfd":(0.03,0.14,30,300),"cbam":(0.04,0.20,10,200),
    "corsia": (0.05,0.25,5,150), "imo": (0.04,0.20,100,800),"vcm":(0.06,0.30,2,200),
    "amc":    (0.02,0.10,20,500),"feebate":(0.03,0.15,10,200),
}

SCENARIO_MULT = {
    "current":  {k:1.0 for k in MECH_ORDER},
    "net_zero": {"ets":1.85,"ctax":1.7,"cbam":1.6,"fuel":1.4,"cfd":1.25,"ccfd":1.4,"corsia":1.5,"imo":1.6,"vcm":1.4,"amc":1.5,"feebate":1.3},
    "worst":    {"ets":0.45,"ctax":0.4,"cbam":0.3,"fuel":0.7,"cfd":0.8,"ccfd":0.6,"corsia":0.5,"imo":0.4,"vcm":0.5,"amc":0.6,"feebate":0.4},
}

SCENARIO_LABEL = {"current":"Current Mechanisms","net_zero":"Net-Zero Aligned","worst":"Worst Case"}

def prices_for_scenario(scenario: str) -> dict:
    out = dict(DEFAULT_PRICES)
    for k, m in SCENARIO_MULT[scenario].items():
        out[k] = DEFAULT_PRICES.get(k, 0) * m
    return out

# ============================================================================
# MONTE CARLO ENGINE
# ============================================================================
Y_MECHS = ["cfd","ccfd","amc","feebate"]
X_MECHS = ["ets","ctax","fuel","cbam","corsia","imo","vcm"]

def generate_price_paths(base: dict, n_years: int, n_sims: int, rng: np.random.Generator) -> dict:
    paths = {}
    for k in MECH_ORDER:
        mu, sigma, floor, cap = GBM_PARAMS[k]
        S0 = base.get(k, 0)
        if S0 <= 0:
            paths[k] = np.zeros((n_sims, n_years))
            continue
        drift = mu - 0.5 * sigma * sigma
        shocks = rng.standard_normal((n_sims, n_years)) * sigma + drift
        log_cum = np.cumsum(shocks, axis=1)
        prices = S0 * np.exp(log_cum)
        paths[k] = np.clip(prices, floor, cap)
    return paths


def run_monte_carlo(tech_id: int, base_prices: dict, n_sims: int = 5000, seed: int = 42, scale: float = 1.0, years: int | None = None) -> dict:
    d = TECHNOLOGIES.iloc[tech_id]
    lt = int(years if years else d["project_lifetime"])
    o = d["annual_output"] * scale
    co2 = o * d["co2_abated_factor"]
    mech_row = MBM_MATRIX[tech_id]
    rng = np.random.default_rng(seed + tech_id * 1000 + int(scale * 10000))

    paths = generate_price_paths(base_prices, lt, n_sims, rng)

    def on(m): return mech_row[MECH_INDEX[m]]
    cfd_ref = base_prices["cfd_ref"]
    ccfd_ref = base_prices["ccfd_ref"]

    x_annual = np.zeros((n_sims, lt))
    if co2 > 0:
        if on("ets"):    x_annual += paths["ets"] * co2
        if on("ctax"):   x_annual += paths["ctax"] * co2
        if on("cbam"):   x_annual += paths["cbam"] * co2 * 0.85
        if on("corsia"): x_annual += paths["corsia"] * co2 * 1.05
        if on("imo"):    x_annual += paths["imo"] * co2 * 0.95
        if on("vcm"):    x_annual += paths["vcm"] * co2
    if o > 0 and on("fuel"):
        x_annual += paths["fuel"] * o * 0.85

    y_annual = np.zeros((n_sims, lt))
    if o > 0 and on("cfd"):
        v = np.clip(paths["cfd"] - cfd_ref, 0, None)
        y_annual += v * o * 0.5
    if co2 > 0 and on("ccfd"):
        v = np.clip(paths["ccfd"] - ccfd_ref, 0, None)
        y_annual += v * co2 * 0.5
    if o > 0 and on("amc"):
        y_annual += paths["amc"] * (o / 1000) * 0.5
    if co2 > 0 and on("feebate"):
        y_annual += paths["feebate"] * co2 * 0.5

    y_life = y_annual.sum(axis=1)
    x_life = x_annual.sum(axis=1)
    total = y_life + x_life
    annual_p50 = np.median(y_annual + x_annual, axis=0)

    return {
        "total_p5": np.percentile(total, 5),
        "total_p10": np.percentile(total, 10),
        "total_p50": np.percentile(total, 50),
        "total_p90": np.percentile(total, 90),
        "total_p95": np.percentile(total, 95),
        "total_mean": total.mean(),
        "total_std": total.std(),
        "y_p5": np.percentile(y_life, 5), "y_p50": np.percentile(y_life, 50), "y_p95": np.percentile(y_life, 95),
        "x_p5": np.percentile(x_life, 5), "x_p50": np.percentile(x_life, 50), "x_p95": np.percentile(x_life, 95),
        "annual_path_p50": annual_p50,
        "y_samples": y_life, "x_samples": x_life, "total_samples": total,
        "prob_positive": (total > 0).mean(),
        "lifetime_years": lt,
    }

# ============================================================================
# VIABILITY
# ============================================================================
def compute_vi(total_p50, total_p5, total_p95, total_mean, total_std, green_premium, conv_cost):
    denom = max(1, green_premium * conv_cost)
    cv = total_std / total_mean if total_mean > 0 else 1
    return {
        "vi_p50": total_p50 / denom,
        "vi_p5": total_p5 / denom,
        "vi_p95": total_p95 / denom,
        "break_even_gp": total_p50 / max(1, conv_cost),
        "confidence": max(0, min(1, 1 - cv * 0.6)),
        "is_viable": (total_p50 / denom) >= 1,
    }

def conventional_cost(tech_id: int) -> float:
    """Estimate conventional lifetime cost for VI denominator."""
    d = TECHNOLOGIES.iloc[tech_id]
    capex = d["capex_per_kw"] * d["installed_capacity"] * 1000  # USD
    opex = (d["other_opex"] + d["feedstock_cost"] * 0.001) * d["project_lifetime"]
    return max(1e6, capex + opex)

# ============================================================================
# UI HELPERS
# ============================================================================
def kpi(label: str, value: str, sub: str = ""):
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div style="color:#9ca3af;font-size:12px;margin-top:4px;">{sub}</div></div>',
        unsafe_allow_html=True,
    )

def fmt_usd(v: float) -> str:
    a = abs(v)
    if a >= 1e12: return f"${v/1e12:.2f}T"
    if a >= 1e9:  return f"${v/1e9:.2f}B"
    if a >= 1e6:  return f"${v/1e6:.2f}M"
    if a >= 1e3:  return f"${v/1e3:.1f}K"
    return f"${v:.0f}"

# ============================================================================
# PAGES
# ============================================================================
def page_overview():
    st.title("🌍 MIDDIC Overview")
    st.caption("Cakupan global Market-Based Mechanisms (MBM) untuk 43 teknologi rendah karbon di 184 negara.")

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Technologies", "43", "innovations tracked")
    with c2: kpi("Mechanisms", "11", "MBM categories")
    with c3: kpi("Countries", str(len(COUNTRIES)), "with ISO3 mapping")
    with c4: kpi("Avg Carbon Price", f"${COUNTRIES['carbon_price'][COUNTRIES['carbon_price']>0].mean():.1f}",
                 "USD/tCO₂e (priced countries)")

    st.markdown("### 🗺️ Global Carbon Price Coverage")
    fig = px.choropleth(
        COUNTRIES, locations="iso3", color="carbon_price",
        hover_name="name", hover_data={"iso3": False, "carbon_price": ":.1f", "region": True},
        color_continuous_scale=["#ecfdf5", "#10b981", "#064e3b"],
        labels={"carbon_price": "USD/tCO₂e"},
    )
    fig.update_layout(height=500, margin=dict(l=0, r=0, t=10, b=0),
                      geo=dict(showframe=False, projection_type="natural earth"))
    st.plotly_chart(fig, use_container_width=True)

    cA, cB = st.columns(2)
    with cA:
        st.markdown("### Mechanism Country Coverage")
        m_sorted = MECHANISMS.sort_values("countries", ascending=True)
        fig = px.bar(m_sorted, x="countries", y="short", orientation="h",
                     color="countries", color_continuous_scale=["#a7f3d0", "#064e3b"],
                     labels={"countries": "# Countries", "short": ""})
        fig.update_layout(height=420, showlegend=False, coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with cB:
        st.markdown("### Top 10 Carbon Pricing Countries")
        top10 = COUNTRIES[COUNTRIES["carbon_price"] > 0].nlargest(10, "carbon_price")
        fig = px.bar(top10.sort_values("carbon_price"), x="carbon_price", y="name", orientation="h",
                     color="carbon_price", color_continuous_scale=["#a7f3d0", "#064e3b"],
                     labels={"carbon_price": "USD/tCO₂e", "name": ""})
        fig.update_layout(height=420, showlegend=False, coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Mechanism Catalog")
    st.dataframe(MECHANISMS[["short", "full", "type", "category", "unit", "countries"]],
                 use_container_width=True, hide_index=True)


def page_revenue():
    st.title("💰 Revenue Estimation")
    st.caption("Monte Carlo lifetime revenue (Y = subsidies/incentives, X = avoided compliance) — GBM 5000 simulations.")

    with st.sidebar:
        st.markdown("### Configuration")
        tech_id = st.selectbox("Technology", TECHNOLOGIES["id"],
                               format_func=lambda i: TECHNOLOGIES.iloc[i]["name"])
        scenario = st.radio("Policy Scenario", list(SCENARIO_LABEL.keys()),
                            format_func=lambda s: SCENARIO_LABEL[s])
        n_sims = st.slider("Monte Carlo iterations", 500, 10000, 5000, step=500)

        st.markdown("### Tech Parameters")
        d = TECHNOLOGIES.iloc[tech_id]
        annual_output = st.number_input("Annual output (units/yr)", 0.0, value=float(d["annual_output"]))
        capacity = st.number_input("Installed capacity (GW)", 0.0, value=float(d["installed_capacity"]))
        lifetime = st.slider("Project lifetime (yrs)", 5, 60, int(d["project_lifetime"]))
        co2_factor = st.slider("CO₂ abated factor", 0.0, 2.0, float(d["co2_abated_factor"]), 0.05)

    # Override defaults for this run
    TECHNOLOGIES.loc[tech_id, "annual_output"] = annual_output
    TECHNOLOGIES.loc[tech_id, "installed_capacity"] = capacity
    TECHNOLOGIES.loc[tech_id, "project_lifetime"] = lifetime
    TECHNOLOGIES.loc[tech_id, "co2_abated_factor"] = co2_factor

    base = prices_for_scenario(scenario)

    with st.spinner(f"Running {n_sims} Monte Carlo simulations..."):
        result = run_monte_carlo(tech_id, base, n_sims=n_sims)

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Lifetime P50", fmt_usd(result["total_p50"]), f"{result['lifetime_years']} years")
    with c2: kpi("P5 – P95", f"{fmt_usd(result['total_p5'])} – {fmt_usd(result['total_p95'])}", "90% confidence")
    with c3: kpi("Subsidies (Y) P50", fmt_usd(result["y_p50"]), "CfD, CCfD, AMC, Feebate")
    with c4: kpi("Compliance (X) P50", fmt_usd(result["x_p50"]), "ETS, Tax, Fuel, CBAM, IMO, VCM")

    cA, cB = st.columns([2, 1])
    with cA:
        st.markdown("### Lifetime Revenue Distribution")
        fig = go.Figure()
        fig.add_trace(go.Box(y=result["y_samples"], name="Y (Subsidies)", marker_color="#10b981"))
        fig.add_trace(go.Box(y=result["x_samples"], name="X (Compliance)", marker_color="#064e3b"))
        fig.add_trace(go.Box(y=result["total_samples"], name="Y + X (Total)", marker_color="#a7f3d0"))
        fig.update_layout(height=420, yaxis_title="USD lifetime", margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with cB:
        st.markdown("### Y vs X Composition (P50)")
        fig = px.pie(values=[result["y_p50"], result["x_p50"]],
                     names=["Y (Subsidies)", "X (Compliance)"],
                     color_discrete_sequence=["#10b981", "#064e3b"], hole=0.5)
        fig.update_layout(height=420, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Annual Revenue Trajectory (P50)")
    years = list(range(1, result["lifetime_years"] + 1))
    df_path = pd.DataFrame({"Year": years, "Annual Revenue (USD)": result["annual_path_p50"]})
    fig = px.area(df_path, x="Year", y="Annual Revenue (USD)",
                  color_discrete_sequence=["#10b981"])
    fig.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🌐 Country Distribution (Lifetime P50, weighted by GDP)")
    df_map = COUNTRIES.copy()
    df_map["revenue"] = df_map["weight"] * result["total_p50"]
    fig = px.choropleth(df_map, locations="iso3", color="revenue", hover_name="name",
                        color_continuous_scale=["#ecfdf5", "#10b981", "#064e3b"],
                        labels={"revenue": "USD lifetime"})
    fig.update_layout(height=480, margin=dict(l=0,r=0,t=10,b=0),
                      geo=dict(showframe=False, projection_type="natural earth"))
    st.plotly_chart(fig, use_container_width=True)


def page_viability():
    st.title("📊 Viability Analytics")
    st.caption("Viability Index (VI) = (Y + X) / (GP × C_conv). VI ≥ 1 → economically viable.")

    with st.sidebar:
        st.markdown("### Configuration")
        tech_id = st.selectbox("Technology", TECHNOLOGIES["id"],
                               format_func=lambda i: TECHNOLOGIES.iloc[i]["name"], key="via_tech")
        scenario = st.radio("Policy Scenario", list(SCENARIO_LABEL.keys()),
                            format_func=lambda s: SCENARIO_LABEL[s], key="via_scen")
        green_premium = st.slider("Green Premium (%)", 5, 100, 30, key="via_gp") / 100

    base = prices_for_scenario(scenario)
    with st.spinner("Computing viability..."):
        result = run_monte_carlo(tech_id, base, n_sims=3000)
        c_conv = conventional_cost(tech_id)
        vi = compute_vi(result["total_p50"], result["total_p5"], result["total_p95"],
                        result["total_mean"], result["total_std"], green_premium, c_conv)

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Viability Index (P50)", f"{vi['vi_p50']:.2f}",
                 "✅ Viable" if vi["is_viable"] else "❌ Below 1.0")
    with c2: kpi("VI Range (P5 – P95)", f"{vi['vi_p5']:.2f} – {vi['vi_p95']:.2f}", "90% interval")
    with c3: kpi("Break-even GP", f"{vi['break_even_gp']*100:.1f}%", "Premium needed for VI=1")
    with c4: kpi("Confidence", f"{vi['confidence']*100:.0f}%", "Inverse coefficient of variation")

    st.markdown("### VI Distribution Across Countries (weighted)")
    df_map = COUNTRIES.copy()
    # Adjust per-country VI by carbon price multiplier
    base_carbon = max(1, COUNTRIES["carbon_price"].mean())
    df_map["vi"] = vi["vi_p50"] * (1 + (df_map["carbon_price"] - base_carbon) / max(1, base_carbon) * 0.3)
    df_map["vi_bucket"] = pd.cut(df_map["vi"], bins=[-np.inf, 0.5, 1.0, 1.5, 2.0, np.inf],
                                  labels=["<0.5", "0.5–1.0", "1.0–1.5", "1.5–2.0", ">2.0"])

    fig = px.choropleth(df_map, locations="iso3", color="vi", hover_name="name",
                        color_continuous_scale=["#fee2e2", "#fef3c7", "#10b981", "#064e3b"],
                        range_color=[0, 2.5], labels={"vi": "VI"})
    fig.update_layout(height=480, margin=dict(l=0,r=0,t=10,b=0),
                      geo=dict(showframe=False, projection_type="natural earth"))
    st.plotly_chart(fig, use_container_width=True)

    cA, cB = st.columns(2)
    with cA:
        st.markdown("### VI Histogram")
        fig = px.histogram(df_map, x="vi", nbins=30, color_discrete_sequence=["#10b981"])
        fig.add_vline(x=1.0, line_dash="dash", line_color="red", annotation_text="VI=1")
        fig.update_layout(height=380, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with cB:
        st.markdown("### Viability Buckets")
        bucket_counts = df_map["vi_bucket"].value_counts().sort_index()
        fig = px.bar(x=bucket_counts.index.astype(str), y=bucket_counts.values,
                     color=bucket_counts.values, color_continuous_scale=["#fee2e2","#10b981","#064e3b"],
                     labels={"x": "VI Bucket", "y": "# Countries"})
        fig.update_layout(height=380, showlegend=False, coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Top 15 Most Viable Countries")
    top = df_map.nlargest(15, "vi")[["name", "region", "carbon_price", "vi"]]
    top.columns = ["Country", "Region", "Carbon Price (USD/tCO₂e)", "Viability Index"]
    st.dataframe(top, use_container_width=True, hide_index=True)


# ============================================================================
# ROUTER
# ============================================================================
PAGES = {
    "🌍 Part 1 — Overview": page_overview,
    "💰 Part 2 — Revenue Estimation": page_revenue,
    "📊 Part 3 — Viability Analytics": page_viability,
}

with st.sidebar:
    st.markdown(f"## 🌱 MIDDIC")
    st.caption("Viability Engine v1.0")
    page = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
    st.markdown("---")

PAGES[page]()

st.markdown("---")
st.caption("MIDDIC Viability Engine • 43 technologies × 11 mechanisms × 184 countries • Monte Carlo GBM")
