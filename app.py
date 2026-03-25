import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
# Your Sheet ID: 1vkO6nqSnQROCJqvJaYP2hi-5-zFR4T6iqPE6es_DRyg
SHEET_ID = "1vkO6nqSnQROCJqvJaYP2hi-5-zFR4T6iqPE6es_DRyg"
SHEET_NAME = "Sheet%201" 
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# Official MOBA Item & Price Database
ITEM_DATA = {
    "MOBA Cloth (Funeral - Red & Black)": 80.00,
    "MOBA Cloth (Ceremonial)": 80.00,
    "MOBA Cloth (General)": 80.00,
    "MOBA Cloth (Funeral - White & Black)": 80.00,
    "MOBA Tie": 200.00,
    "MOBA Sticker (RECTANGULARE- LONG)": 50.00,
    "Mfantsipim Sticker (SQUARE-SMALL)": 30.00,
    "Mfantsipim Sticker (SQUARE-BIG)": 50.00,
    "Mfantsipim Sticker (RECTANGULARE- LONG)": 50.00,
    "MFANTSIPIM Pennant": 100.00,
    "MFANTSIPIM CUFFLINKS": 150.00,
    "MFANTSIPIM PIN BADGE/LAPEL PIN": 50.00,
    "Mfantsipim T-Shirt (Ash)": 150.00,
    "Mfantsipim T-Shirt (White)": 150.00,
    "Mfantsipim T-Shirt (Red)": 150.00,
}

st.set_page_config(page_title="MOBA Sales Tracker", layout="wide", page_icon="🎓")

# --- DATA LOADING ---
@st.cache_data(ttl=10)
def load_data():
    return pd.read_csv(URL)

st.title("📊 MOBA Sales Ledger")

try:
    df = load_data()
    # Clean up any empty rows/columns from the Google Sheet import
    df = df.dropna(how="all").dropna(axis=1, how="all")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.info("💡 Data is synced from Google Sheets. Use the sidebar to generate new sales entries.")
except Exception:
    st.error("Could not connect to Google Sheets.")
    st.warning("Ensure the sheet is shared: 'Anyone with the link can view'.")

# --- SIDEBAR ENTRY FORM ---
with st.sidebar:
    st.header("📝 Log New Sale")
    with st.form("entry_form", clear_on_submit=True):
        date = st.date_input("Sales Date", datetime.now())
        buyer = st.text_input("Buyer Name")
        year = st.number_input("Year (Graduation)", min_value=1900, max_value=2026, value=2000)
        contact = st.text_input("Contact (Phone/Email)")
        
        selected_item = st.selectbox("Select Item", list(ITEM_DATA.keys()))
        unit_price = ITEM_DATA[selected_item]
        st.write(f"**Unit Price:** GHS {unit_price:.2f}")
        
        qty = st.number_input("Quantity", min_value=1, step=1, value=1)
        mode = st.selectbox("Payment Mode", ["CASH", "MOMO", "TRANSFER"])
        
        submit = st.form_submit_button("Generate Entry Row")

    if submit:
        total = unit_price * qty
        # Format: Date, Buyer, Year, Contact, Item, Price, Qty, Total, Mode
        entry_string = f"{date.strftime('%d/%m/%Y')},{buyer},{year},{contact},{selected_item},{unit_price},{qty},{total},{mode}"
        
        st.subheader("Copy & Paste this row:")
        st.code(entry_string)
        st.success("Now just paste this line into the next empty row of your Google Sheet.")