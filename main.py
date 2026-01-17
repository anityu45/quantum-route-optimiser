import streamlit as st
import config, state, frontend

st.set_page_config(page_title="Quantum Logistics", layout="wide")
config.load_css()
state.init_session()

st.title("⚛️ Quantum Logistics Optimizer")
frontend.render_sidebar()
frontend.render_map()
