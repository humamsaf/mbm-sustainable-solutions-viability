import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

st.set_page_config(
    page_title="MBM Revenue Model v2",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #f5f7fa !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stSidebar"] {
    min-width: 248px !important; max-width: 248px !important;
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    box-shadow: 2px 0 16px rgba(0,0,0,0.05) !important;
}
[data-testid="stSidebarContent"] { padding: 0 !important; }
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
.block-container {
    padding: 1.5rem 1.75rem 2rem 1.75rem !important;
    max-width: 100% !important;
    background: #f5f7fa !important;
}
.page-header {
    background: linear-gradient(135deg, #065f46 0%, #059669 55%, #34d399 100%);
    border-radius: 14px; padding: 26px 30px 24px 30px;
    margin-bottom: 22px; position: relative; overflow: hidden;
}
.page-header::after {
    content: ''; position: absolute; right: -50px; top: -50px;
    width: 200px; height: 200px; border-radius: 50%;
    background: rgba(255,255,255,0.07); pointer-events: none;
}
.page-header-badge {
    display: inline-block; background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.25); border-radius: 99px;
    padding: 3px 12px; font-size: 0.65rem; font-weight: 700;
    color: rgba(255,255,255,0.9); text-transform: uppercase;
    letter-spacing: 0.1em; margin-bottom: 10px;
}
.page-header-title { font-size: 1.45rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em; margin: 0 0 5px 0; line-height: 1.2; }
.page-header-sub { font-size: 0.8rem; color: rgba(255,255,255,0.72); margin: 0; font-weight: 400; }
.kpi-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 18px 20px 16px 20px; box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    position: relative; overflow: hidden; height: 100%;
}
.kpi-card::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0;
    width: 4px; border-radius: 12px 0 0 12px;
    background: linear-gradient(180deg, #059669, #34d399);
}
.kpi-value { font-size: 1.45rem; font-weight: 800; color: #064e3b; line-height: 1; margin-bottom: 6px; font-variant-numeric: tabular-nums; }
.kpi-label { font-size: 0.66rem; font-weight: 700; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.09em; margin-bottom: 4px; }
.kpi-sub { font-size: 0.73rem; color: #059669; font-weight: 500; }
.sec-head {
    font-size: 0.68rem; font-weight: 700; color: #059669; text-transform: uppercase;
    letter-spacing: 0.12em; margin: 20px 0 12px 0; display: flex; align-items: center; gap: 8px;
}
.sec-head::after { content: ''; flex: 1; height: 1.5px; background: linear-gradient(90deg, #d1fae5, transparent); }
[data-testid="stPlotlyChart"] {
    background: #ffffff !important; border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important; padding: 14px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04) !important; overflow: hidden !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important; color: #374151 !important;
    border: none !important; border-radius: 8px !important; font-size: 0.8rem !important;
    font-weight: 500 !important; text-align: left !important; padding: 9px 14px !important;
    box-shadow: none !important; transition: background 0.15s, color 0.15s !important; width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover { background: #f0fdf4 !important; color: #059669 !important; }
.reset-btn > button { background: #fff7ed !important; color: #c2410c !important; border: 1px solid #fed7aa !important; border-radius: 8px !important; font-size: 0.78rem !important; font-weight: 600 !important; }
.prog-wrap { margin-bottom: 9px; }
.prog-row { display: flex; justify-content: space-between; font-size: 0.73rem; color: #6b7280; margin-bottom: 3px; }
.prog-row b { color: #1f2937; font-weight: 600; }
.prog-bg { background: #f0fdf4; border-radius: 6px; height: 5px; }
.prog-fill { height: 5px; border-radius: 6px; background: linear-gradient(90deg, #059669, #34d399); }
.chip { display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px; border-radius: 99px; font-size: 0.68rem; font-weight: 600; margin: 2px; }
.chip-d   { background: #d1fae5; border: 1px solid #6ee7b7; color: #065f46; }
.chip-i   { background: #dbeafe; border: 1px solid #93c5fd; color: #1e3a8a; }
.chip-off { background: #f9fafb; border: 1px solid #e5e7eb; color: #d1d5db; }
.stTabs [data-baseweb="tab-list"] { gap: 0; background: transparent !important; border-bottom: 2px solid #e2e8f0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; font-size: 0.79rem !important; color: #9ca3af !important; padding: 9px 20px !important; border-bottom: 2px solid transparent !important; margin-bottom: -2px !important; }
.stTabs [aria-selected="true"] { color: #059669 !important; border-bottom: 2px solid #059669 !important; font-weight: 700 !important; }
[data-testid="stSlider"] [data-testid="stSliderThumb"] { background: #059669 !important; }
[data-baseweb="select"] > div { background: #ffffff !important; border: 1px solid #d1d5db !important; border-radius: 8px !important; }
[data-testid="stDataFrameResizable"] { border: 1px solid #e2e8f0 !important; border-radius: 10px !important; overflow: hidden !important; }
hr { border-color: #e2e8f0 !important; margin: 12px 0 !important; }
.cat-badge {
    display: inline-block; padding: 2px 10px; border-radius: 99px;
    font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 8px;
}
.cat-energy    { background:#d1fae5; color:#065f46; border:1px solid #6ee7b7; }
.cat-storage   { background:#dbeafe; color:#1e3a8a; border:1px solid #93c5fd; }
.cat-industrial{ background:#fef3c7; color:#92400e; border:1px solid #fcd34d; }
.cat-transport { background:#ede9fe; color:#4c1d95; border:1px solid #c4b5fd; }
.cat-carbon    { background:#fee2e2; color:#7f1d1d; border:1px solid #fca5a5; }
.cat-building  { background:#f0fdf4; color:#14532d; border:1px solid #86efac; }
.cat-circular  { background:#fdf4ff; color:#6b21a8; border:1px solid #d8b4fe; }
.nav-group-label {
    font-size: 0.58rem; font-weight: 700; color: #cbd5e1; text-transform: uppercase;
    letter-spacing: 0.13em; padding: 10px 18px 3px 18px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# TECHNOLOGY DEFINITIONS (44 technologies)
# ─────────────────────────────────────────────────────────────────
TECHNOLOGIES = [
    "Solar PV", "Onshore Wind", "Offshore Wind (fixed foundation)", "Floating Offshore Wind",
    "Concentrated Solar Power (CSP)", "Ocean / Tidal / Wave Energy", "Small Modular Reactors (SMR)",
    "Enhanced Geothermal Systems (EGS)", "Green Hydrogen (electrolysis)",
    "Battery Storage (grid-scale)", "Long-Duration Energy Storage (LDES)", "Smart Grid & Grid Modernization",
    "HVDC Transmission", "Virtual Power Plants (VPP)",
    "Low-carbon Steel & Cement", "Electric Arc Furnace (EAF)", "Green Aluminium", "Low-carbon Concrete",
    "Green Fertilizer (low-carbon NH3)", "Hydrogen-based Chemicals", "Industrial Heat Pumps (high-temp)",
    "Sustainable Aviation Fuel (SAF)", "HVO (Hydrotreated Vegetable Oil)", "E-kerosene (aviation e-fuel)",
    "E-Ammonia (maritime fuel)", "E-Methanol (maritime fuel)", "E-diesel / E-methanol (road & ship)",
    "Biogas (anaerobic digestion)", "Biomethane (upgraded to grid)", "Electric Vehicles (EVs)",
    "Hydrogen Fuel Cells (heavy-duty)", "Electric Aviation (eVTOL/short-haul)", "Rail Electrification",
    "Carbon Capture & Storage (CCUS)", "BECCS (Bioenergy + CCS)", "Direct Air Capture (DAC)",
    "Waste-to-Energy + CCS", "Reforestation / REDD+ / NBS", "Blue Carbon (mangroves, seagrass)",
    "Building Energy Efficiency / Retrofits",
    "Advanced / Chemical Recycling", "Critical Minerals Processing (low-C)",
    "Green Data Centers",
]
N = len(TECHNOLOGIES)

TECH_CATEGORIES = [
    "Clean Energy Generation","Clean Energy Generation","Clean Energy Generation","Clean Energy Generation",
    "Clean Energy Generation","Clean Energy Generation","Clean Energy Generation","Clean Energy Generation","Clean Energy Generation",
    "Energy Storage & Grid","Energy Storage & Grid","Energy Storage & Grid","Energy Storage & Grid","Energy Storage & Grid",
    "Industrial Decarbonisation","Industrial Decarbonisation","Industrial Decarbonisation","Industrial Decarbonisation",
    "Industrial Decarbonisation","Industrial Decarbonisation","Industrial Decarbonisation",
    "Transport & Fuels","Transport & Fuels","Transport & Fuels","Transport & Fuels","Transport & Fuels",
    "Transport & Fuels","Transport & Fuels","Transport & Fuels","Transport & Fuels","Transport & Fuels",
    "Transport & Fuels","Transport & Fuels",
    "Carbon Removal & Nature","Carbon Removal & Nature","Carbon Removal & Nature","Carbon Removal & Nature",
    "Carbon Removal & Nature","Carbon Removal & Nature",
    "Building & Efficiency",
    "Circular Economy","Circular Economy",
    "Digital Infrastructure",
]

CAT_STYLE = {
    "Clean Energy Generation":    ("cat-energy",    "⚡"),
    "Energy Storage & Grid":      ("cat-storage",   "🔋"),
    "Industrial Decarbonisation": ("cat-industrial","🏭"),
    "Transport & Fuels":          ("cat-transport", "🚗"),
    "Carbon Removal & Nature":    ("cat-carbon",    "🌿"),
    "Building & Efficiency":      ("cat-building",  "🏢"),
    "Circular Economy":           ("cat-circular",  "♻️"),
    "Digital Infrastructure":     ("cat-storage",   "💻"),
}

TECH_SHORT = [
    "Solar PV","Onshore Wind","Offshore Wind","Float. Offshore","CSP","Ocean/Tidal","SMR","Geothermal","Green H₂",
    "Battery Stor.","LDES","Smart Grid","HVDC","VPP",
    "Steel/Cement","EAF","Green Al","Low-C Concrete","Green NH3","H₂ Chem","Ind. Heat Pump",
    "SAF","HVO","E-kerosene","E-Ammonia","E-Methanol","E-diesel","Biogas","Biomethane","EVs","H₂ Fuel Cell","eVTOL","Rail Electrif.",
    "CCUS","BECCS","DAC","W2E+CCS","Reforestation","Blue Carbon",
    "Bldg Efficiency",
    "Chem Recycling","Critical Min.",
    "Green Data Ctr",
]

MBM_MATRIX = [
    ('D','D',None,'D',None,'I',None,None,'D',None,None),
    ('D','D',None,'D',None,None,None,None,'D',None,None),
    ('D','D',None,'D',None,None,None,None,'D',None,None),
    ('D','D',None,'D',None,None,None,None,'D',None,None),
    ('D','D',None,'D',None,None,None,None,'D',None,None),
    ('D','D',None,'D',None,None,None,None,'D',None,None),
    ('D','D',None,'D',None,None,None,None,'I',None,None),
    ('D','D',None,'D',None,None,None,None,'D',None,None),
    ('D','D','D','I','D','D',None,'D','D','D',None),
    ('D','D',None,'D',None,None,None,None,'D',None,None),
    ('D','D',None,'D',None,None,None,None,'D',None,None),
    ('I',None,None,None,None,None,None,None,'I',None,None),
    ('I',None,None,None,None,None,None,None,None,None,None),
    ('I',None,None,None,None,None,None,None,'I',None,None),
    ('D','D',None,None,'D','D',None,None,'D','D',None),
    ('D','D',None,None,'D','D',None,None,'D','D',None),
    ('D','D',None,None,'D','D',None,None,'D',None,None),
    ('D','D',None,None,'D','D',None,None,'D','D',None),
    ('D','D',None,None,'D','D',None,None,'D',None,None),
    ('D','D',None,None,'D','D',None,None,'D',None,None),
    ('D','D',None,None,'D',None,None,None,'D',None,None),
    ('D','D','D','D','D',None,'D',None,'D','D',None),
    ('D','D','D',None,None,None,'D',None,'D',None,None),
    ('D','D','D','D','D',None,'D',None,'D',None,None),
    ('D','D','D',None,'D','I',None,'D','D',None,None),
    ('D','D','D',None,'D',None,None,'D','D',None,None),
    ('D','D','D',None,'D',None,None,'D','D',None,None),
    ('D','D','D',None,None,None,None,None,'D',None,None),
    ('D','D','D',None,None,None,None,None,'D',None,None),
    ('D','D',None,None,None,None,None,None,None,None,'D'),
    ('D','D',None,None,'D',None,None,None,'D',None,'D'),
    ('D','D',None,None,None,None,'D',None,'D',None,None),
    ('D','D',None,None,None,None,None,None,'D',None,None),
    ('D','D',None,None,'D',None,None,None,'D','D',None),
    ('D','D','D','D','D',None,None,None,'D','D',None),
    ('D','D','I',None,'D',None,None,None,'D','D',None),
    ('D','D',None,None,'D',None,None,None,'D',None,None),
    ('D','I',None,None,None,None,'D',None,'D',None,None),
    (None,None,None,None,None,None,'D',None,'D',None,None),
    ('D','D',None,None,None,None,None,None,'D',None,None),
    ('D','D',None,None,'D',None,None,None,'D',None,None),
    ('D','D',None,None,None,'D',None,None,None,None,None),
    ('D','D',None,None,None,None,None,None,'D',None,None),
]

MBM_MECH_NAMES = ["ETS","Carbon Tax","Fuel Mandate","CfD","CCfD","CBAM","CORSIA","IMO Levy","VCM/CDM","AMC","Feebate"]

# ─────────────────────────────────────────────────────────────────
# COUNTRY DATA FROM EXCEL (194 countries, Country Level sheet)
# ─────────────────────────────────────────────────────────────────
COUNTRY_DATA_RAW = {"Afghanistan":{"region":"South Asia","iso3":"AFG","techs":{"Sustainable Aviation Fuel (SAF)":{"CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"CORSIA":"D"},"E-Ammonia (maritime fuel)":{"IMO Levy":"D"},"E-Methanol (maritime fuel)":{"IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"IMO Levy":"I"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Angola":{"region":"Southern Africa","iso3":"AGO","techs":{"Solar PV":{"VCM":"D"},"Concentrated Solar Power (CSP)":{"VCM":"D"},"Enhanced Geothermal Systems (EGS)":{"CDM/PACM":"D"},"Sustainable Aviation Fuel (SAF)":{"CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"CORSIA":"D"},"E-Ammonia (maritime fuel)":{"IMO Levy":"D"},"E-Methanol (maritime fuel)":{"IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"IMO Levy":"I"},"Reforestation / REDD+ / NBS":{"VCM":"D"},"Blue Carbon (mangroves, seagrass)":{"VCM":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Albania":{"region":"Southern Europe","iso3":"ALB","techs":{"Solar PV":{"Carbon Tax":"D"},"Onshore Wind":{"Carbon Tax":"D"},"Offshore Wind (fixed foundation)":{"Carbon Tax":"D"},"Floating Offshore Wind":{"Carbon Tax":"D"},"Concentrated Solar Power (CSP)":{"Carbon Tax":"D"},"Ocean / Tidal / Wave Energy":{"Carbon Tax":"D"},"Small Modular Reactors (SMR)":{"Carbon Tax":"D"},"Enhanced Geothermal Systems (EGS)":{"Carbon Tax":"D"},"Green Hydrogen (electrolysis)":{"Carbon Tax":"D","IMO Levy":"D"},"Battery Storage (grid-scale)":{"Carbon Tax":"D"},"Long-Duration Energy Storage (LDES)":{"Carbon Tax":"D"},"Low-carbon Steel & Cement":{"Carbon Tax":"D"},"Electric Arc Furnace (EAF)":{"Carbon Tax":"D"},"Green Aluminium":{"Carbon Tax":"D"},"Low-carbon Concrete":{"Carbon Tax":"D"},"Green Fertilizer (low-carbon NH3)":{"Carbon Tax":"D"},"Hydrogen-based Chemicals":{"Carbon Tax":"D"},"Industrial Heat Pumps (high-temp)":{"Carbon Tax":"D"},"Sustainable Aviation Fuel (SAF)":{"Carbon Tax":"D","CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"Carbon Tax":"D","CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"Carbon Tax":"D","CORSIA":"D"},"E-Ammonia (maritime fuel)":{"Carbon Tax":"D","IMO Levy":"D"},"E-Methanol (maritime fuel)":{"Carbon Tax":"D","IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"Carbon Tax":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"Carbon Tax":"D"},"Biomethane (upgraded to grid)":{"Carbon Tax":"D"},"Carbon Capture & Storage (CCUS)":{"Carbon Tax":"D"},"BECCS (Bioenergy + CCS)":{"Carbon Tax":"D"},"Direct Air Capture (DAC)":{"Carbon Tax":"D"},"Waste-to-Energy + CCS":{"Carbon Tax":"D"},"Reforestation / REDD+ / NBS":{"Carbon Tax":"I"},"Building Energy Efficiency / Retrofits":{"Carbon Tax":"D"},"Advanced / Chemical Recycling":{"Carbon Tax":"D"},"Critical Minerals Processing (low-C)":{"Carbon Tax":"D"},"Green Data Centers":{"Carbon Tax":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Andorra":{"region":"Southern Europe","iso3":"AND","techs":{"Green Hydrogen (electrolysis)":{"IMO Levy":"D"},"Sustainable Aviation Fuel (SAF)":{"CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"CORSIA":"D"},"E-Ammonia (maritime fuel)":{"IMO Levy":"D"},"E-Methanol (maritime fuel)":{"IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"IMO Levy":"I"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"United Arab Emirates":{"region":"West Asia (Middle East)","iso3":"ARE","techs":{"Enhanced Geothermal Systems (EGS)":{"CDM/PACM":"D"},"Green Hydrogen (electrolysis)":{"Fuel Mandate":"D","IMO Levy":"D"},"Sustainable Aviation Fuel (SAF)":{"Fuel Mandate":"D","CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"Fuel Mandate":"D","CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"Fuel Mandate":"D","CORSIA":"D"},"E-Ammonia (maritime fuel)":{"Fuel Mandate":"D","IMO Levy":"D"},"E-Methanol (maritime fuel)":{"Fuel Mandate":"D","IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"Fuel Mandate":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"Fuel Mandate":"D"},"Biomethane (upgraded to grid)":{"Fuel Mandate":"D"},"BECCS (Bioenergy + CCS)":{"Fuel Mandate":"D"},"Direct Air Capture (DAC)":{"Fuel Mandate":"I"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Argentina":{"region":"South America","iso3":"ARG","techs":{"Solar PV":{"VCM":"D"},"Onshore Wind":{"VCM":"D"},"Concentrated Solar Power (CSP)":{"VCM":"D"},"Ocean / Tidal / Wave Energy":{"VCM":"D"},"Small Modular Reactors (SMR)":{"VCM":"I"},"Enhanced Geothermal Systems (EGS)":{"VCM":"D","CDM/PACM":"D"},"Green Hydrogen (electrolysis)":{"IMO Levy":"D","VCM":"D"},"Battery Storage (grid-scale)":{"VCM":"D"},"Long-Duration Energy Storage (LDES)":{"VCM":"D"},"Sustainable Aviation Fuel (SAF)":{"CORSIA":"D","VCM":"D"},"HVO (Hydrotreated Vegetable Oil)":{"CORSIA":"I","IMO Levy":"I","VCM":"D"},"E-kerosene (aviation e-fuel)":{"CORSIA":"D","VCM":"D"},"E-Ammonia (maritime fuel)":{"IMO Levy":"D","VCM":"D"},"E-Methanol (maritime fuel)":{"IMO Levy":"D","VCM":"D"},"E-diesel / E-methanol (road & ship)":{"IMO Levy":"I"},"Biogas (anaerobic digestion)":{"VCM":"D"},"Biomethane (upgraded to grid)":{"VCM":"D"},"Carbon Capture & Storage (CCUS)":{"VCM":"D"},"BECCS (Bioenergy + CCS)":{"VCM":"D"},"Direct Air Capture (DAC)":{"VCM":"D"},"Waste-to-Energy + CCS":{"VCM":"D"},"Reforestation / REDD+ / NBS":{"VCM":"D"},"Blue Carbon (mangroves, seagrass)":{"VCM":"D"},"Building Energy Efficiency / Retrofits":{"VCM":"D"},"Advanced / Chemical Recycling":{"VCM":"D"},"Green Data Centers":{"VCM":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Armenia":{"region":"West Asia (Middle East)","iso3":"ARM","techs":{"Green Hydrogen (electrolysis)":{"IMO Levy":"D"},"Sustainable Aviation Fuel (SAF)":{"CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"CORSIA":"D"},"E-Ammonia (maritime fuel)":{"IMO Levy":"D"},"E-Methanol (maritime fuel)":{"IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"IMO Levy":"I"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Antigua and Barbuda":{"region":"Caribbean","iso3":"ATG","techs":{"Green Hydrogen (electrolysis)":{"IMO Levy":"D"},"Sustainable Aviation Fuel (SAF)":{"CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"CORSIA":"D"},"E-Ammonia (maritime fuel)":{"IMO Levy":"D"},"E-Methanol (maritime fuel)":{"IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"IMO Levy":"I"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Australia":{"region":"Australia & New Zealand","iso3":"AUS","techs":{"Solar PV":{"ETS":"D","VCM":"D"},"Onshore Wind":{"ETS":"D","VCM":"D"},"Offshore Wind (fixed foundation)":{"ETS":"D"},"Floating Offshore Wind":{"ETS":"D"},"Concentrated Solar Power (CSP)":{"ETS":"D","VCM":"D"},"Ocean / Tidal / Wave Energy":{"ETS":"D","VCM":"D"},"Small Modular Reactors (SMR)":{"ETS":"D","VCM":"I"},"Enhanced Geothermal Systems (EGS)":{"ETS":"D","VCM":"D"},"Green Hydrogen (electrolysis)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"Battery Storage (grid-scale)":{"ETS":"D","VCM":"D"},"Long-Duration Energy Storage (LDES)":{"ETS":"D","VCM":"D"},"Low-carbon Steel & Cement":{"ETS":"D","VCM":"D"},"Electric Arc Furnace (EAF)":{"ETS":"D","VCM":"D"},"Green Aluminium":{"ETS":"D","VCM":"D"},"Low-carbon Concrete":{"ETS":"D","VCM":"D"},"Green Fertilizer (low-carbon NH3)":{"ETS":"D","VCM":"D"},"Hydrogen-based Chemicals":{"ETS":"D","VCM":"D"},"Industrial Heat Pumps (high-temp)":{"ETS":"D","VCM":"D"},"Sustainable Aviation Fuel (SAF)":{"ETS":"D","CORSIA":"D","VCM":"D"},"HVO (Hydrotreated Vegetable Oil)":{"ETS":"D","CORSIA":"I","IMO Levy":"I","VCM":"D"},"E-kerosene (aviation e-fuel)":{"ETS":"D","CORSIA":"D","VCM":"D"},"E-Ammonia (maritime fuel)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"E-Methanol (maritime fuel)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"E-diesel / E-methanol (road & ship)":{"ETS":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"ETS":"D","VCM":"D"},"Biomethane (upgraded to grid)":{"ETS":"D","VCM":"D"},"Carbon Capture & Storage (CCUS)":{"ETS":"D","VCM":"D"},"BECCS (Bioenergy + CCS)":{"ETS":"D","VCM":"D"},"Direct Air Capture (DAC)":{"ETS":"D","VCM":"D"},"Waste-to-Energy + CCS":{"ETS":"D","VCM":"D"},"Reforestation / REDD+ / NBS":{"ETS":"D","VCM":"D"},"Blue Carbon (mangroves, seagrass)":{"VCM":"D"},"Building Energy Efficiency / Retrofits":{"ETS":"D","VCM":"D"},"Advanced / Chemical Recycling":{"ETS":"D","VCM":"D"},"Critical Minerals Processing (low-C)":{"ETS":"D"},"Green Data Centers":{"ETS":"D","VCM":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Austria":{"region":"Western Europe","iso3":"AUT","techs":{"Solar PV":{"ETS":"D","CBAM":"I"},"Onshore Wind":{"ETS":"D","CBAM":"I"},"Offshore Wind (fixed foundation)":{"ETS":"D","CBAM":"I"},"Floating Offshore Wind":{"ETS":"D","CBAM":"I"},"Concentrated Solar Power (CSP)":{"ETS":"D","CBAM":"I"},"Ocean / Tidal / Wave Energy":{"ETS":"D","CBAM":"I"},"Small Modular Reactors (SMR)":{"ETS":"D","CBAM":"I"},"Enhanced Geothermal Systems (EGS)":{"ETS":"D","CBAM":"I"},"Green Hydrogen (electrolysis)":{"ETS":"D","CBAM":"D","IMO Levy":"D"},"Battery Storage (grid-scale)":{"ETS":"D","CBAM":"I"},"Long-Duration Energy Storage (LDES)":{"ETS":"D","CBAM":"I"},"Low-carbon Steel & Cement":{"ETS":"D","CBAM":"D"},"Electric Arc Furnace (EAF)":{"ETS":"D","CBAM":"D"},"Green Aluminium":{"ETS":"D","CBAM":"D"},"Low-carbon Concrete":{"ETS":"D","CBAM":"D"},"Green Fertilizer (low-carbon NH3)":{"ETS":"D","CBAM":"D"},"Hydrogen-based Chemicals":{"ETS":"D","CBAM":"D"},"Industrial Heat Pumps (high-temp)":{"ETS":"D"},"Sustainable Aviation Fuel (SAF)":{"ETS":"D","CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"ETS":"D","CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"ETS":"D","CORSIA":"D"},"E-Ammonia (maritime fuel)":{"ETS":"D","IMO Levy":"D"},"E-Methanol (maritime fuel)":{"ETS":"D","IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"ETS":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"ETS":"D"},"Biomethane (upgraded to grid)":{"ETS":"D"},"Carbon Capture & Storage (CCUS)":{"ETS":"D"},"BECCS (Bioenergy + CCS)":{"ETS":"D"},"Direct Air Capture (DAC)":{"ETS":"D"},"Waste-to-Energy + CCS":{"ETS":"D"},"Reforestation / REDD+ / NBS":{"ETS":"D"},"Building Energy Efficiency / Retrofits":{"ETS":"D"},"Advanced / Chemical Recycling":{"ETS":"D"},"Critical Minerals Processing (low-C)":{"ETS":"D","CBAM":"D"},"Green Data Centers":{"ETS":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Azerbaijan":{"region":"West Asia (Middle East)","iso3":"AZE","techs":{"Green Hydrogen (electrolysis)":{"IMO Levy":"D"},"Sustainable Aviation Fuel (SAF)":{"CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"CORSIA":"D"},"E-Ammonia (maritime fuel)":{"IMO Levy":"D"},"E-Methanol (maritime fuel)":{"IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"IMO Levy":"I"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Burundi":{"region":"East Africa","iso3":"BDI","techs":{"Green Hydrogen (electrolysis)":{"IMO Levy":"D"},"Sustainable Aviation Fuel (SAF)":{"CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"CORSIA":"D"},"E-Ammonia (maritime fuel)":{"IMO Levy":"D"},"E-Methanol (maritime fuel)":{"IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"IMO Levy":"I"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Belgium":{"region":"Western Europe","iso3":"BEL","techs":{"Solar PV":{"ETS":"D","CBAM":"I"},"Onshore Wind":{"ETS":"D","CBAM":"I"},"Offshore Wind (fixed foundation)":{"ETS":"D","CBAM":"I"},"Floating Offshore Wind":{"ETS":"D","CBAM":"I"},"Concentrated Solar Power (CSP)":{"ETS":"D","CBAM":"I"},"Ocean / Tidal / Wave Energy":{"ETS":"D","CBAM":"I"},"Small Modular Reactors (SMR)":{"ETS":"D","CBAM":"I"},"Enhanced Geothermal Systems (EGS)":{"ETS":"D","CBAM":"I"},"Green Hydrogen (electrolysis)":{"ETS":"D","CBAM":"D","IMO Levy":"D"},"Battery Storage (grid-scale)":{"ETS":"D","CBAM":"I"},"Long-Duration Energy Storage (LDES)":{"ETS":"D","CBAM":"I"},"Low-carbon Steel & Cement":{"ETS":"D","CBAM":"D"},"Electric Arc Furnace (EAF)":{"ETS":"D","CBAM":"D"},"Green Aluminium":{"ETS":"D","CBAM":"D"},"Low-carbon Concrete":{"ETS":"D","CBAM":"D"},"Green Fertilizer (low-carbon NH3)":{"ETS":"D","CBAM":"D"},"Hydrogen-based Chemicals":{"ETS":"D","CBAM":"D"},"Industrial Heat Pumps (high-temp)":{"ETS":"D"},"Sustainable Aviation Fuel (SAF)":{"ETS":"D","CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"ETS":"D","CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"ETS":"D","CORSIA":"D"},"E-Ammonia (maritime fuel)":{"ETS":"D","IMO Levy":"D"},"E-Methanol (maritime fuel)":{"ETS":"D","IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"ETS":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"ETS":"D"},"Biomethane (upgraded to grid)":{"ETS":"D"},"Carbon Capture & Storage (CCUS)":{"ETS":"D"},"BECCS (Bioenergy + CCS)":{"ETS":"D"},"Direct Air Capture (DAC)":{"ETS":"D"},"Waste-to-Energy + CCS":{"ETS":"D"},"Reforestation / REDD+ / NBS":{"ETS":"D"},"Building Energy Efficiency / Retrofits":{"ETS":"D"},"Advanced / Chemical Recycling":{"ETS":"D"},"Critical Minerals Processing (low-C)":{"ETS":"D","CBAM":"D"},"Green Data Centers":{"ETS":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Germany":{"region":"Western Europe","iso3":"DEU","techs":{"Solar PV":{"ETS":"D","CBAM":"I"},"Onshore Wind":{"ETS":"D","CBAM":"I"},"Offshore Wind (fixed foundation)":{"ETS":"D","CBAM":"I"},"Floating Offshore Wind":{"ETS":"D","CBAM":"I"},"Concentrated Solar Power (CSP)":{"ETS":"D","CBAM":"I"},"Ocean / Tidal / Wave Energy":{"ETS":"D","CBAM":"I"},"Small Modular Reactors (SMR)":{"ETS":"D","CBAM":"I"},"Enhanced Geothermal Systems (EGS)":{"ETS":"D","CBAM":"I"},"Green Hydrogen (electrolysis)":{"ETS":"D","CBAM":"D","IMO Levy":"D"},"Battery Storage (grid-scale)":{"ETS":"D","CBAM":"I"},"Long-Duration Energy Storage (LDES)":{"ETS":"D","CBAM":"I"},"Low-carbon Steel & Cement":{"ETS":"D","CBAM":"D"},"Electric Arc Furnace (EAF)":{"ETS":"D","CBAM":"D"},"Green Aluminium":{"ETS":"D","CBAM":"D"},"Low-carbon Concrete":{"ETS":"D","CBAM":"D"},"Green Fertilizer (low-carbon NH3)":{"ETS":"D","CBAM":"D"},"Hydrogen-based Chemicals":{"ETS":"D","CBAM":"D"},"Industrial Heat Pumps (high-temp)":{"ETS":"D"},"Sustainable Aviation Fuel (SAF)":{"ETS":"D","CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"ETS":"D","CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"ETS":"D","CORSIA":"D"},"E-Ammonia (maritime fuel)":{"ETS":"D","IMO Levy":"D"},"E-Methanol (maritime fuel)":{"ETS":"D","IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"ETS":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"ETS":"D"},"Biomethane (upgraded to grid)":{"ETS":"D"},"Carbon Capture & Storage (CCUS)":{"ETS":"D"},"BECCS (Bioenergy + CCS)":{"ETS":"D"},"Direct Air Capture (DAC)":{"ETS":"D"},"Waste-to-Energy + CCS":{"ETS":"D"},"Reforestation / REDD+ / NBS":{"ETS":"D"},"Building Energy Efficiency / Retrofits":{"ETS":"D"},"Advanced / Chemical Recycling":{"ETS":"D"},"Critical Minerals Processing (low-C)":{"ETS":"D","CBAM":"D"},"Green Data Centers":{"ETS":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"France":{"region":"Western Europe","iso3":"FRA","techs":{"Solar PV":{"ETS":"D","Carbon Tax":"D","CBAM":"I","VCM":"D"},"Onshore Wind":{"ETS":"D","Carbon Tax":"D","CBAM":"I"},"Offshore Wind (fixed foundation)":{"ETS":"D","Carbon Tax":"D","CBAM":"I"},"Floating Offshore Wind":{"ETS":"D","Carbon Tax":"D","CBAM":"I"},"Concentrated Solar Power (CSP)":{"ETS":"D","Carbon Tax":"D","CBAM":"I"},"Ocean / Tidal / Wave Energy":{"ETS":"D","Carbon Tax":"D","CBAM":"I"},"Small Modular Reactors (SMR)":{"ETS":"D","Carbon Tax":"D","CBAM":"I"},"Enhanced Geothermal Systems (EGS)":{"ETS":"D","Carbon Tax":"D","CBAM":"I"},"Green Hydrogen (electrolysis)":{"ETS":"D","Carbon Tax":"D","CBAM":"D","IMO Levy":"D"},"Battery Storage (grid-scale)":{"ETS":"D","Carbon Tax":"D","CBAM":"I"},"Long-Duration Energy Storage (LDES)":{"ETS":"D","Carbon Tax":"D","CBAM":"I"},"Low-carbon Steel & Cement":{"ETS":"D","Carbon Tax":"D","CBAM":"D"},"Electric Arc Furnace (EAF)":{"ETS":"D","Carbon Tax":"D","CBAM":"D"},"Green Aluminium":{"ETS":"D","Carbon Tax":"D","CBAM":"D"},"Low-carbon Concrete":{"ETS":"D","Carbon Tax":"D","CBAM":"D"},"Green Fertilizer (low-carbon NH3)":{"ETS":"D","Carbon Tax":"D","CBAM":"D"},"Hydrogen-based Chemicals":{"ETS":"D","Carbon Tax":"D","CBAM":"D"},"Industrial Heat Pumps (high-temp)":{"ETS":"D","Carbon Tax":"D"},"Sustainable Aviation Fuel (SAF)":{"ETS":"D","Carbon Tax":"D","CORSIA":"D"},"HVO (Hydrotreated Vegetable Oil)":{"ETS":"D","Carbon Tax":"D","CORSIA":"I","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"ETS":"D","Carbon Tax":"D","CORSIA":"D"},"E-Ammonia (maritime fuel)":{"ETS":"D","Carbon Tax":"D","IMO Levy":"D"},"E-Methanol (maritime fuel)":{"ETS":"D","Carbon Tax":"D","IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"ETS":"D","Carbon Tax":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"ETS":"D","Carbon Tax":"D"},"Biomethane (upgraded to grid)":{"ETS":"D","Carbon Tax":"D"},"Carbon Capture & Storage (CCUS)":{"ETS":"D","Carbon Tax":"D"},"BECCS (Bioenergy + CCS)":{"ETS":"D","Carbon Tax":"D"},"Direct Air Capture (DAC)":{"ETS":"D","Carbon Tax":"D"},"Waste-to-Energy + CCS":{"ETS":"D","Carbon Tax":"D"},"Reforestation / REDD+ / NBS":{"ETS":"D","Carbon Tax":"I"},"Building Energy Efficiency / Retrofits":{"ETS":"D","Carbon Tax":"D"},"Advanced / Chemical Recycling":{"ETS":"D","Carbon Tax":"D"},"Critical Minerals Processing (low-C)":{"ETS":"D","Carbon Tax":"D","CBAM":"D"},"Green Data Centers":{"ETS":"D","Carbon Tax":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"United Kingdom":{"region":"Northern Europe","iso3":"GBR","techs":{"Solar PV":{"ETS":"D","VCM":"D"},"Onshore Wind":{"ETS":"D","VCM":"D"},"Offshore Wind (fixed foundation)":{"ETS":"D"},"Floating Offshore Wind":{"ETS":"D"},"Concentrated Solar Power (CSP)":{"ETS":"D","VCM":"D"},"Ocean / Tidal / Wave Energy":{"ETS":"D","VCM":"D"},"Small Modular Reactors (SMR)":{"ETS":"D","VCM":"I"},"Enhanced Geothermal Systems (EGS)":{"ETS":"D","VCM":"D"},"Green Hydrogen (electrolysis)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"Battery Storage (grid-scale)":{"ETS":"D","VCM":"D"},"Long-Duration Energy Storage (LDES)":{"ETS":"D","VCM":"D"},"Low-carbon Steel & Cement":{"ETS":"D","VCM":"D"},"Electric Arc Furnace (EAF)":{"ETS":"D","VCM":"D"},"Green Aluminium":{"ETS":"D","VCM":"D"},"Low-carbon Concrete":{"ETS":"D","VCM":"D"},"Green Fertilizer (low-carbon NH3)":{"ETS":"D","VCM":"D"},"Hydrogen-based Chemicals":{"ETS":"D","VCM":"D"},"Industrial Heat Pumps (high-temp)":{"ETS":"D","VCM":"D"},"Sustainable Aviation Fuel (SAF)":{"ETS":"D","CORSIA":"D","VCM":"D"},"HVO (Hydrotreated Vegetable Oil)":{"ETS":"D","CORSIA":"I","IMO Levy":"I","VCM":"D"},"E-kerosene (aviation e-fuel)":{"ETS":"D","CORSIA":"D","VCM":"D"},"E-Ammonia (maritime fuel)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"E-Methanol (maritime fuel)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"E-diesel / E-methanol (road & ship)":{"ETS":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"ETS":"D","VCM":"D"},"Biomethane (upgraded to grid)":{"ETS":"D","VCM":"D"},"Carbon Capture & Storage (CCUS)":{"ETS":"D","VCM":"D"},"BECCS (Bioenergy + CCS)":{"ETS":"D","VCM":"D"},"Direct Air Capture (DAC)":{"ETS":"D","VCM":"D"},"Waste-to-Energy + CCS":{"ETS":"D","VCM":"D"},"Reforestation / REDD+ / NBS":{"ETS":"D","VCM":"D"},"Blue Carbon (mangroves, seagrass)":{"VCM":"D"},"Building Energy Efficiency / Retrofits":{"ETS":"D","VCM":"D"},"Advanced / Chemical Recycling":{"ETS":"D","VCM":"D"},"Critical Minerals Processing (low-C)":{"ETS":"D"},"Green Data Centers":{"ETS":"D","VCM":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"China":{"region":"East Asia","iso3":"CHN","techs":{"Solar PV":{"ETS":"D"},"Onshore Wind":{"ETS":"D"},"Offshore Wind (fixed foundation)":{"ETS":"D"},"Floating Offshore Wind":{"ETS":"D"},"Concentrated Solar Power (CSP)":{"ETS":"D"},"Ocean / Tidal / Wave Energy":{"ETS":"D"},"Small Modular Reactors (SMR)":{"ETS":"D"},"Enhanced Geothermal Systems (EGS)":{"ETS":"D"},"Green Hydrogen (electrolysis)":{"ETS":"D","IMO Levy":"D"},"Battery Storage (grid-scale)":{"ETS":"D"},"Long-Duration Energy Storage (LDES)":{"ETS":"D"},"Low-carbon Steel & Cement":{"ETS":"D"},"Electric Arc Furnace (EAF)":{"ETS":"D"},"Green Aluminium":{"ETS":"D"},"Low-carbon Concrete":{"ETS":"D"},"Green Fertilizer (low-carbon NH3)":{"ETS":"D"},"Hydrogen-based Chemicals":{"ETS":"D"},"Industrial Heat Pumps (high-temp)":{"ETS":"D"},"Sustainable Aviation Fuel (SAF)":{"ETS":"D"},"HVO (Hydrotreated Vegetable Oil)":{"ETS":"D","IMO Levy":"I"},"E-kerosene (aviation e-fuel)":{"ETS":"D"},"E-Ammonia (maritime fuel)":{"ETS":"D","IMO Levy":"D"},"E-Methanol (maritime fuel)":{"ETS":"D","IMO Levy":"D"},"E-diesel / E-methanol (road & ship)":{"ETS":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"ETS":"D"},"Biomethane (upgraded to grid)":{"ETS":"D"},"Carbon Capture & Storage (CCUS)":{"ETS":"D"},"BECCS (Bioenergy + CCS)":{"ETS":"D"},"Direct Air Capture (DAC)":{"ETS":"D"},"Waste-to-Energy + CCS":{"ETS":"D"},"Reforestation / REDD+ / NBS":{"ETS":"D"},"Building Energy Efficiency / Retrofits":{"ETS":"D"},"Advanced / Chemical Recycling":{"ETS":"D"},"Critical Minerals Processing (low-C)":{"ETS":"D"},"Green Data Centers":{"ETS":"D"}}},"Japan":{"region":"East Asia","iso3":"JPN","techs":{"Solar PV":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Onshore Wind":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Offshore Wind (fixed foundation)":{"ETS":"D","Carbon Tax":"D"},"Floating Offshore Wind":{"ETS":"D","Carbon Tax":"D"},"Concentrated Solar Power (CSP)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Ocean / Tidal / Wave Energy":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Small Modular Reactors (SMR)":{"ETS":"D","Carbon Tax":"D","VCM":"I"},"Enhanced Geothermal Systems (EGS)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Green Hydrogen (electrolysis)":{"ETS":"D","Carbon Tax":"D","IMO Levy":"D","VCM":"D"},"Battery Storage (grid-scale)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Long-Duration Energy Storage (LDES)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Low-carbon Steel & Cement":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Electric Arc Furnace (EAF)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Green Aluminium":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Low-carbon Concrete":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Green Fertilizer (low-carbon NH3)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Hydrogen-based Chemicals":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Industrial Heat Pumps (high-temp)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Sustainable Aviation Fuel (SAF)":{"ETS":"D","Carbon Tax":"D","CORSIA":"D","VCM":"D"},"HVO (Hydrotreated Vegetable Oil)":{"ETS":"D","Carbon Tax":"D","CORSIA":"I","IMO Levy":"I","VCM":"D"},"E-kerosene (aviation e-fuel)":{"ETS":"D","Carbon Tax":"D","CORSIA":"D","VCM":"D"},"E-Ammonia (maritime fuel)":{"ETS":"D","Carbon Tax":"D","IMO Levy":"D","VCM":"D"},"E-Methanol (maritime fuel)":{"ETS":"D","Carbon Tax":"D","IMO Levy":"D","VCM":"D"},"E-diesel / E-methanol (road & ship)":{"ETS":"D","Carbon Tax":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Biomethane (upgraded to grid)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Carbon Capture & Storage (CCUS)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"BECCS (Bioenergy + CCS)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Direct Air Capture (DAC)":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Waste-to-Energy + CCS":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Reforestation / REDD+ / NBS":{"ETS":"D","Carbon Tax":"I","VCM":"D"},"Blue Carbon (mangroves, seagrass)":{"VCM":"D"},"Building Energy Efficiency / Retrofits":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Advanced / Chemical Recycling":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Critical Minerals Processing (low-C)":{"ETS":"D","Carbon Tax":"D"},"Green Data Centers":{"ETS":"D","Carbon Tax":"D","VCM":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"United States":{"region":"North America","iso3":"USA","techs":{"Solar PV":{"ETS":"D","VCM":"D"},"Onshore Wind":{"ETS":"D","VCM":"D"},"Offshore Wind (fixed foundation)":{"ETS":"D"},"Floating Offshore Wind":{"ETS":"D"},"Concentrated Solar Power (CSP)":{"ETS":"D","VCM":"D"},"Ocean / Tidal / Wave Energy":{"ETS":"D","VCM":"D"},"Small Modular Reactors (SMR)":{"ETS":"D","VCM":"I"},"Enhanced Geothermal Systems (EGS)":{"ETS":"D","VCM":"D"},"Green Hydrogen (electrolysis)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"Battery Storage (grid-scale)":{"ETS":"D","VCM":"D"},"Long-Duration Energy Storage (LDES)":{"ETS":"D","VCM":"D"},"Low-carbon Steel & Cement":{"ETS":"D","VCM":"D"},"Electric Arc Furnace (EAF)":{"ETS":"D","VCM":"D"},"Green Aluminium":{"ETS":"D","VCM":"D"},"Low-carbon Concrete":{"ETS":"D","VCM":"D"},"Green Fertilizer (low-carbon NH3)":{"ETS":"D","VCM":"D"},"Hydrogen-based Chemicals":{"ETS":"D","VCM":"D"},"Industrial Heat Pumps (high-temp)":{"ETS":"D","VCM":"D"},"Sustainable Aviation Fuel (SAF)":{"ETS":"D","CORSIA":"D","VCM":"D"},"HVO (Hydrotreated Vegetable Oil)":{"ETS":"D","CORSIA":"I","IMO Levy":"I","VCM":"D"},"E-kerosene (aviation e-fuel)":{"ETS":"D","CORSIA":"D","VCM":"D"},"E-Ammonia (maritime fuel)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"E-Methanol (maritime fuel)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"E-diesel / E-methanol (road & ship)":{"ETS":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"ETS":"D","VCM":"D"},"Biomethane (upgraded to grid)":{"ETS":"D","VCM":"D"},"Carbon Capture & Storage (CCUS)":{"ETS":"D","VCM":"D"},"BECCS (Bioenergy + CCS)":{"ETS":"D","VCM":"D"},"Direct Air Capture (DAC)":{"ETS":"D","VCM":"D"},"Waste-to-Energy + CCS":{"ETS":"D","VCM":"D"},"Reforestation / REDD+ / NBS":{"ETS":"D","VCM":"D"},"Blue Carbon (mangroves, seagrass)":{"VCM":"D"},"Building Energy Efficiency / Retrofits":{"ETS":"D","VCM":"D"},"Advanced / Chemical Recycling":{"ETS":"D","VCM":"D"},"Critical Minerals Processing (low-C)":{"ETS":"D"},"Green Data Centers":{"ETS":"D","VCM":"D"}}},"India":{"region":"South Asia","iso3":"IND","techs":{"Solar PV":{"VCM":"D"},"Onshore Wind":{"VCM":"D"},"Concentrated Solar Power (CSP)":{"VCM":"D"},"Ocean / Tidal / Wave Energy":{"VCM":"D"},"Enhanced Geothermal Systems (EGS)":{"CDM/PACM":"D"},"Green Hydrogen (electrolysis)":{"IMO Levy":"D","VCM":"D"},"Battery Storage (grid-scale)":{"VCM":"D"},"Long-Duration Energy Storage (LDES)":{"VCM":"D"},"Sustainable Aviation Fuel (SAF)":{"CORSIA":"D","VCM":"D"},"HVO (Hydrotreated Vegetable Oil)":{"CORSIA":"I","IMO Levy":"I","VCM":"D"},"E-kerosene (aviation e-fuel)":{"CORSIA":"D","VCM":"D"},"E-Ammonia (maritime fuel)":{"IMO Levy":"D","VCM":"D"},"E-Methanol (maritime fuel)":{"IMO Levy":"D","VCM":"D"},"E-diesel / E-methanol (road & ship)":{"IMO Levy":"I"},"Biogas (anaerobic digestion)":{"VCM":"D"},"Biomethane (upgraded to grid)":{"VCM":"D"},"Carbon Capture & Storage (CCUS)":{"VCM":"D"},"BECCS (Bioenergy + CCS)":{"VCM":"D"},"Direct Air Capture (DAC)":{"VCM":"D"},"Waste-to-Energy + CCS":{"VCM":"D"},"Reforestation / REDD+ / NBS":{"VCM":"D"},"Blue Carbon (mangroves, seagrass)":{"VCM":"D"},"Building Energy Efficiency / Retrofits":{"VCM":"D"},"Advanced / Chemical Recycling":{"VCM":"D"},"Green Data Centers":{"VCM":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Brazil":{"region":"South America","iso3":"BRA","techs":{"Solar PV":{"VCM":"D"},"Onshore Wind":{"VCM":"D"},"Concentrated Solar Power (CSP)":{"VCM":"D"},"Ocean / Tidal / Wave Energy":{"VCM":"D"},"Enhanced Geothermal Systems (EGS)":{"VCM":"D","CDM/PACM":"D"},"Green Hydrogen (electrolysis)":{"IMO Levy":"D","VCM":"D"},"Battery Storage (grid-scale)":{"VCM":"D"},"Long-Duration Energy Storage (LDES)":{"VCM":"D"},"Sustainable Aviation Fuel (SAF)":{"CORSIA":"D","VCM":"D"},"HVO (Hydrotreated Vegetable Oil)":{"CORSIA":"I","IMO Levy":"I","VCM":"D"},"E-kerosene (aviation e-fuel)":{"CORSIA":"D","VCM":"D"},"E-Ammonia (maritime fuel)":{"IMO Levy":"D","VCM":"D"},"E-Methanol (maritime fuel)":{"IMO Levy":"D","VCM":"D"},"E-diesel / E-methanol (road & ship)":{"IMO Levy":"I"},"Biogas (anaerobic digestion)":{"VCM":"D"},"Biomethane (upgraded to grid)":{"VCM":"D"},"Carbon Capture & Storage (CCUS)":{"VCM":"D"},"BECCS (Bioenergy + CCS)":{"VCM":"D"},"Direct Air Capture (DAC)":{"VCM":"D"},"Waste-to-Energy + CCS":{"VCM":"D"},"Reforestation / REDD+ / NBS":{"VCM":"D"},"Blue Carbon (mangroves, seagrass)":{"VCM":"D"},"Building Energy Efficiency / Retrofits":{"VCM":"D"},"Advanced / Chemical Recycling":{"VCM":"D"},"Green Data Centers":{"VCM":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"Canada":{"region":"North America","iso3":"CAN","techs":{"Solar PV":{"ETS":"D","VCM":"D"},"Onshore Wind":{"ETS":"D","VCM":"D"},"Offshore Wind (fixed foundation)":{"ETS":"D"},"Floating Offshore Wind":{"ETS":"D"},"Concentrated Solar Power (CSP)":{"ETS":"D","VCM":"D"},"Ocean / Tidal / Wave Energy":{"ETS":"D","VCM":"D"},"Small Modular Reactors (SMR)":{"ETS":"D","VCM":"I"},"Enhanced Geothermal Systems (EGS)":{"ETS":"D","VCM":"D"},"Green Hydrogen (electrolysis)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"Battery Storage (grid-scale)":{"ETS":"D","VCM":"D"},"Long-Duration Energy Storage (LDES)":{"ETS":"D","VCM":"D"},"Low-carbon Steel & Cement":{"ETS":"D","VCM":"D"},"Electric Arc Furnace (EAF)":{"ETS":"D","VCM":"D"},"Green Aluminium":{"ETS":"D","VCM":"D"},"Low-carbon Concrete":{"ETS":"D","VCM":"D"},"Green Fertilizer (low-carbon NH3)":{"ETS":"D","VCM":"D"},"Hydrogen-based Chemicals":{"ETS":"D","VCM":"D"},"Industrial Heat Pumps (high-temp)":{"ETS":"D","VCM":"D"},"Sustainable Aviation Fuel (SAF)":{"ETS":"D","CORSIA":"D","VCM":"D"},"HVO (Hydrotreated Vegetable Oil)":{"ETS":"D","CORSIA":"I","IMO Levy":"I","VCM":"D"},"E-kerosene (aviation e-fuel)":{"ETS":"D","CORSIA":"D","VCM":"D"},"E-Ammonia (maritime fuel)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"E-Methanol (maritime fuel)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"E-diesel / E-methanol (road & ship)":{"ETS":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"ETS":"D","VCM":"D"},"Biomethane (upgraded to grid)":{"ETS":"D","VCM":"D"},"Carbon Capture & Storage (CCUS)":{"ETS":"D","VCM":"D"},"BECCS (Bioenergy + CCS)":{"ETS":"D","VCM":"D"},"Direct Air Capture (DAC)":{"ETS":"D","VCM":"D"},"Waste-to-Energy + CCS":{"ETS":"D","VCM":"D"},"Reforestation / REDD+ / NBS":{"ETS":"D","VCM":"D"},"Blue Carbon (mangroves, seagrass)":{"VCM":"D"},"Building Energy Efficiency / Retrofits":{"ETS":"D","VCM":"D"},"Advanced / Chemical Recycling":{"ETS":"D","VCM":"D"},"Critical Minerals Processing (low-C)":{"ETS":"D"},"Green Data Centers":{"ETS":"D","VCM":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}},"South Korea":{"region":"East Asia","iso3":"KOR","techs":{"Solar PV":{"ETS":"D","VCM":"D"},"Onshore Wind":{"ETS":"D","VCM":"D"},"Offshore Wind (fixed foundation)":{"ETS":"D"},"Floating Offshore Wind":{"ETS":"D"},"Concentrated Solar Power (CSP)":{"ETS":"D","VCM":"D"},"Ocean / Tidal / Wave Energy":{"ETS":"D","VCM":"D"},"Small Modular Reactors (SMR)":{"ETS":"D","VCM":"I"},"Enhanced Geothermal Systems (EGS)":{"ETS":"D","VCM":"D"},"Green Hydrogen (electrolysis)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"Battery Storage (grid-scale)":{"ETS":"D","VCM":"D"},"Long-Duration Energy Storage (LDES)":{"ETS":"D","VCM":"D"},"Low-carbon Steel & Cement":{"ETS":"D","VCM":"D"},"Electric Arc Furnace (EAF)":{"ETS":"D","VCM":"D"},"Green Aluminium":{"ETS":"D","VCM":"D"},"Low-carbon Concrete":{"ETS":"D","VCM":"D"},"Green Fertilizer (low-carbon NH3)":{"ETS":"D","VCM":"D"},"Hydrogen-based Chemicals":{"ETS":"D","VCM":"D"},"Industrial Heat Pumps (high-temp)":{"ETS":"D","VCM":"D"},"Sustainable Aviation Fuel (SAF)":{"ETS":"D","CORSIA":"D","VCM":"D"},"HVO (Hydrotreated Vegetable Oil)":{"ETS":"D","CORSIA":"I","IMO Levy":"I","VCM":"D"},"E-kerosene (aviation e-fuel)":{"ETS":"D","CORSIA":"D","VCM":"D"},"E-Ammonia (maritime fuel)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"E-Methanol (maritime fuel)":{"ETS":"D","IMO Levy":"D","VCM":"D"},"E-diesel / E-methanol (road & ship)":{"ETS":"D","IMO Levy":"I"},"Biogas (anaerobic digestion)":{"ETS":"D","VCM":"D"},"Biomethane (upgraded to grid)":{"ETS":"D","VCM":"D"},"Carbon Capture & Storage (CCUS)":{"ETS":"D","VCM":"D"},"BECCS (Bioenergy + CCS)":{"ETS":"D","VCM":"D"},"Direct Air Capture (DAC)":{"ETS":"D","VCM":"D"},"Waste-to-Energy + CCS":{"ETS":"D","VCM":"D"},"Reforestation / REDD+ / NBS":{"ETS":"D","VCM":"D"},"Blue Carbon (mangroves, seagrass)":{"VCM":"D"},"Building Energy Efficiency / Retrofits":{"ETS":"D","VCM":"D"},"Advanced / Chemical Recycling":{"ETS":"D","VCM":"D"},"Critical Minerals Processing (low-C)":{"ETS":"D"},"Green Data Centers":{"ETS":"D","VCM":"D"},"Electric Aviation (eVTOL/short-haul)":{"CORSIA":"I"}}}}

# Country lat/lon for map
COUNTRY_COORDS = {
    "Afghanistan": (33.93, 67.71), "Albania": (41.15, 20.17), "Algeria": (28.03, 1.66),
    "Andorra": (42.55, 1.60), "Angola": (11.20, 17.87), "Antigua and Barbuda": (17.06, -61.80),
    "Argentina": (-38.42, -63.62), "Armenia": (40.07, 45.04), "Australia": (-25.27, 133.78),
    "Austria": (47.52, 14.55), "Azerbaijan": (40.14, 47.58), "Bahamas": (25.03, -77.40),
    "Bahrain": (26.00, 50.55), "Bangladesh": (23.68, 90.36), "Barbados": (13.19, -59.54),
    "Belarus": (53.71, 27.95), "Belgium": (50.50, 4.47), "Belize": (17.19, -88.50),
    "Benin": (9.31, 2.32), "Bhutan": (27.51, 90.43), "Bolivia": (-16.29, -63.59),
    "Bosnia and Herzegovina": (43.92, 17.68), "Botswana": (-22.33, 24.68),
    "Brazil": (-14.24, -51.93), "Brunei": (4.54, 114.73), "Bulgaria": (42.73, 25.49),
    "Burkina Faso": (12.36, -1.54), "Burundi": (-3.37, 29.92), "Cambodia": (12.57, 104.99),
    "Cameroon": (3.85, 11.50), "Canada": (56.13, -106.35), "Cape Verde": (16.54, -23.04),
    "Central African Republic": (6.61, 20.94), "Chad": (15.45, 18.73), "Chile": (-35.68, -71.54),
    "China": (35.86, 104.20), "Colombia": (4.57, -74.30), "Comoros": (-11.88, 43.87),
    "Congo": (-0.23, 15.83), "Costa Rica": (9.75, -83.75), "Croatia": (45.10, 15.20),
    "Cuba": (21.52, -77.78), "Cyprus": (35.13, 33.43), "Czech Republic": (49.82, 15.47),
    "DR Congo": (-4.04, 21.76), "Denmark": (56.26, 9.50), "Djibouti": (11.83, 42.59),
    "Dominica": (15.41, -61.37), "Dominican Republic": (18.74, -70.16), "Ecuador": (-1.83, -78.18),
    "Egypt": (26.82, 30.80), "El Salvador": (13.79, -88.90), "Equatorial Guinea": (1.65, 10.27),
    "Eritrea": (15.18, 39.78), "Estonia": (58.60, 25.01), "Eswatini": (-26.52, 31.47),
    "Ethiopia": (9.15, 40.49), "Fiji": (-17.71, 178.07), "Finland": (61.92, 25.75),
    "France": (46.23, 2.21), "Gabon": (-0.80, 11.61), "Gambia": (13.44, -15.31),
    "Georgia": (42.32, 43.36), "Germany": (51.17, 10.45), "Ghana": (7.95, -1.02),
    "Greece": (39.07, 21.82), "Grenada": (12.12, -61.68), "Guatemala": (15.78, -90.23),
    "Guinea": (9.95, -9.70), "Guinea-Bissau": (11.80, -15.18), "Guyana": (4.86, -58.93),
    "Haiti": (18.97, -72.29), "Honduras": (15.20, -86.24), "Hungary": (47.16, 19.50),
    "Iceland": (64.96, -19.02), "India": (20.59, 78.96), "Indonesia": (-0.79, 113.92),
    "Iran": (32.43, 53.69), "Iraq": (33.22, 43.68), "Ireland": (53.41, -8.24),
    "Israel": (31.05, 34.85), "Italy": (41.87, 12.57), "Jamaica": (18.11, -77.30),
    "Japan": (36.20, 138.25), "Jordan": (30.59, 36.24), "Kazakhstan": (48.02, 66.92),
    "Kenya": (-0.02, 37.91), "Kiribati": (1.87, -157.36), "Kuwait": (29.31, 47.48),
    "Kyrgyzstan": (41.20, 74.77), "Laos": (19.86, 102.50), "Latvia": (56.88, 24.60),
    "Lebanon": (33.85, 35.86), "Lesotho": (-29.61, 28.23), "Liberia": (6.43, -9.43),
    "Libya": (26.34, 17.23), "Liechtenstein": (47.14, 9.55), "Lithuania": (55.17, 23.88),
    "Luxembourg": (49.82, 6.13), "Madagascar": (-18.77, 46.87), "Malawi": (-13.25, 34.30),
    "Malaysia": (4.21, 101.98), "Maldives": (3.20, 73.22), "Mali": (17.57, -3.99),
    "Malta": (35.94, 14.37), "Marshall Islands": (7.13, 171.18), "Mauritania": (21.01, -10.94),
    "Mauritius": (-20.35, 57.55), "Mexico": (23.63, -102.55), "Micronesia": (7.43, 150.55),
    "Moldova": (47.41, 28.37), "Monaco": (43.73, 7.40), "Mongolia": (46.86, 103.85),
    "Montenegro": (42.71, 19.37), "Morocco": (31.79, -7.09), "Mozambique": (-18.67, 35.53),
    "Myanmar": (21.92, 95.96), "Namibia": (-22.96, 18.49), "Nauru": (-0.52, 166.93),
    "Nepal": (28.39, 84.12), "Netherlands": (52.13, 5.29), "New Zealand": (-40.90, 174.89),
    "Nicaragua": (12.87, -85.21), "Niger": (17.61, 8.08), "Nigeria": (9.08, 8.68),
    "North Korea": (40.34, 127.51), "North Macedonia": (41.61, 21.75), "Norway": (60.47, 8.47),
    "Oman": (21.51, 55.92), "Pakistan": (30.38, 69.35), "Palau": (7.51, 134.58),
    "Panama": (8.54, -80.78), "Papua New Guinea": (-6.31, 143.96), "Paraguay": (-23.44, -58.44),
    "Peru": (-9.19, -75.02), "Philippines": (12.88, 121.77), "Poland": (51.92, 19.15),
    "Portugal": (39.40, -8.22), "Qatar": (25.35, 51.18), "Romania": (45.94, 24.97),
    "Russia": (61.52, 105.32), "Rwanda": (-1.94, 29.87), "Saint Kitts and Nevis": (17.36, -62.78),
    "Saint Lucia": (13.91, -60.98), "Saint Vincent and the Grenadines": (13.25, -61.20),
    "Samoa": (-13.76, -172.10), "San Marino": (43.94, 12.46), "Sao Tome and Principe": (0.19, 6.61),
    "Saudi Arabia": (23.89, 45.08), "Senegal": (14.50, -14.45), "Serbia": (44.02, 21.01),
    "Seychelles": (-4.68, 55.49), "Sierra Leone": (8.46, -11.78), "Singapore": (1.35, 103.82),
    "Slovakia": (48.67, 19.70), "Slovenia": (46.15, 14.99), "Solomon Islands": (-9.65, 160.16),
    "Somalia": (5.15, 46.20), "South Africa": (-30.56, 22.94), "South Korea": (35.91, 127.77),
    "South Sudan": (6.88, 31.31), "Spain": (40.46, -3.75), "Sri Lanka": (7.87, 80.77),
    "Sudan": (12.86, 30.22), "Suriname": (3.92, -56.03), "Sweden": (60.13, 18.64),
    "Switzerland": (46.82, 8.23), "Syria": (34.80, 38.99), "Taiwan": (23.70, 120.96),
    "Tajikistan": (38.86, 71.28), "Tanzania": (-6.37, 34.89), "Thailand": (15.87, 100.99),
    "Timor-Leste": (-8.87, 125.73), "Togo": (8.62, 0.82), "Tonga": (-21.18, -175.20),
    "Trinidad and Tobago": (10.69, -61.22), "Tunisia": (33.89, 9.54), "Turkey": (38.96, 35.24),
    "Turkmenistan": (38.97, 59.56), "Tuvalu": (-7.11, 177.65), "Uganda": (1.37, 32.29),
    "Ukraine": (48.38, 31.17), "United Arab Emirates": (23.42, 53.85),
    "United Kingdom": (55.38, -3.44), "United States": (37.09, -95.71), "Uruguay": (-32.52, -55.77),
    "Uzbekistan": (41.38, 64.59), "Vanuatu": (-15.38, 166.96), "Venezuela": (6.42, -66.59),
    "Vietnam": (14.06, 108.28), "Yemen": (15.55, 48.52), "Zambia": (-13.13, 27.85),
    "Zimbabwe": (-19.02, 29.15),
}

# ─────────────────────────────────────────────────────────────────
# DEFAULT PARAMETERS per technology (44 techs)
# ─────────────────────────────────────────────────────────────────


def normalize_country_name(name):
    if not name:
        return ""
    s = str(name).strip()
    s = s.replace("’", "'").replace("`", "'")
    s = " ".join(s.split())
    return s

COUNTRY_NAME_ALIASES = {
    "United States of America": "United States",
    "USA": "United States",
    "US": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "UK": "United Kingdom",
    "Republic of Korea": "South Korea",
    "Korea, Republic of": "South Korea",
    "Korea (Republic of)": "South Korea",
    "Korea, South": "South Korea",
    "Democratic Republic of the Congo": "DR Congo",
    "Congo, Dem. Rep.": "DR Congo",
    "DRC": "DR Congo",
    "Congo (Kinshasa)": "DR Congo",
    "Republic of the Congo": "Congo",
    "Congo, Rep.": "Congo",
    "Congo (Brazzaville)": "Congo",
    "Czechia": "Czech Republic",
    "Türkiye": "Turkey",
    "Viet Nam": "Vietnam",
    "Lao PDR": "Laos",
    "Cabo Verde": "Cape Verde",
    "Eswatini (fmr. Swaziland)": "Eswatini",
    "Timor Leste": "Timor-Leste",
    "Micronesia (Federated States of)": "Micronesia",
    "Russian Federation": "Russia",
    "Syrian Arab Republic": "Syria",
    "Iran (Islamic Republic of)": "Iran",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Moldova, Republic of": "Moldova",
    "Tanzania, United Republic of": "Tanzania",
}

COUNTRY_COORDS_LOWER = {k.lower(): v for k, v in COUNTRY_COORDS.items()}
COUNTRY_ALIAS_LOWER = {k.lower(): v for k, v in COUNTRY_NAME_ALIASES.items()}

def get_country_coords(country_name):
    raw = normalize_country_name(country_name)
    candidate = COUNTRY_NAME_ALIASES.get(raw, raw)
    coords = COUNTRY_COORDS.get(candidate)
    if coords:
        return coords
    raw_low = raw.lower()
    if raw_low in COUNTRY_ALIAS_LOWER:
        mapped = COUNTRY_ALIAS_LOWER[raw_low]
        coords = COUNTRY_COORDS.get(mapped) or COUNTRY_COORDS_LOWER.get(mapped.lower())
        if coords:
            return coords
    if raw_low in COUNTRY_COORDS_LOWER:
        return COUNTRY_COORDS_LOWER[raw_low]
    return (None, None)

def make_defaults():
    d = {k: [0]*N for k in ["annual_output","installed_capacity","project_lifetime","capex_per_kw","feedstock_cost","other_opex","market_price"]}
    d.update({k: [0.0]*N for k in ["capacity_factor","opex_pct","wacc","co2_abated_factor","learning_rate","cum_cap_now","cum_cap_2035"]})
    vals = [
        (500000,200,0.28,25,1100,0.015,0,500000,0.07,65,0.45,0.20,2000,8000),
        (450000,200,0.28,25,1400,0.015,0,600000,0.07,65,0.45,0.15,900,4000),
        (420000,200,0.40,25,3200,0.020,0,1000000,0.08,80,0.45,0.12,60,500),
        (380000,150,0.40,25,4500,0.025,0,1200000,0.09,85,0.45,0.10,1,50),
        (200000,100,0.40,30,5000,0.020,0,800000,0.08,90,0.45,0.08,5,80),
        (50000,30,0.35,25,8000,0.030,0,500000,0.09,100,0.45,0.05,0.2,5),
        (800000,300,0.90,60,8000,0.025,0,2000000,0.09,80,0.50,0.04,0.001,10),
        (150000,50,0.90,30,6000,0.030,0,700000,0.08,90,0.45,0.06,0.01,5),
        (50000,100,0.45,20,2500,0.025,8000000,2000000,0.09,4500,0.90,0.18,0.5,10),
        (300000,150,0.25,15,1800,0.020,0,800000,0.08,90,0.30,0.22,1500,5000),
        (100000,50,0.30,20,3500,0.025,0,600000,0.09,100,0.30,0.10,0.1,20),
        (0,0,1.0,20,0,0.050,0,2000000,0.08,0,0.15,0.08,500,2000),
        (0,0,1.0,30,0,0.020,0,3000000,0.08,0,0.10,0.05,10,100),
        (0,0,1.0,15,0,0.060,0,1500000,0.08,0,0.15,0.12,50,500),
        (250000,50,0.90,25,5000,0.040,5000000,2000000,0.10,700,0.80,0.06,0.1,2),
        (300000,60,0.90,25,4000,0.035,4000000,1800000,0.10,650,0.75,0.08,0.05,1),
        (150000,40,0.90,25,5500,0.040,3000000,1500000,0.10,2500,0.80,0.07,0.02,0.5),
        (200000,50,0.90,25,4500,0.040,4000000,1800000,0.10,600,0.75,0.07,0.05,1),
        (100000,80,0.90,20,3500,0.030,4000000,1500000,0.09,950,0.85,0.10,0.02,0.5),
        (80000,60,0.90,20,4000,0.030,3500000,1200000,0.09,1200,0.80,0.09,0.01,0.3),
        (200000,80,0.85,20,2000,0.025,1000000,800000,0.08,100,0.40,0.08,0.1,3),
        (150000,80,0.85,20,3000,0.030,6000000,1500000,0.10,2800,0.70,0.12,0.05,0.5),
        (100000,60,0.85,20,2500,0.028,5000000,1200000,0.09,1800,0.65,0.10,0.02,0.3),
        (80000,60,0.85,20,4500,0.035,7000000,1500000,0.10,3500,0.75,0.08,0.005,0.1),
        (60000,80,0.90,20,3500,0.030,4000000,1000000,0.09,950,0.85,0.10,0.01,0.2),
        (50000,60,0.90,20,3200,0.030,3500000,900000,0.09,1300,0.75,0.10,0.01,0.2),
        (60000,60,0.90,20,3000,0.028,3000000,900000,0.09,1100,0.70,0.10,0.01,0.2),
        (80000,30,0.85,20,2000,0.028,2000000,700000,0.08,80,0.60,0.08,10,100),
        (100000,40,0.85,20,2500,0.028,2500000,800000,0.08,90,0.60,0.08,5,50),
        (0,0,1.0,10,0,0.050,0,500000,0.08,0,0.30,0.22,100,1000),
        (0,0,1.0,15,0,0.060,1000000,800000,0.09,0,0.50,0.15,0.1,5),
        (0,0,1.0,15,0,0.050,0,500000,0.09,0,0.40,0.18,0.001,1),
        (0,0,1.0,40,0,0.020,0,2000000,0.07,0,0.35,0.05,50,200),
        (100000,50,0.90,30,4000,0.035,2000000,1000000,0.10,80,0.85,0.08,0.03,0.5),
        (120000,60,0.85,25,5000,0.040,3000000,1500000,0.09,150,0.90,0.07,0.01,0.2),
        (50000,25,0.95,20,15000,0.050,3000000,2000000,0.10,500,1.00,0.15,0.001,1),
        (80000,40,0.85,25,4500,0.040,2000000,1200000,0.09,100,0.80,0.07,0.01,0.2),
        (80000,0,1.0,30,500,0.100,500000,300000,0.06,12,1.00,0.05,500,1000),
        (30000,0,1.0,30,300,0.120,200000,100000,0.06,30,1.00,0.04,10,50),
        (400000,0,1.0,20,800,0.050,0,1000000,0.07,100,0.40,0.08,5000,8000),
        (100000,30,0.85,20,2000,0.040,2000000,800000,0.09,200,0.50,0.10,0.5,10),
        (50000,20,0.85,20,3000,0.035,1000000,600000,0.09,500,0.40,0.08,0.1,2),
        (200000,50,0.90,10,1500,0.050,0,1500000,0.08,80,0.20,0.10,50,500),
    ]
    for i, v in enumerate(vals):
        d["annual_output"][i]=v[0]; d["installed_capacity"][i]=v[1]; d["capacity_factor"][i]=v[2]
        d["project_lifetime"][i]=v[3]; d["capex_per_kw"][i]=v[4]; d["opex_pct"][i]=v[5]
        d["feedstock_cost"][i]=v[6]; d["other_opex"][i]=v[7]; d["wacc"][i]=v[8]
        d["market_price"][i]=v[9]; d["co2_abated_factor"][i]=v[10]; d["learning_rate"][i]=v[11]
        d["cum_cap_now"][i]=v[12]; d["cum_cap_2035"][i]=v[13]
    return d

DEFAULTS = make_defaults()

# ─────────────────────────────────────────────────────────────────
# MBM PRICE DEFAULTS
# ─────────────────────────────────────────────────────────────────
DEFAULT_PRICES = {
    "ets": 70, "ctax": 50, "fuel": 240, "cfd_strike": 120, "cfd_ref": 80,
    "ccfd_strike": 100, "ccfd_ref": 60,
    "cbam": 55, "corsia": 22, "imo": 380, "vcm": 100, "amc": 100,
    "feebate": 50, "electricity": 60, "gas": 8, "biomass": 40,
}

MBM_LABELS = {
    "ets":   ("ETS / Carbon Market",  "USD/tCO₂e"),
    "ctax":  ("Carbon Tax",           "USD/tCO₂e"),
    "fuel":  ("Fuel Mandate",         "USD/MWh"),
    "cfd":   ("CfD",                  "USD/MWh"),
    "ccfd":  ("CCfD",                 "USD/tCO₂e"),
    "cbam":  ("CBAM Import",          "USD/tCO₂e"),
    "corsia":("CORSIA Credit",        "USD/tCO₂e"),
    "imo":   ("IMO Levy",             "USD/tCO₂e"),
    "vcm":   ("VCM / CDM Credit",     "USD/tCO₂e"),
    "amc":   ("AMC",                  "USD/unit"),
    "feebate":("Feebate",             "USD/tCO₂e"),
}

# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
GREENS = ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399","#6ee7b7","#a7f3d0","#d1fae5","#ecfdf5","#f0fdf4"]
PBG, FC, GC = "rgba(0,0,0,0)", "#374151", "rgba(5,150,105,0.07)"

def pl(h=380, ml=20, mr=20, mt=20, mb=30):
    return dict(
        paper_bgcolor=PBG, plot_bgcolor=PBG,
        font=dict(family="Inter", color=FC, size=10),
        height=h, margin=dict(l=ml, r=mr, t=mt, b=mb),
        legend=dict(orientation="h", y=-0.22, font=dict(size=9)),
        xaxis=dict(gridcolor=GC, linecolor="#e2e8f0", zeroline=False, tickfont=dict(size=9)),
        yaxis=dict(gridcolor=GC, linecolor="#e2e8f0", zeroline=False, tickfont=dict(size=9)),
    )

def calc_crf(w, l):
    return 1/l if w == 0 else (w*(1+w)**l)/((1+w)**l - 1)

def fm(v):
    if abs(v) >= 1e9: return f"${v/1e9:.2f}B"
    if abs(v) >= 1e6: return f"${v/1e6:.1f}M"
    if abs(v) >= 1e3: return f"${v/1e3:.0f}K"
    return f"${v:.0f}"

def kpi(val, label, sub=""):
    s = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return (f'<div class="kpi-card">'
            f'<div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{val}</div>{s}</div>')

def compute(prices, t, ti):
    o  = ti["annual_output"][t]
    ck = ti["installed_capacity"][t] * 1000
    lt = ti["project_lifetime"][t]
    w  = ti["wacc"][t]
    cap = ck * ti["capex_per_kw"][t]
    crf = calc_crf(w, lt)
    ac  = cap * crf
    fo  = cap * ti["opex_pct"][t]
    tc  = ac + fo + ti["feedstock_cost"][t] + ti["other_opex"][t]
    co2 = o * ti["co2_abated_factor"][t]
    dr  = o * ti["market_price"][t] if o > 0 else 0

    def active(mi): return MBM_MATRIX[t][mi] is not None

    e  = co2*prices["ets"]              if active(0) and co2>0 else 0
    cx = co2*prices["ctax"]             if active(1) and co2>0 else 0
    fu = o*prices["fuel"]*0.85          if active(2) and o>0   else 0
    cf = (o*max(0,prices["cfd_strike"]-prices["cfd_ref"])*0.5 if active(3) and o>0 else 0)
    ccf= (co2*max(0,prices["ccfd_strike"]-prices["ccfd_ref"])*0.5 if active(4) and co2>0 else 0)
    cb = co2*prices["cbam"]*0.85        if active(5) and co2>0 else 0
    co = co2*prices["corsia"]*1.05      if active(6) and co2>0 else 0
    im = co2*prices["imo"]*0.95         if active(7) and co2>0 else 0
    v  = co2*prices["vcm"]              if active(8) and co2>0 else 0
    am = (o/1000)*prices["amc"]*0.5     if active(9) and o>0   else 0
    fb = co2*prices["feebate"]*0.5      if active(10) and co2>0 else 0

    mb = e+cx+fu+cf+ccf+cb+co+im+v+am+fb
    tr = mb+dr
    return {
        "tc":tc,"ac":ac,"fo":fo,"co2":co2,"dr":dr,"mb":mb,"tr":tr,
        "nc":tr-tc,"lr":tr*lt,"rc":tr/tc if tc>0 else 0,
        "bd":{"ETS":e,"Carbon Tax":cx,"Fuel Mandate":fu,"CfD":cf,"CCfD":ccf,
              "CBAM":cb,"CORSIA":co,"IMO Levy":im,"VCM/CDM":v,"AMC":am,"Feebate":fb},
    }

def compute_country_excel(country_name, base_prices, t, ti):
    """Compute using Excel country data — only apply mechanisms present in the Excel data."""
    cp = dict(base_prices)
    cdata = COUNTRY_DATA_RAW.get(country_name, {})
    tech_name = TECHNOLOGIES[t]
    # Normalize tech name lookup (Excel uses slightly different names for some)
    tech_lookup = tech_name
    tech_mbms = cdata.get("techs", {}).get(tech_lookup, {})

    # Build a price dict where only active mechanisms (from Excel) retain their price
    allowed_mechs = set(tech_mbms.keys())
    # Map Excel MBM names to price keys
    mech_map = {
        "ETS": "ets", "Carbon Tax": "ctax", "Fuel Mandate": "fuel",
        "CfD": "cfd_strike", "CCfD": "ccfd_strike", "CBAM": "cbam",
        "CORSIA": "corsia", "IMO Levy": "imo", "VCM": "vcm",
        "CDM/PACM": "vcm", "AMC": "amc", "Feebate": "feebate",
    }
    # Zero out mechanisms not in this country-tech combo
    for excel_name, price_key in mech_map.items():
        if excel_name not in allowed_mechs:
            if price_key in ["ets", "ctax", "cbam", "corsia", "imo", "vcm", "amc", "feebate", "fuel"]:
                cp[price_key] = 0
    # Zero CfD/CCfD if not active
    if "CfD" not in allowed_mechs:
        cp["cfd_strike"] = cp.get("cfd_ref", 80)  # strike==ref → no payment
    if "CCfD" not in allowed_mechs:
        cp["ccfd_strike"] = cp.get("ccfd_ref", 60)
    return compute(cp, t, ti)

# ─────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────
if "ti"   not in st.session_state: st.session_state.ti = {k: list(v) for k,v in DEFAULTS.items()}
if "p"    not in st.session_state: st.session_state.p  = dict(DEFAULT_PRICES)
if "page" not in st.session_state: st.session_state.page = "Portfolio Overview"

# ─────────────────────────────────────────────────────────────────
# SIDEBAR — REVISED NAVIGATION
# ─────────────────────────────────────────────────────────────────
NAV = [
    ("Setup & Input", [
        ("Portfolio Overview",  "📊"),
        ("Technology Detail",   "🔬"),
        ("MBM Price Controls",  "⚙️"),
    ]),
    ("Result", [
        ("MBM Results",         "📈"),
        ("NPV Analysis",        "💰"),
        ("Tech Calculations",   "🧮"),
    ]),
    ("Spatial Viability", [
        ("Spatial Viability",   "🌍"),
    ]),
]

with st.sidebar:
    st.markdown("""
    <div style="padding:22px 18px 16px 18px;border-bottom:1px solid #f1f5f9;">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:38px;height:38px;border-radius:10px;flex-shrink:0;
                        background:linear-gradient(135deg,#059669,#34d399);
                        display:flex;align-items:center;justify-content:center;
                        font-size:18px;box-shadow:0 3px 10px rgba(5,150,105,0.28);">🌿</div>
            <div>
                <div style="font-size:0.88rem;font-weight:800;color:#064e3b;letter-spacing:-0.01em;line-height:1.1;">MBM Revenue</div>
                <div style="font-size:0.65rem;color:#9ca3af;margin-top:2px;">Model v2 · 44 Technologies</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for group_label, items in NAV:
        st.markdown(f'<div class="nav-group-label">{group_label}</div>', unsafe_allow_html=True)
        for label, icon in items:
            active = (st.session_state.page == label)
            if active:
                st.markdown(f"""
                <style>
                [data-testid="stSidebar"] div[data-testid="stButton"]:has(button[title="{label}"]) button {{
                    background: linear-gradient(90deg,#059669,#10b981) !important;
                    color: #ffffff !important; font-weight: 700 !important;
                }}
                </style>""", unsafe_allow_html=True)
            if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True, help=label):
                st.session_state.page = label
                st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown('<hr style="margin:0 0 10px 0;">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
        if st.button("↺  Reset Defaults", use_container_width=True, key="rst"):
            st.session_state.p  = dict(DEFAULT_PRICES)
            st.session_state.ti = {k: list(v) for k,v in DEFAULTS.items()}
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# PRE-COMPUTE
# ─────────────────────────────────────────────────────────────────
AR  = [compute(st.session_state.p, i, st.session_state.ti) for i in range(N)]
TR  = sum(r["tr"] for r in AR); TM = sum(r["mb"] for r in AR)
TD  = sum(r["dr"] for r in AR); TC = sum(r["tc"] for r in AR)
TN  = sum(r["nc"] for r in AR); TCO = sum(r["co2"] for r in AR)
page = st.session_state.page

# ═════════════════════════════════════════════════════════════════
# PAGE: PORTFOLIO OVERVIEW  (Setup & Input)
# ═════════════════════════════════════════════════════════════════
if page == "Portfolio Overview":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Setup & Input</div>
        <div class="page-header-title">📊 Portfolio Overview</div>
        <div class="page-header-sub">Annual revenue performance across 44 clean technology verticals — 11 MBM mechanisms</div>
    </div>''', unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(kpi(fm(TR), "Total Annual Revenue", "Portfolio-wide"), unsafe_allow_html=True)
    c2.markdown(kpi(fm(TM), "MBM Revenue", f"{TM/TR*100:.1f}% of total" if TR else "—"), unsafe_allow_html=True)
    c3.markdown(kpi(fm(TD), "Direct Revenue", f"{TD/TR*100:.1f}% of total" if TR else "—"), unsafe_allow_html=True)
    c4.markdown(kpi(fm(TN), "Net Cash Flow", f"R/C {TR/TC:.2f}×" if TC else "—"), unsafe_allow_html=True)
    c5.markdown(kpi(f"{TCO/1e6:.2f}M tCO₂e", "CO₂ Abated", "per year"), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Revenue by Category</div>', unsafe_allow_html=True)
    cats = {}
    for i, r in enumerate(AR):
        cat = TECH_CATEGORIES[i]
        if cat not in cats: cats[cat] = {"mb":0,"dr":0,"tc":0,"nc":0}
        cats[cat]["mb"] += r["mb"]; cats[cat]["dr"] += r["dr"]
        cats[cat]["tc"] += r["tc"]; cats[cat]["nc"] += r["nc"]

    cat_names = list(cats.keys())
    cat_colors = {"Clean Energy Generation":"#059669","Energy Storage & Grid":"#3b82f6",
                  "Industrial Decarbonisation":"#f59e0b","Transport & Fuels":"#8b5cf6",
                  "Carbon Removal & Nature":"#ef4444","Building & Efficiency":"#10b981",
                  "Circular Economy":"#a855f7","Digital Infrastructure":"#06b6d4"}

    fig_cat = go.Figure()
    fig_cat.add_trace(go.Bar(name="MBM Revenue", x=cat_names, y=[cats[c]["mb"]/1e6 for c in cat_names],
        marker_color=[cat_colors.get(c,"#059669") for c in cat_names]))
    fig_cat.add_trace(go.Bar(name="Direct Revenue", x=cat_names, y=[cats[c]["dr"]/1e6 for c in cat_names],
        marker_color=[cat_colors.get(c,"#34d399")+"88" for c in cat_names]))
    fig_cat.update_layout(**pl(330, mb=80))
    fig_cat.update_layout(barmode="stack", xaxis=dict(tickangle=-30), yaxis_title="USD Million")
    st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown('<div class="sec-head">Revenue by Technology</div>', unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2])
    with col_l:
        srt = sorted(range(N), key=lambda i: AR[i]["tr"], reverse=True)[:20]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="MBM Revenue", x=[TECH_SHORT[i] for i in srt], y=[AR[i]["mb"]/1e6 for i in srt], marker_color="#059669"))
        fig.add_trace(go.Bar(name="Direct Revenue", x=[TECH_SHORT[i] for i in srt], y=[AR[i]["dr"]/1e6 for i in srt], marker_color="#34d399"))
        fig.add_trace(go.Bar(name="Cost", x=[TECH_SHORT[i] for i in srt], y=[-AR[i]["tc"]/1e6 for i in srt], marker_color="#dcfce7"))
        fig.update_layout(**pl(420))
        fig.update_layout(barmode="relative", xaxis=dict(tickangle=-40), yaxis_title="USD Million",
            title=dict(text="Top 20 Technologies by Revenue", font=dict(size=11,color=FC), y=0.98))
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        agg = {}
        for r in AR:
            for k, v in r["bd"].items(): agg[k] = agg.get(k,0) + v
        mf = {k: v for k,v in agg.items() if v > 0}
        fig2 = go.Figure(go.Pie(labels=list(mf.keys()), values=list(mf.values()),
            hole=0.52, textinfo="label+percent", marker=dict(colors=GREENS[:len(mf)]),
            textfont=dict(size=8.5, color=FC)))
        fig2.update_layout(**pl(420, ml=10, mr=10, mt=30, mb=30))
        fig2.update_layout(showlegend=False,
            title=dict(text="MBM Revenue Mix (11 mechanisms)", font=dict(size=11,color=FC), y=0.98))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="sec-head">Net Annual Cash Flow — All Technologies</div>', unsafe_allow_html=True)
    nv = [AR[i]["nc"]/1e6 for i in range(N)]
    fig3 = go.Figure(go.Bar(x=TECH_SHORT, y=nv,
        marker_color=["#059669" if v >= 0 else "#fca5a5" for v in nv],
        text=[f"${v:.1f}M" for v in nv], textposition="outside", textfont=dict(size=8, color=FC)))
    fig3.update_layout(**pl(320, mb=80))
    fig3.update_layout(xaxis=dict(tickangle=-45), yaxis_title="USD Million")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="sec-head">Technology Ranking</div>', unsafe_allow_html=True)
    srt2 = sorted(range(N), key=lambda i: AR[i]["tr"], reverse=True)
    mx   = AR[srt2[0]]["tr"] if AR[srt2[0]]["tr"] > 0 else 1
    cols = st.columns(3)
    for rank, i in enumerate(srt2):
        col = cols[rank % 3]
        pct = AR[i]["tr"] / mx * 100
        col.markdown(f'''<div class="prog-wrap">
            <div class="prog-row"><span>{TECH_SHORT[i]}</span><b>{fm(AR[i]["tr"])}</b></div>
            <div class="prog-bg"><div class="prog-fill" style="width:{pct:.1f}%"></div></div>
        </div>''', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# PAGE: TECHNOLOGY DETAIL  (Setup & Input)
# ═════════════════════════════════════════════════════════════════
elif page == "Technology Detail":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Setup & Input — Technology Configuration</div>
        <div class="page-header-title">🔬 Technology Detail</div>
        <div class="page-header-sub">Configure individual technology parameters and view granular revenue breakdown</div>
    </div>''', unsafe_allow_html=True)

    ti = st.session_state.ti
    cat_sel = st.selectbox("Filter by Category", ["All"] + list(dict.fromkeys(TECH_CATEGORIES)), key="td_cat")
    avail = list(range(N)) if cat_sel == "All" else [i for i,c in enumerate(TECH_CATEGORIES) if c == cat_sel]
    sel  = st.selectbox("Select Technology", [TECHNOLOGIES[i] for i in avail], index=0)
    t    = TECHNOLOGIES.index(sel)
    cat  = TECH_CATEGORIES[t]
    cs, ci = CAT_STYLE.get(cat, ("cat-energy","⚡"))
    st.markdown(f'<span class="cat-badge {cs}">{ci} {cat}</span>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Technology Inputs</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Scale & Output**")
        ti["annual_output"][t]      = st.number_input("Annual Output (units/yr)", 0, 50_000_000, int(ti["annual_output"][t]), 10000, key=f"ao{t}")
        ti["installed_capacity"][t] = st.number_input("Installed Capacity (MW)", 0, 10000, int(ti["installed_capacity"][t]), 10, key=f"ic{t}")
        ti["capacity_factor"][t]    = st.slider("Capacity Factor", 0.0, 1.0, ti["capacity_factor"][t], 0.01, key=f"cf{t}")
        ti["project_lifetime"][t]   = st.slider("Project Lifetime (yr)", 5, 60, int(ti["project_lifetime"][t]), 1, key=f"pl{t}")
    with c2:
        st.markdown("**Cost Structure**")
        ti["capex_per_kw"][t]   = st.number_input("CAPEX/kW (USD/kW)", 0, 30000, int(ti["capex_per_kw"][t]), 100, key=f"ck{t}")
        ti["opex_pct"][t]       = st.slider("OPEX (% CAPEX p.a.)", 0.0, 0.20, ti["opex_pct"][t], 0.005, format="%.3f", key=f"op{t}")
        ti["feedstock_cost"][t] = st.number_input("Feedstock (USD/yr)", 0, 50_000_000, int(ti["feedstock_cost"][t]), 100000, key=f"fc{t}")
        ti["other_opex"][t]     = st.number_input("Other OPEX (USD/yr)", 0, 20_000_000, int(ti["other_opex"][t]), 100000, key=f"ov{t}")
        ti["wacc"][t]           = st.slider("WACC", 0.01, 0.25, ti["wacc"][t], 0.005, format="%.3f", key=f"wc{t}")
    with c3:
        st.markdown("**Revenue Drivers**")
        ti["market_price"][t]      = st.number_input("Market Price (USD/unit)", 0, 200000, int(ti["market_price"][t]), 10, key=f"mp{t}")
        ti["co2_abated_factor"][t] = st.slider("CO₂ Abated / Unit", 0.0, 2.0, ti["co2_abated_factor"][t], 0.01, key=f"ca{t}")

    r = compute(st.session_state.p, t, ti)
    st.markdown('<div class="sec-head">Results</div>', unsafe_allow_html=True)
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.markdown(kpi(fm(r["tr"]), "Total Revenue"), unsafe_allow_html=True)
    m2.markdown(kpi(fm(r["mb"]), "MBM Revenue"), unsafe_allow_html=True)
    m3.markdown(kpi(fm(r["dr"]), "Direct Revenue"), unsafe_allow_html=True)
    m4.markdown(kpi(fm(r["tc"]), "Total Cost"), unsafe_allow_html=True)
    m5.markdown(kpi(fm(r["nc"]), "Net Cash Flow", f"R/C {r['rc']:.2f}×"), unsafe_allow_html=True)

    ca, cb_ = st.columns(2)
    with ca:
        st.markdown('<div class="sec-head">MBM Breakdown (11 mechanisms)</div>', unsafe_allow_html=True)
        bd = {k: v for k,v in r["bd"].items() if v > 0}
        if bd:
            sb = sorted(bd.items(), key=lambda x: x[1], reverse=True)
            fb = go.Figure(go.Bar(x=[x[0] for x in sb], y=[x[1]/1e6 for x in sb],
                marker=dict(color=list(range(len(sb))), colorscale=[[0,"#a7f3d0"],[0.5,"#059669"],[1,"#064e3b"]]),
                text=[f"${x[1]/1e6:.2f}M" for x in sb], textposition="outside", textfont=dict(size=9,color=FC)))
            fb.update_layout(**pl(310)); fb.update_yaxes(title_text="USD Million")
            st.plotly_chart(fb, use_container_width=True)
        else:
            st.info("No active MBM mechanisms for this technology.")
    with cb_:
        st.markdown('<div class="sec-head">Cost vs Revenue</div>', unsafe_allow_html=True)
        cats_ = ["Direct Rev","MBM Rev","CAPEX ann.","Fixed OPEX","Feedstock","Other OPEX"]
        vals_ = [r["dr"]/1e6,r["mb"]/1e6,-r["ac"]/1e6,-r["fo"]/1e6,-ti["feedstock_cost"][t]/1e6,-ti["other_opex"][t]/1e6]
        fw = go.Figure(go.Bar(x=cats_, y=vals_, marker_color=["#059669" if v>=0 else "#fca5a5" for v in vals_],
            text=[f"${abs(v):.2f}M" for v in vals_], textposition="outside", textfont=dict(size=9,color=FC)))
        fw.add_hline(y=0, line_color="#e2e8f0", line_width=1.5)
        fw.update_layout(**pl(310)); fw.update_yaxes(title_text="USD Million")
        st.plotly_chart(fw, use_container_width=True)

    st.markdown('<div class="sec-head">Active MBM Mechanisms</div>', unsafe_allow_html=True)
    mech_keys = ["ets","ctax","fuel","cfd","ccfd","cbam","corsia","imo","vcm","amc","feebate"]
    html = ""
    for mi, mk in enumerate(mech_keys):
        lbl = MBM_LABELS[mk][0]
        val = MBM_MATRIX[t][mi]
        if val == 'D':   html += f'<span class="chip chip-d">✓ {lbl} (Direct)</span>'
        elif val == 'I': html += f'<span class="chip chip-i">~ {lbl} (Indirect)</span>'
        else:            html += f'<span class="chip chip-off">✕ {lbl}</span>'
    st.markdown(html, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# PAGE: MBM PRICE CONTROLS  (Setup & Input)
# ═════════════════════════════════════════════════════════════════
elif page == "MBM Price Controls":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Setup & Input — Global Parameters</div>
        <div class="page-header-title">⚙️ MBM Price Controls</div>
        <div class="page-header-sub">Adjust all 11 market-based mechanism parameters — changes propagate instantly to all pages</div>
    </div>''', unsafe_allow_html=True)

    p = st.session_state.p

    st.markdown('<div class="sec-head">Carbon Pricing Mechanisms</div>', unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        p["ets"]    = st.slider("ETS / Carbon Market (USD/tCO₂e)",  5,  300, p["ets"],     5,  key="mb_ets")
        p["ctax"]   = st.slider("Carbon Tax (USD/tCO₂e)",           0,  200, p["ctax"],    5,  key="mb_ctax")
        p["vcm"]    = st.slider("VCM / CDM Credit (USD/tCO₂e)",     5,  300, p["vcm"],     5,  key="mb_vcm")
        p["corsia"] = st.slider("CORSIA Credit (USD/tCO₂e)",        3,  100, int(p["corsia"]), 1, key="mb_corsia")
    with pc2:
        p["cbam"]   = st.slider("CBAM Import Cost (USD/tCO₂e)",    10,  150, p["cbam"],    5,  key="mb_cbam")
        p["imo"]    = st.slider("IMO Levy (USD/tCO₂e)",            50,  800, p["imo"],    10,  key="mb_imo")
        p["feebate"]= st.slider("Feebate Rate (USD/tCO₂e)",         0,  150, p["feebate"], 5,  key="mb_feebate")
        p["amc"]    = st.slider("AMC Price (USD/unit)",             50,  300, p["amc"],    10,  key="mb_amc")
    with pc3:
        p["cfd_strike"]  = st.slider("CfD Strike Price (USD/MWh)",      50, 300, p["cfd_strike"],   5, key="mb_cfd_s")
        p["cfd_ref"]     = st.slider("CfD Market Reference (USD/MWh)",  30, 200, p["cfd_ref"],      5, key="mb_cfd_r")
        p["ccfd_strike"] = st.slider("CCfD Strike Price (USD/tCO₂e)",   30, 250, p["ccfd_strike"],  5, key="mb_ccfd_s")
        p["ccfd_ref"]    = st.slider("CCfD Reference Price (USD/tCO₂e)",10, 150, p["ccfd_ref"],     5, key="mb_ccfd_r")

    st.markdown('<div class="sec-head">Energy & Commodity Prices</div>', unsafe_allow_html=True)
    pe1, pe2, pe3 = st.columns(3)
    with pe1:
        p["fuel"]       = st.slider("Fuel Mandate Offtake (USD/MWh)", 100, 600, p["fuel"],       10, key="mb_fuel")
    with pe2:
        p["electricity"]= st.slider("Grid Electricity (USD/MWh)",      20, 200, p["electricity"],  5, key="mb_elec")
        p["gas"]        = st.slider("Natural Gas (USD/MMBtu)",           2,  30, p["gas"],           1, key="mb_gas")
    with pe3:
        p["biomass"]    = st.slider("Biomass / Feedstock (USD/MWh)",   10, 120, p["biomass"],      5, key="mb_bio")
    st.session_state.p = p

    st.markdown('<div class="sec-head">Current Price Summary</div>', unsafe_allow_html=True)
    items = [
        ("ETS / Carbon Market", p["ets"], "USD/tCO₂e"), ("Carbon Tax", p["ctax"], "USD/tCO₂e"),
        ("VCM / CDM Credit", p["vcm"], "USD/tCO₂e"), ("CBAM Import", p["cbam"], "USD/tCO₂e"),
        ("CORSIA Credit", p["corsia"], "USD/tCO₂e"), ("IMO Levy", p["imo"], "USD/tCO₂e"),
        ("Feebate", p["feebate"], "USD/tCO₂e"), ("CfD Strike", p["cfd_strike"], "USD/MWh"),
        ("CfD Reference", p["cfd_ref"], "USD/MWh"), ("CCfD Strike", p["ccfd_strike"], "USD/tCO₂e"),
        ("CCfD Reference", p["ccfd_ref"], "USD/tCO₂e"), ("Fuel Mandate", p["fuel"], "USD/MWh"),
        ("AMC Price", p["amc"], "USD/unit"), ("Grid Electricity", p["electricity"], "USD/MWh"),
    ]
    cols_ = st.columns(4)
    for idx, (lbl, val, unit) in enumerate(items):
        cols_[idx%4].markdown(kpi(val, lbl, unit), unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    rb1, _, _ = st.columns([1,1,4])
    with rb1:
        if st.button("↺  Reset to Defaults", use_container_width=True, key="rst_mbm"):
            st.session_state.p  = dict(DEFAULT_PRICES)
            st.session_state.ti = {k: list(v) for k,v in DEFAULTS.items()}
            st.rerun()

# ═════════════════════════════════════════════════════════════════
# PAGE: MBM RESULTS  (Result)
# ═════════════════════════════════════════════════════════════════
elif page == "MBM Results":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Result</div>
        <div class="page-header-title">📈 MBM Results</div>
        <div class="page-header-sub">MBM breakdown, cost vs revenue, active mechanisms, and ETS carbon price sensitivity</div>
    </div>''', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["  MBM Breakdown  ", "  Cost & Revenue  ", "  Active Mechanisms  ", "  ETS Price Sensitivity  "])

    with tab1:
        st.markdown('<div class="sec-head">MBM Revenue Breakdown — All Mechanisms</div>', unsafe_allow_html=True)
        ch_l, ch_r = st.columns(2)
        mbm_keys   = ["ETS","Carbon Tax","Fuel Mandate","CfD","CCfD","CBAM","CORSIA","IMO Levy","VCM/CDM","AMC","Feebate"]
        mbm_colors = ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399","#6ee7b7","#a7f3d0","#d1fae5","#bbf7d0","#ecfdf5"]
        with ch_l:
            srt_stk = sorted(range(N), key=lambda i: AR[i]["mb"], reverse=True)[:20]
            fig_stk = go.Figure()
            for mkey, mcol in zip(mbm_keys, mbm_colors):
                vals = [AR[i]["bd"].get(mkey,0)/1e6 for i in srt_stk]
                fig_stk.add_trace(go.Bar(name=mkey, x=[TECH_SHORT[i] for i in srt_stk], y=vals,
                    marker_color=mcol,
                    text=[f"${v:.1f}M" if v > 2 else "" for v in vals],
                    textposition="inside", textfont=dict(size=7, color="#fff")))
            fig_stk.update_layout(**pl(440, mb=90))
            fig_stk.update_layout(barmode="stack", xaxis=dict(tickangle=-45), yaxis_title="USD Million",
                legend=dict(orientation="h", y=-0.35, font=dict(size=8)),
                title=dict(text="MBM Revenue — Top 20 (11 mechanisms)", font=dict(size=11,color=FC), y=0.98))
            st.plotly_chart(fig_stk, use_container_width=True)
        with ch_r:
            agg = {}
            for r in AR:
                for k, v in r["bd"].items(): agg[k] = agg.get(k,0) + v
            mf = {k: v for k,v in agg.items() if v > 0}
            fig_pie = go.Figure(go.Pie(labels=list(mf.keys()), values=list(mf.values()),
                hole=0.52, textinfo="label+percent", marker=dict(colors=GREENS[:len(mf)]),
                textfont=dict(size=8.5, color=FC)))
            fig_pie.update_layout(**pl(440, ml=10, mr=10, mt=30, mb=30))
            fig_pie.update_layout(showlegend=False,
                title=dict(text="Portfolio MBM Mix", font=dict(size=11,color=FC), y=0.98))
            st.plotly_chart(fig_pie, use_container_width=True)

        # Per-mechanism KPIs
        st.markdown('<div class="sec-head">Mechanism Revenue Summary</div>', unsafe_allow_html=True)
        cols_m = st.columns(4)
        for idx, mkey in enumerate(mbm_keys):
            total_m = sum(r["bd"].get(mkey, 0) for r in AR)
            cols_m[idx%4].markdown(kpi(fm(total_m), mkey, "Annual portfolio"), unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="sec-head">Cost vs Revenue — Portfolio</div>', unsafe_allow_html=True)
        srt_cmp = sorted(range(N), key=lambda i: AR[i]["tr"], reverse=True)[:15]
        fig_cmp = go.Figure()
        fig_cmp.add_trace(go.Bar(name="Direct Revenue", x=[AR[i]["dr"]/1e6 for i in srt_cmp],
            y=[TECH_SHORT[i] for i in srt_cmp], orientation="h", marker_color="#dc2626",
            text=[f"${AR[i]['dr']/1e6:.0f}M" if AR[i]["dr"]>1e6 else "" for i in srt_cmp],
            textposition="inside", textfont=dict(size=8, color="#fff")))
        fig_cmp.add_trace(go.Bar(name="MBM Revenue", x=[AR[i]["mb"]/1e6 for i in srt_cmp],
            y=[TECH_SHORT[i] for i in srt_cmp], orientation="h", marker_color="#059669",
            text=[f"${AR[i]['mb']/1e6:.0f}M" if AR[i]["mb"]>1e6 else "" for i in srt_cmp],
            textposition="inside", textfont=dict(size=8, color="#fff")))
        fig_cmp.update_layout(**pl(440, ml=100, mb=40))
        fig_cmp.update_layout(barmode="group", xaxis_title="USD Million",
            legend=dict(orientation="h", y=-0.12, font=dict(size=8)),
            title=dict(text="Direct vs MBM — Top 15", font=dict(size=11,color=FC), y=0.98))
        st.plotly_chart(fig_cmp, use_container_width=True)

        st.markdown('<div class="sec-head">Net Annual Cash Flow — All Technologies</div>', unsafe_allow_html=True)
        nv = [AR[i]["nc"]/1e6 for i in range(N)]
        fig_nc = go.Figure(go.Bar(x=TECH_SHORT, y=nv,
            marker_color=["#059669" if v >= 0 else "#fca5a5" for v in nv],
            text=[f"${v:.1f}M" for v in nv], textposition="outside", textfont=dict(size=8, color=FC)))
        fig_nc.update_layout(**pl(320, mb=80))
        fig_nc.update_layout(xaxis=dict(tickangle=-45), yaxis_title="USD Million")
        st.plotly_chart(fig_nc, use_container_width=True)

    with tab3:
        st.markdown('<div class="sec-head">MBM Mechanism Applicability Heatmap</div>', unsafe_allow_html=True)
        mech_cols = ["ETS","Carbon Tax","Fuel Mandate","CfD","CCfD","CBAM","CORSIA","IMO Levy","VCM/CDM","AMC","Feebate"]
        z, texts_z = [], []
        for i in range(N):
            row_z, row_t = [], []
            for mi in range(11):
                val = MBM_MATRIX[i][mi]
                if val == 'D':   row_z.append(2); row_t.append("D")
                elif val == 'I': row_z.append(1); row_t.append("I")
                else:            row_z.append(0); row_t.append("")
            z.append(row_z); texts_z.append(row_t)

        fhm = go.Figure(go.Heatmap(z=z, x=mech_cols, y=TECH_SHORT,
            colorscale=[[0,"#f9fafb"],[0.01,"#dbeafe"],[0.5,"#93c5fd"],[0.5001,"#d1fae5"],[1,"#059669"]],
            showscale=False,
            hovertemplate="<b>%{y}</b> × <b>%{x}</b><br>%{text}<extra></extra>",
            text=texts_z))
        for i in range(N):
            for j in range(11):
                if MBM_MATRIX[i][j]:
                    color = "#065f46" if MBM_MATRIX[i][j]=='D' else "#1e3a8a"
                    fhm.add_annotation(x=mech_cols[j], y=TECH_SHORT[i],
                        text=MBM_MATRIX[i][j], showarrow=False,
                        font=dict(size=9, color=color, family="Inter"))
        fhm.update_layout(**pl(900, ml=130, mr=40, mt=20, mb=120))
        fhm.update_layout(xaxis=dict(tickangle=-42, side="bottom"))
        st.plotly_chart(fhm, use_container_width=True)
        st.markdown("""
        <div style="font-size:0.75rem;color:#6b7280;margin-top:-8px;">
        🟢 <b>D</b> = Direct mechanism linkage &nbsp;|&nbsp; 🔵 <b>I</b> = Indirect mechanism linkage &nbsp;|&nbsp; ⬜ = Not applicable
        </div>""", unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="sec-head">ETS Carbon Price Sensitivity</div>', unsafe_allow_html=True)
        bp = dict(st.session_state.p)
        er = list(range(10, 310, 10))
        tvs, mvs, nvs = [], [], []
        for ep in er:
            tp = {**bp, "ets": ep}
            res = [compute(tp, i, st.session_state.ti) for i in range(N)]
            tvs.append(sum(r["tr"] for r in res)/1e6)
            mvs.append(sum(r["mb"] for r in res)/1e6)
            nvs.append(sum(r["nc"] for r in res)/1e6)

        fs = make_subplots(rows=1, cols=2, subplot_titles=("Total Revenue & Net CF","MBM Revenue"))
        fs.add_trace(go.Scatter(x=er, y=tvs, name="Total Revenue", line=dict(color="#059669",width=2.5)), row=1, col=1)
        fs.add_trace(go.Scatter(x=er, y=nvs, name="Net Cash Flow", line=dict(color="#34d399",width=2,dash="dot")), row=1, col=1)
        fs.add_trace(go.Scatter(x=er, y=mvs, name="MBM Revenue",
            fill="tozeroy", fillcolor="rgba(5,150,105,0.08)",
            line=dict(color="#059669",width=2)), row=1, col=2)
        for ci in [1,2]:
            fs.add_vline(x=bp["ets"], line_color="#d1fae5", line_dash="dash", row=1, col=ci)
        fs.update_layout(paper_bgcolor=PBG, plot_bgcolor=PBG, font=dict(family="Inter",color=FC,size=10),
            height=380, margin=dict(l=20,r=20,t=38,b=20),
            legend=dict(orientation="h",y=-0.15,font=dict(size=9)))
        for ax in ["xaxis","xaxis2"]:
            fs.update_layout(**{ax: dict(gridcolor=GC, title_text="ETS Price (USD/tCO₂e)", title_font=dict(size=9), tickfont=dict(size=9))})
        for ax in ["yaxis","yaxis2"]:
            fs.update_layout(**{ax: dict(gridcolor=GC, title_text="USD Million", title_font=dict(size=9), tickfont=dict(size=9))})
        st.plotly_chart(fs, use_container_width=True)

        # Current ETS price annotation
        curr_ets = bp["ets"]
        curr_tr = sum(r["tr"] for r in AR)/1e6
        curr_mb = sum(r["mb"] for r in AR)/1e6
        col_a, col_b, col_c = st.columns(3)
        col_a.markdown(kpi(f"${curr_ets}", "Current ETS Price", "USD/tCO₂e"), unsafe_allow_html=True)
        col_b.markdown(kpi(fm(curr_tr*1e6), "Total Revenue @ Current ETS", "Portfolio-wide"), unsafe_allow_html=True)
        col_c.markdown(kpi(fm(curr_mb*1e6), "MBM Revenue @ Current ETS", "Portfolio-wide"), unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# PAGE: NPV ANALYSIS  (Result)
# ═════════════════════════════════════════════════════════════════
elif page == "NPV Analysis":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Result — Investment Valuation</div>
        <div class="page-header-title">💰 NPV Analysis</div>
        <div class="page-header-sub">Net Present Value incorporating MBM revenue streams and forecast assumptions</div>
    </div>''', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#f0fdf4;border:1px solid #6ee7b7;border-radius:10px;padding:14px 18px;margin-bottom:18px;">
    <div style="font-size:0.75rem;font-weight:700;color:#065f46;margin-bottom:6px;">NPV EQUATION WITH MBM (11 mechanisms)</div>
    <div style="font-size:0.82rem;color:#1f2937;font-family:monospace;">
    NPV = −CAPEX  +  Σ<sub>t=1..T</sub>  [ (Direct_Rev<sub>t</sub> + MBM_Rev<sub>t</sub> − OPEX<sub>t</sub>) / (1 + WACC)<sup>t</sup> ]
    </div>
    <div style="font-size:0.72rem;color:#6b7280;margin-top:6px;">
    MBM includes: ETS + Carbon Tax + VCM/CDM + CfD + <b>CCfD</b> + CBAM + CORSIA + IMO + AMC + Feebate + Fuel Mandate
    </div>
    </div>""", unsafe_allow_html=True)

    nc1, nc2, nc3 = st.columns(3)
    with nc1:
        cat_f = st.selectbox("Filter Category", ["All"] + list(dict.fromkeys(TECH_CATEGORIES)), key="npv_cat")
        avail_npv = list(range(N)) if cat_f=="All" else [i for i,c in enumerate(TECH_CATEGORIES) if c==cat_f]
        sel_npv  = st.selectbox("Technology", [TECHNOLOGIES[i] for i in avail_npv], key="npv_sel")
        t_npv    = TECHNOLOGIES.index(sel_npv)
        discount_rate = st.slider("Discount Rate (WACC override %)", 2.0, 25.0,
                                   st.session_state.ti["wacc"][t_npv]*100, 0.5, key="npv_dr") / 100
    with nc2:
        mbm_growth    = st.slider("Annual MBM Price Growth (%/yr)", -5.0, 20.0, 5.0, 0.5, key="npv_mg") / 100
        direct_growth = st.slider("Annual Direct Rev Growth (%/yr)", -5.0, 15.0, 2.0, 0.5, key="npv_dg") / 100
    with nc3:
        opex_inflation = st.slider("OPEX Inflation (%/yr)", 0.0, 10.0, 2.5, 0.5, key="npv_oi") / 100
        show_mbm_toggle = st.radio("Include MBM in NPV?", ["Yes — with MBM","No — without MBM"], key="npv_mbm")

    include_mbm = (show_mbm_toggle == "Yes — with MBM")
    ti = st.session_state.ti; p = st.session_state.p
    lt = ti["project_lifetime"][t_npv]; ck = ti["installed_capacity"][t_npv]*1000
    capex_total = ck * ti["capex_per_kw"][t_npv]

    base_result = compute(p, t_npv, ti)
    base_dr = base_result["dr"]; base_mb = base_result["mb"]
    base_opex = base_result["tc"] - base_result["ac"]

    years, cfs_mbm, cfs_no_mbm, disc_cfs_mbm, disc_cfs_no_mbm = [], [], [], [], []
    cumulative_mbm, cumulative_no = [], []
    cum_m = -capex_total; cum_n = -capex_total

    for yr in range(1, lt+1):
        dr_t   = base_dr   * (1+direct_growth)**(yr-1)
        mb_t   = base_mb   * (1+mbm_growth)**(yr-1)
        opex_t = base_opex * (1+opex_inflation)**(yr-1)
        cf_mbm = dr_t+mb_t-opex_t; cf_no = dr_t-opex_t
        dcf_mbm= cf_mbm/(1+discount_rate)**yr; dcf_no = cf_no/(1+discount_rate)**yr
        years.append(yr)
        cfs_mbm.append(cf_mbm/1e6); cfs_no_mbm.append(cf_no/1e6)
        disc_cfs_mbm.append(dcf_mbm/1e6); disc_cfs_no_mbm.append(dcf_no/1e6)
        cum_m += dcf_mbm; cum_n += dcf_no
        cumulative_mbm.append(cum_m/1e6); cumulative_no.append(cum_n/1e6)

    npv_with_mbm  = sum(disc_cfs_mbm) - capex_total/1e6
    npv_no_mbm    = sum(disc_cfs_no_mbm) - capex_total/1e6
    mbm_npv_delta = npv_with_mbm - npv_no_mbm

    n1,n2,n3,n4 = st.columns(4)
    npv_disp = npv_with_mbm if include_mbm else npv_no_mbm
    n1.markdown(kpi(f"${npv_disp:.1f}M", "NPV"+(" (with MBM)" if include_mbm else " (no MBM)"),
                    "✅ Positive" if npv_disp>=0 else "❌ Negative"), unsafe_allow_html=True)
    n2.markdown(kpi(f"${npv_with_mbm:.1f}M", "NPV with MBM", f"CAPEX {capex_total/1e6:.1f}M"), unsafe_allow_html=True)
    n3.markdown(kpi(f"${npv_no_mbm:.1f}M",   "NPV without MBM", f"Δ ${mbm_npv_delta:.1f}M"), unsafe_allow_html=True)
    n4.markdown(kpi(f"${mbm_npv_delta:.1f}M","MBM NPV Uplift", "Value added by MBM"), unsafe_allow_html=True)

    fn1, fn2 = st.columns(2)
    with fn1:
        st.markdown('<div class="sec-head">Annual Cash Flows</div>', unsafe_allow_html=True)
        fig_cf = go.Figure()
        fig_cf.add_trace(go.Bar(name="CF (with MBM)", x=years, y=cfs_mbm, marker_color="#059669", opacity=0.85))
        fig_cf.add_trace(go.Bar(name="CF (no MBM)",   x=years, y=cfs_no_mbm, marker_color="#a7f3d0"))
        fig_cf.add_hline(y=0, line_color="#e2e8f0", line_width=1.5)
        fig_cf.update_layout(**pl(340))
        fig_cf.update_layout(barmode="overlay", xaxis_title="Year", yaxis_title="USD Million")
        st.plotly_chart(fig_cf, use_container_width=True)
    with fn2:
        st.markdown('<div class="sec-head">Cumulative NPV (incl. CAPEX)</div>', unsafe_allow_html=True)
        fig_cum = go.Figure()
        fig_cum.add_trace(go.Scatter(name="Cumul. NPV (with MBM)", x=years, y=cumulative_mbm,
            line=dict(color="#059669",width=2.5), fill="tozeroy", fillcolor="rgba(5,150,105,0.08)"))
        fig_cum.add_trace(go.Scatter(name="Cumul. NPV (no MBM)", x=years, y=cumulative_no,
            line=dict(color="#6ee7b7",width=2,dash="dot")))
        fig_cum.add_hline(y=0, line_color="#dc2626", line_width=1.5, line_dash="dash",
            annotation_text="Break-even", annotation_font_color="#dc2626", annotation_font_size=9)
        fig_cum.update_layout(**pl(340))
        fig_cum.update_layout(xaxis_title="Year", yaxis_title="USD Million (NPV)")
        st.plotly_chart(fig_cum, use_container_width=True)

    st.markdown('<div class="sec-head">Portfolio NPV Summary — All 44 Technologies</div>', unsafe_allow_html=True)
    npv_rows = []
    for i in range(N):
        lt_i = ti["project_lifetime"][i]; ck_i = ti["installed_capacity"][i]*1000
        cap_i = ck_i*ti["capex_per_kw"][i]; dr_i = AR[i]["dr"]; mb_i = AR[i]["mb"]
        op_i  = AR[i]["tc"]-AR[i]["ac"]; w_i = ti["wacc"][i]
        npv_m = -cap_i+sum((dr_i*(1+direct_growth)**(y-1)+mb_i*(1+mbm_growth)**(y-1)
                            -op_i*(1+opex_inflation)**(y-1))/(1+w_i)**y for y in range(1,lt_i+1))
        npv_n = -cap_i+sum((dr_i*(1+direct_growth)**(y-1)
                            -op_i*(1+opex_inflation)**(y-1))/(1+w_i)**y for y in range(1,lt_i+1))
        npv_rows.append({
            "Technology": TECHNOLOGIES[i], "Category": TECH_CATEGORIES[i],
            "CAPEX ($M)": round(cap_i/1e6,1), "Lifetime (yr)": lt_i, "WACC (%)": round(w_i*100,1),
            "NPV with MBM ($M)": round(npv_m/1e6,1), "NPV no MBM ($M)": round(npv_n/1e6,1),
            "MBM Uplift ($M)": round((npv_m-npv_n)/1e6,1),
            "Viable (MBM)?": "✅ Yes" if npv_m>=0 else "❌ No",
            "Viable (no MBM)?": "✅ Yes" if npv_n>=0 else "❌ No",
        })
    df_npv = pd.DataFrame(npv_rows)
    st.dataframe(df_npv.style.bar(subset=["NPV with MBM ($M)","NPV no MBM ($M)","MBM Uplift ($M)"],
                 color="#bbf7d0", align="mid"), use_container_width=True, height=600)
    st.download_button("⬇ Download NPV CSV", df_npv.to_csv(index=False).encode(), "npv_analysis.csv", "text/csv")

# ═════════════════════════════════════════════════════════════════
# PAGE: TECH CALCULATIONS  (Result)
# ═════════════════════════════════════════════════════════════════
elif page == "Tech Calculations":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Result — Engineering Economics</div>
        <div class="page-header-title">🧮 Technology Calculations</div>
        <div class="page-header-sub">Core engineering and financial equations per technology</div>
    </div>''', unsafe_allow_html=True)

    cat_f2 = st.selectbox("Filter Category", ["All"]+list(dict.fromkeys(TECH_CATEGORIES)), key="tc_cat")
    avail_tc = list(range(N)) if cat_f2=="All" else [i for i,c in enumerate(TECH_CATEGORIES) if c==cat_f2]
    sel_tc = st.selectbox("Select Technology", [TECHNOLOGIES[i] for i in avail_tc], key="tc_sel")
    t_tc   = TECHNOLOGIES.index(sel_tc)
    ti = st.session_state.ti; p = st.session_state.p

    o   = ti["annual_output"][t_tc]; ck = ti["installed_capacity"][t_tc]*1000
    lt  = ti["project_lifetime"][t_tc]; w  = ti["wacc"][t_tc]
    cap = ck*ti["capex_per_kw"][t_tc]; cf = ti["capacity_factor"][t_tc]
    crf = calc_crf(w, lt); ann_cap = cap*crf; fo = cap*ti["opex_pct"][t_tc]
    feedstock = ti["feedstock_cost"][t_tc]; other_op = ti["other_opex"][t_tc]
    co2 = o*ti["co2_abated_factor"][t_tc]; lr = ti["learning_rate"][t_tc]
    cum_now = ti["cum_cap_now"][t_tc]; cum_2035 = ti["cum_cap_2035"][t_tc]
    r_tc = compute(p, t_tc, ti)

    st.markdown('<div class="sec-head">📐 Capacity & Output</div>', unsafe_allow_html=True)
    tc1,tc2,tc3,tc4 = st.columns(4)
    theoretical = ck*cf*8760/1000
    tc1.markdown(kpi(f"{ck/1000:.1f} MW", "Installed Capacity", "Nameplate"), unsafe_allow_html=True)
    tc2.markdown(kpi(f"{cf*100:.1f}%", "Capacity Factor", "Utilisation"), unsafe_allow_html=True)
    tc3.markdown(kpi(f"{theoretical:,.0f} MWh", "Theoretical Output/yr", f"CF × {ck/1000:.0f} MW × 8760h"), unsafe_allow_html=True)
    tc4.markdown(kpi(f"{o:,.0f}", "Configured Output/yr", "MWh or units"), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🏗️ CAPEX & Annualisation</div>', unsafe_allow_html=True)
    cc1,cc2,cc3,cc4 = st.columns(4)
    cc1.markdown(kpi(f"${cap/1e6:.1f}M", "Total CAPEX", f"${ti['capex_per_kw'][t_tc]:,}/kW"), unsafe_allow_html=True)
    cc2.markdown(kpi(f"{w*100:.1f}%", "WACC", "Discount rate"), unsafe_allow_html=True)
    cc3.markdown(kpi(f"{crf:.4f}", "Capital Recovery Factor", "CRF"), unsafe_allow_html=True)
    cc4.markdown(kpi(f"${ann_cap/1e6:.2f}M", "Annualised CAPEX", "CAPEX × CRF"), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🌿 CO₂ Abatement & Carbon Value</div>', unsafe_allow_html=True)
    cv1,cv2,cv3,cv4 = st.columns(4)
    mac = (r_tc["tc"]-r_tc["dr"])/co2 if co2>0 else 0
    cv1.markdown(kpi(f"{co2/1e6:.3f} MtCO₂", "Annual Abatement", f"{ti['co2_abated_factor'][t_tc]} tCO₂/unit"), unsafe_allow_html=True)
    cv2.markdown(kpi(f"${r_tc['bd'].get('ETS',0)/1e6:.2f}M", "ETS Value", f"@${p['ets']}/tCO₂e"), unsafe_allow_html=True)
    cv3.markdown(kpi(f"${r_tc['bd'].get('VCM/CDM',0)/1e6:.2f}M", "VCM Value", f"@${p['vcm']}/tCO₂e"), unsafe_allow_html=True)
    cv4.markdown(kpi(f"${mac:.1f}/tCO₂", "Marginal Abatement Cost", "Net cost/CO₂ abated"), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">📉 Learning Curve (Wright\'s Law)</div>', unsafe_allow_html=True)
    lcol1, lcol2 = st.columns([2,1])
    with lcol1:
        if cum_now > 0 and cum_2035 > cum_now and lr > 0:
            cum_vals = np.logspace(np.log10(cum_now), np.log10(cum_2035), 50)
            lcost = [ti["capex_per_kw"][t_tc]*(c/cum_now)**(-lr/np.log2(2)) for c in cum_vals]
            fig_lc = go.Figure()
            fig_lc.add_trace(go.Scatter(x=cum_vals, y=lcost, mode="lines",
                line=dict(color="#059669",width=2.5), name="CAPEX/kW"))
            fig_lc.add_vline(x=cum_now, line_dash="dot", line_color="#6ee7b7", annotation_text="Today", annotation_font_size=9)
            fig_lc.add_vline(x=cum_2035, line_dash="dot", line_color="#059669", annotation_text="2035", annotation_font_size=9)
            fig_lc.update_layout(**pl(280))
            fig_lc.update_layout(xaxis_title="Cumulative Capacity (GW)", xaxis_type="log",
                yaxis_title="CAPEX (USD/kW)",
                title=dict(text=f"Wright's Law: Learning Rate {lr*100:.0f}%", font=dict(size=11,color=FC), y=0.98))
            st.plotly_chart(fig_lc, use_container_width=True)
        else:
            st.info("Learning curve unavailable for service-type technologies with zero capacity.")
    with lcol2:
        if cum_now > 0 and cum_2035 > cum_now and lr > 0:
            cost_2035 = ti["capex_per_kw"][t_tc]*(cum_2035/cum_now)**(-lr/np.log2(2))
            reduction = (1-cost_2035/ti["capex_per_kw"][t_tc])*100
            st.markdown(kpi(f"${ti['capex_per_kw'][t_tc]:,}/kW", "CAPEX Today"), unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown(kpi(f"${cost_2035:,.0f}/kW", "CAPEX 2035 Est.", f"−{reduction:.0f}%"), unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown(kpi(f"{lr*100:.0f}%", "Learning Rate", "Per doubling"), unsafe_allow_html=True)

    st.markdown('<div class="sec-head">📊 Levelised Cost (LCOE / LCOX)</div>', unsafe_allow_html=True)
    lco1, lco2, lco3 = st.columns(3)
    total_annual_cost = ann_cap+fo+feedstock+other_op
    lcoe = total_annual_cost/o if o > 0 else 0
    lco_per_tco2 = total_annual_cost/co2 if co2 > 0 else 0
    lco1.markdown(kpi(f"${lcoe:.3f}/unit", "LCOE / Unit Cost", "Total cost / annual output"), unsafe_allow_html=True)
    lco2.markdown(kpi(f"${lco_per_tco2:.1f}/tCO₂", "LCOX (Cost/tCO₂)", "Total cost / CO₂ abated"), unsafe_allow_html=True)
    lco3.markdown(kpi(f"{r_tc['rc']:.2f}×", "Revenue / Cost Ratio", "R/C > 1 = viable"), unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# PAGE: SPATIAL VIABILITY  (Spatial Viability)
# ═════════════════════════════════════════════════════════════════
elif page == "Spatial Viability":
    st.markdown('''
    <div class="page-header">
        <div class="page-header-badge">Spatial Viability · 194 Countries · Excel Data</div>
        <div class="page-header-title">🌍 Spatial Viability</div>
        <div class="page-header-sub">Technology viability across 194 countries — MBM applicability from Country Level sheet (Task___Country_and_Sector.xlsx)</div>
    </div>''', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#dbeafe;border:1px solid #93c5fd;border-radius:8px;padding:10px 16px;margin-bottom:14px;font-size:0.78rem;color:#1e3a8a;">
    📌 <b>Data source:</b> MBM applicability per country and technology is drawn from the <b>Country Level</b> sheet
    of <b>Task___Country_and_Sector.xlsx</b>. Each country has its own set of applicable MBM mechanisms per technology (D=Direct, I=Indirect).
    </div>""", unsafe_allow_html=True)

    ti = st.session_state.ti
    ALL_REGIONS_EXCEL = sorted(set(v["region"] for v in COUNTRY_DATA_RAW.values()))

    sv1, sv2 = st.columns([2, 2])
    with sv1:
        cat_sv = st.selectbox("Filter Category", ["All"]+list(dict.fromkeys(TECH_CATEGORIES)), key="sv_cat")
        avail_sv = list(range(N)) if cat_sv=="All" else [i for i,c in enumerate(TECH_CATEGORIES) if c==cat_sv]
        sel_sv = st.selectbox("Technology to Deploy", [TECHNOLOGIES[i] for i in avail_sv], key="sv_sel")
        t_sv   = TECHNOLOGIES.index(sel_sv)
    with sv2:
        show_regions = st.multiselect("Filter Regions", ALL_REGIONS_EXCEL, default=ALL_REGIONS_EXCEL, key="sv_region")
        mbm_growth_sv = st.slider("MBM Growth Rate (%/yr)", 0.0, 15.0, 5.0, 0.5, key="sv_mg") / 100

    # Build country viability table from Excel data
    sv_rows = []
    for country, cdata in COUNTRY_DATA_RAW.items():
        if cdata["region"] not in show_regions:
            continue
        r_sv = compute_country_excel(country, st.session_state.p, t_sv, ti)
        lt_sv = ti["project_lifetime"][t_sv]
        ck_sv = ti["installed_capacity"][t_sv]*1000
        cap_sv = ck_sv*ti["capex_per_kw"][t_sv]
        w_sv  = ti["wacc"][t_sv]
        dr_sv = r_sv["dr"]; mb_sv = r_sv["mb"]; op_sv = r_sv["tc"]-r_sv["ac"]
        npv_sv = -cap_sv+sum((dr_sv+mb_sv*(1+mbm_growth_sv)**(y-1)-op_sv)/(1+w_sv)**y
                              for y in range(1, lt_sv+1))

        # Get active MBMs for this country-tech
        tech_mbms = cdata["techs"].get(sel_sv, {})
        active_mbms_str = ", ".join([f"{k}({v})" for k,v in tech_mbms.items()]) if tech_mbms else "None"

        sv_rows.append({
            "Country": country, "ISO3": cdata["iso3"], "Region": cdata["region"],
            "Active MBMs": active_mbms_str,
            "MBM Rev ($M)": round(r_sv["mb"]/1e6, 2),
            "Direct Rev ($M)": round(r_sv["dr"]/1e6, 2),
            "Total Rev ($M)": round(r_sv["tr"]/1e6, 2),
            "Total Cost ($M)": round(r_sv["tc"]/1e6, 2),
            "Net CF ($M)": round(r_sv["nc"]/1e6, 2),
            "R/C Ratio": round(r_sv["rc"], 2),
            "NPV ($M)": round(npv_sv/1e6, 1),
            "Viable?": "✅ Yes" if npv_sv >= 0 else "❌ No",
            "lat": get_country_coords(country)[0],
            "lon": get_country_coords(country)[1],
        })

    if not sv_rows:
        st.warning("No countries found for selected filters.")
        st.stop()

    df_sv = pd.DataFrame(sv_rows).sort_values("NPV ($M)", ascending=False).reset_index(drop=True)

    viable_count = (df_sv["Viable?"] == "✅ Yes").sum()
    total_count  = len(df_sv)
    best_country = df_sv.iloc[0]["Country"] if total_count > 0 else "N/A"
    best_val     = df_sv.iloc[0]["NPV ($M)"] if total_count > 0 else 0
    worst_country= df_sv.iloc[-1]["Country"] if total_count > 0 else "N/A"

    sv_k1,sv_k2,sv_k3,sv_k4 = st.columns(4)
    sv_k1.markdown(kpi(f"{viable_count}/{total_count}", "Viable Markets", "NPV ≥ 0"), unsafe_allow_html=True)
    sv_k2.markdown(kpi(best_country, "Best Market", f"NPV: ${best_val}M"), unsafe_allow_html=True)
    sv_k3.markdown(kpi(worst_country, "Weakest Market", f"NPV: ${df_sv.iloc[-1]['NPV ($M)']}M"), unsafe_allow_html=True)
    sv_k4.markdown(kpi(f"{viable_count/total_count*100:.0f}%" if total_count else "N/A",
                        "Viability Rate", "Across countries"), unsafe_allow_html=True)

    # ── WORLD MAP ──────────────────────────────────────────────────
    st.markdown('<div class="sec-head">🗺️ World Viability Map</div>', unsafe_allow_html=True)

    df_map = df_sv[df_sv["lat"] != 0].copy()
    df_map["color_val"] = df_map["NPV ($M)"]
    df_map["marker_size"] = df_map["NPV ($M)"].clip(lower=0).apply(lambda x: max(6, min(24, 6+x/10)))
    df_map["hover"] = df_map.apply(lambda row:
        f"<b>{row['Country']}</b><br>NPV: ${row['NPV ($M)']}M<br>MBMs: {row['Active MBMs']}<br>{row['Viable?']}", axis=1)

    viable_df   = df_map[df_map["Viable?"] == "✅ Yes"]
    nonviable_df= df_map[df_map["Viable?"] == "❌ No"]
    no_data_df  = df_map[df_map["Active MBMs"] == "None"]

    fig_map = go.Figure()

    # Non-viable countries
    if len(nonviable_df) > 0:
        fig_map.add_trace(go.Scattergeo(
            lat=nonviable_df["lat"], lon=nonviable_df["lon"],
            mode="markers",
            marker=dict(size=7, color="#fca5a5", symbol="circle",
                        line=dict(width=0.5, color="#ef4444")),
            text=nonviable_df["hover"], hoverinfo="text",
            name="❌ Not Viable",
        ))

    # No MBM applicable
    if len(no_data_df) > 0:
        fig_map.add_trace(go.Scattergeo(
            lat=no_data_df["lat"], lon=no_data_df["lon"],
            mode="markers",
            marker=dict(size=5, color="#e5e7eb", symbol="circle",
                        line=dict(width=0.5, color="#9ca3af")),
            text=no_data_df["hover"], hoverinfo="text",
            name="⬜ No MBM Applicable",
        ))

    # Viable countries
    if len(viable_df) > 0:
        fig_map.add_trace(go.Scattergeo(
            lat=viable_df["lat"], lon=viable_df["lon"],
            mode="markers",
            marker=dict(
                size=viable_df["marker_size"],
                color=viable_df["color_val"],
                colorscale=[[0,"#d1fae5"],[0.5,"#059669"],[1,"#064e3b"]],
                showscale=True,
                colorbar=dict(title=dict(text="NPV ($M)", font=dict(size=10)), tickfont=dict(size=9)),
                line=dict(width=0.5, color="#065f46"),
                symbol="circle",
            ),
            text=viable_df["hover"], hoverinfo="text",
            name="✅ Viable",
        ))

    fig_map.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            showframe=False, showcoastlines=True, showland=True, showocean=True, showlakes=False,
            landcolor="#f1f5f9", oceancolor="#e0f2fe", coastlinecolor="#cbd5e1",
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)",
        ),
        height=500, margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", y=-0.05, font=dict(size=9, family="Inter")),
        font=dict(family="Inter", size=10),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ── BAR CHART ──────────────────────────────────────────────────
    st.markdown('<div class="sec-head">Country Viability Ranking (Top 40)</div>', unsafe_allow_html=True)
    top40 = df_sv.head(40)
    colors_sv = ["#059669" if v >= 0 else "#fca5a5" for v in top40["NPV ($M)"]]
    fig_sv = go.Figure(go.Bar(
        x=top40["Country"], y=top40["NPV ($M)"],
        marker_color=colors_sv,
        text=[f"{v:.1f}" for v in top40["NPV ($M)"]],
        textposition="outside", textfont=dict(size=8, color=FC),
    ))
    fig_sv.add_hline(y=0, line_color="#e2e8f0", line_width=1.5)
    fig_sv.update_layout(**pl(360, mb=90))
    fig_sv.update_layout(xaxis=dict(tickangle=-45), yaxis_title="NPV ($M)",
        title=dict(text=f"{sel_sv} — NPV by Country (Top 40)", font=dict(size=11,color=FC), y=0.98))
    st.plotly_chart(fig_sv, use_container_width=True)

    # ── MBM DECOMPOSITION ──────────────────────────────────────────
    st.markdown('<div class="sec-head">MBM Revenue Decomposition by Country (Top 30)</div>', unsafe_allow_html=True)
    top30_countries = df_sv.head(30)["Country"].tolist()
    mbm_breakdown_data = {}
    for country in top30_countries:
        r2 = compute_country_excel(country, st.session_state.p, t_sv, ti)
        mbm_breakdown_data[country] = r2["bd"]

    mbm_keys_plot = ["ETS","Carbon Tax","Fuel Mandate","CfD","CCfD","CBAM","CORSIA","IMO Levy","VCM/CDM","AMC","Feebate"]
    mbm_colors_plot = ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399","#6ee7b7","#a7f3d0","#d1fae5","#bbf7d0","#ecfdf5"]
    fig_mbm_c = go.Figure()
    for mkey, mcol in zip(mbm_keys_plot, mbm_colors_plot):
        vals = [mbm_breakdown_data[c].get(mkey, 0)/1e6 for c in top30_countries]
        fig_mbm_c.add_trace(go.Bar(name=mkey, x=top30_countries, y=vals, marker_color=mcol))
    fig_mbm_c.update_layout(**pl(360, mb=90))
    fig_mbm_c.update_layout(barmode="stack", xaxis=dict(tickangle=-45), yaxis_title="USD Million",
        title=dict(text="MBM Revenue Stack by Country", font=dict(size=11,color=FC), y=0.98),
        legend=dict(orientation="h", y=-0.35, font=dict(size=8)))
    st.plotly_chart(fig_mbm_c, use_container_width=True)

    # ── DATA TABLE ─────────────────────────────────────────────────
    st.markdown('<div class="sec-head">Full Country Data Table</div>', unsafe_allow_html=True)
    display_cols = ["Country","ISO3","Region","Active MBMs","MBM Rev ($M)","Direct Rev ($M)",
                    "Total Rev ($M)","Total Cost ($M)","Net CF ($M)","R/C Ratio","NPV ($M)","Viable?"]
    st.dataframe(df_sv[display_cols].style.bar(subset=["NPV ($M)","Net CF ($M)","MBM Rev ($M)"],
                 color="#bbf7d0", align="mid"), use_container_width=True, height=600)
    st.download_button("⬇ Download Spatial Viability CSV",
                       df_sv[display_cols].to_csv(index=False).encode(),
                       "spatial_viability.csv", "text/csv")
