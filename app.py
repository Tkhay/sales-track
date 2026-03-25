import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
SHEET_ID = "1vkO6nqSnQROCJqvJaYP2hi-5-zFR4T6iqPE6es_DRyg"
SHEET_NAME = "Sheet%201" 
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

ITEM_DATA = {
    "MOBA Cloth (Funeral - R&B)": 80.0, "MOBA Cloth (Ceremonial)": 80.0,
    "MOBA Cloth (General)": 80.0, "MOBA Cloth (Funeral - W&B)": 80.0,
    "MOBA Tie": 200.0, "MOBA Sticker (RECT-LONG)": 50.0,
    "Mfantsipim Sticker (SQ-SMALL)": 30.0, "Mfantsipim Sticker (SQ-BIG)": 50.0,
    "MFANTSIPIM Pennant": 100.0, "MFANTSIPIM CUFFLINKS": 150.0,
    "MFANTSIPIM PIN/LAPEL": 50.0, "Mfantsipim T-Shirt (Ash)": 150.0,
    "Mfantsipim T-Shirt (White)": 150.0, "Mfantsipim T-Shirt (Red)": 150.0,
}

st.set_page_config(page_title="MOBA Sales Tracker", layout="wide", page_icon="🎓")

@st.cache_data(ttl=5)
def load_data():
    return pd.read_csv(URL)

st.title("📊 MOBA Sales Ledger")

try:
    df = load_data().dropna(how="all").dropna(axis=1, how="all")
    # Updated to 2026 Streamlit standards
    st.dataframe(df, width='stretch', hide_index=True)
except Exception:
    st.error("Connection Error. Check Sheet Sharing settings.")

# --- SIDEBAR ENTRY FORM ---
with st.sidebar:
    st.header("📝 Log New Sale")
    with st.form("entry_form", clear_on_submit=True):
        date = st.date_input("Sales Date", datetime.now())
        buyer = st.text_input("Buyer Name (Optional)")
        year = st.number_input("Year (Optional)", value=0, step=1)
        contact = st.text_input("Contact (Optional)")
        
        selected_items = st.multiselect("Select Merchandise", list(ITEM_DATA.keys()))
        subtotal = sum(ITEM_DATA[item] for item in selected_items)
        st.write(f"**Current Total:** GHS {subtotal:.2f}")
        
        mode = st.selectbox("Payment Mode", ["CASH", "MOMO", "TRANSFER"])
        submit = st.form_submit_button("Generate Entry Row")

    if submit and selected_items:
        items_combined = " | ".join(selected_items)
        disp_year = year if year > 0 else ""
        disp_buyer = buyer if buyer else "-"
        disp_contact = contact if contact else "-"
        
        # Row Format for copy-pasting
        entry_string = f"{date.strftime('%d/%m/%Y')},{disp_buyer},{disp_year},{disp_contact},\"{items_combined}\",{subtotal},1,{subtotal},{mode}"
        
        st.subheader("Copy & Paste this row:")
        st.code(entry_string)
        st.success("Paste this into your Google Sheet.")
    elif submit and not selected_items:
        st.warning("Please select at least one item.")