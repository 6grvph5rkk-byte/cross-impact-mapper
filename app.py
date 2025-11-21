import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cross-Impact Mapping – pi-studio / MA Designing Education",
    layout="wide",
)

# --------------------------------------------------------------------
# Header & branding
# --------------------------------------------------------------------
st.title("Cross-Impact Mapping Tool – pi-studio / MA Designing Education")

st.markdown(
    """
This is a tool for organisations to explore **factors of influence** and use it in
relationship to **future prospecting**, and in relationship to the  
**MA in Designing Education at Goldsmiths, University of London**.

Cross-impact analysis was originally developed by **Gordon & Helmer (1966)** in futures s
