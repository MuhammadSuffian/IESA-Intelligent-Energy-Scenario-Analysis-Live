import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import mysql.connector
from mysql_con import get_connection, fetch_table_data
import base64
from PIL import Image
import time
import os

# Importing other dashboard modules
import energy_by_souce
import total_energy
import electricty
import gas
from utils.logger import setup_logger
import final_dashboard
import final_iesa_data_planner
import final_scenerio_analysis
import final_prediction_engine
import final_personalized_recommendations
import final_wisdom_mining

# --- Session State Initialization ---
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'
if 'df' not in st.session_state:
    st.session_state.df = None
if 'transactions' not in st.session_state:
    st.session_state.transactions = None
if 'run_analysis' not in st.session_state:
    st.session_state.run_analysis = False

# --- Page Configuration ---
st.set_page_config(
    page_title="IESA Dashboard",
    page_icon="📊",
    initial_sidebar_state=st.session_state.sidebar_state,
    layout="wide",
    menu_items={
        'Get Help': 'https://www.linkedin.com/company/104830960',
        'Report a bug': 'https://www.linkedin.com/company/104830960',
        'About': (
            "Intelligent Energy Scenario Analysis (IESA) is an AI-based business intelligence project "
            "that will revolutionize energy scenario analysis by utilizing AI and machine learning to "
            "provide accurate and efficient insights.\n\n"
            "Developers:\n\n"
            "• M. Suffian Tafoor\n\n"
            "• M. Yasir Khan\n\n"
            "• M. Farzam Baig\n\n"
        )
    }
)

# --- Navigation Menu ---
selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Data Planner", "Scenario", "Wisdom Mining", "Prediction", "IESA Assistant"],
    icons=["clipboard-data", "bar-chart", "graph-up", "graph-up-arrow", "robot", "robot"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important", 
            "background-color": "transparent",
            "margin-top": "0px", 
            "position": "relative", 
            "z-index": "100",
            "border-radius": "0px",
            "box-shadow": "none",
            "border": "none",
            "border-bottom": "2px solid #e0e5eb",
            "margin-bottom": "15px"
         },
        "icon": {"color": "106466", "font-size": "18px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "--hover-color": "rgba(255,255,255,0.1)",
            "padding": "10px",
            "margin": "0 2px",
            "position": "relative",
            "border": "none",
            "background-color": "transparent"
        },
        "nav-link-selected": {
            "background-color": "transparent", 
            "color": "#106466",
            "font-weight": "600",
            "border-radius": "0px",
            "border": "none",
            "border-bottom": "3px solid #73c8a9"
        },
    }
)

# --- Setup Logger ---
logger = setup_logger("iesa_dashboard")

# --- Smooth Loader & Transition Logic ---
def render_page(page_name, load_func):
    """Encapsulates the page loading logic with a visual spinner and fade-in effect."""
    logger.info(f"User navigated to {page_name}")
    
    # Injecting CSS for a smooth fade-in effect
    st.markdown("""
        <style>
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        .main-content {
          animation: fadeIn 0.6s ease-in-out;
        }
        </style>
    """, unsafe_allow_html=True)
        
    # Loader
    with st.spinner(f"⚡ Synchronizing {page_name}..."):
        # Small delay to ensure the spinner is visible to the user
        time.sleep(0.4) 
        
        # Create a container for the fade-in animation
        with st.container():
            st.markdown('<div class="main-content">', unsafe_allow_html=True)
            load_func(logger)
            st.markdown('</div>', unsafe_allow_html=True)

# --- Page Mapping ---
pages = {
    "Dashboard": final_dashboard.load_dash,
    "Data Planner": final_iesa_data_planner.load_data_planner,
    "Scenario": final_scenerio_analysis.load_scenerio_analysis,
    "Wisdom Mining": final_wisdom_mining.load_wisdom_mining,
    "Prediction": final_prediction_engine.load_prediction_engine,
    "IESA Assistant": final_personalized_recommendations.load_personalized_recommendations
}

# --- Execution ---
if selected in pages:
    render_page(selected, pages[selected])