import os
import streamlit as st
import sqlite3
import pandas as pd
import logging
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "tmp", "gpu_metrics.db")

# Load log level from config
LOG_LEVEL = "INFO"
CONFIG_PATH = os.path.join(BASE_DIR, "config", "metrics_collector_config.yaml")
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as f:
        try:
            config = yaml.safe_load(f)
            LOG_LEVEL = config.get('log_level', 'INFO').upper()
        except Exception:
            pass
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger("streamlit_dashboard")

def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM gpu_metrics ORDER BY id DESC LIMIT 1000", conn)
        conn.close()
        logger.debug(f"Loaded {len(df)} rows from database.")
        return df
    except Exception as e:
        logger.warning(f"Could not load data: {e}")
        st.warning(f"Could not load data: {e}")
        return pd.DataFrame()

st.title("NVIDIA GPU Metrics Dashboard")
logger.info("Dashboard title set.")

data = load_data()
if data.empty:
    logger.info("No data available.")
    st.write("No data available.")
else:
    logger.info("Displaying data.")
    st.dataframe(data)
    logger.debug("Dataframe displayed.")
    # Dynamically plot all numeric columns except 'id' and 'timestamp'
    numeric_cols = [col for col in data.columns if col not in ['id', 'timestamp', 'name'] and pd.api.types.is_numeric_dtype(data[col])]
    logger.debug(f"Numeric columns identified: {numeric_cols}")
    for col in numeric_cols:
        logger.debug(f"Plotting line chart for {col}.")
        st.subheader(f"{col.replace('_', ' ').title()} Over Time")
        st.line_chart(data.set_index('timestamp')[col])
        logger.debug(f"Line chart plotted for {col}.")

    # Analytics: Moving Average (window=10)
    st.subheader("Analytics: Moving Average (window=10)")
    window = 10
    logger.debug(f"Calculating moving average with window size {window}.")
    for col in numeric_cols:
        logger.debug(f"Calculating moving average for {col}.")
        st.line_chart(data.set_index('timestamp')[col].rolling(window).mean(),
                      height=150, use_container_width=True)
        st.caption(f"Moving average for {col}")
        logger.debug(f"Moving average plotted for {col}.")

    # Analytics: Min/Max/Mean
    st.subheader("Analytics: Min/Max/Mean")
    stats = data[numeric_cols].agg(['min', 'max', 'mean'])
    logger.debug("Displaying min/max/mean statistics.")
    st.table(stats)
    logger.debug("Statistics table displayed.")

    # Analytics: Histogram for first numeric column (if exists)
    if numeric_cols:
        logger.debug(f"Displaying histogram for {numeric_cols[0]}.")
        st.subheader(f"Histogram: {numeric_cols[0].replace('_', ' ').title()}")
        st.bar_chart(data[numeric_cols[0]].value_counts().sort_index())
        logger.debug(f"Histogram displayed for {numeric_cols[0]}.")
