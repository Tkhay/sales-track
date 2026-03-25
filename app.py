import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
SHEET_ID = "1vkO6nqSnQROCJqvJaYP2hi-5-zFR4T6iqPE6es_DRyg"
SHEET_NAME = "Sheet%201" 
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

ITEM_DATA = {
    "MOBA Cloth (Funeral - R&B)": 80.0, 
    "MOBA Cloth (Ceremonial)": 80.0,
    "MOBA Cloth (General)": 80.0, 
    "MOBA Cloth (Funeral - W&B)": 80.0,
    "MOBA Tie": 200.0, 
    "MOBA Sticker (RECT-LONG)": 40.0,
    "Mfantsipim Sticker (SQ-SMALL)": 30.0, 
    "Mfantsipim Sticker (SQ-BIG)": 50.0,
    "MFANTSIPIM Pennant": 100.0, 
    "MFANTSIPIM CUFFLINKS": 150.0,
    "MFANTSIPIM PIN/LAPEL": 50.0, 
    "Mfantsipim T-Shirt (Ash)": 150.0,
    "Mfantsipim T-Shirt (White)": 150.0, 
    "Mfantsipim T-Shirt (Red)": 150.0,
    "Mfantsipim Mug": 80.0,
}

st.set_page_config(page_title="MOBA Sales Tracker", layout="wide", page_icon="🎓")

@st.cache_data(ttl=5)
def load_data():
    try:
        return pd.read_csv(URL)
    except:
        return pd.DataFrame()

st.title("📊 MOBA Sales Ledger")

df = load_data()
if not df.empty:
    st.dataframe(df.dropna(how="all").dropna(axis=1, how="all"), width='stretch', hide_index=True)

# --- SIDEBAR CART SYSTEM ---
with st.sidebar:
    st.header("📝 Log New Sale")
    
    date = st.date_input("Sales Date", datetime.now())
    buyer = st.text_input("Buyer Name (Optional)")
    year = st.number_input("Year (Optional)", value=0, step=1)
    contact = st.text_input("Contact (Optional)")
    
    st.divider()
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    st.subheader("🛒 Add to Cart")
    col1, col2 = st.columns([2, 1])
    with col1:
        item_to_add = st.selectbox("Select Item", list(ITEM_DATA.keys()))
    with col2:
        qty_to_add = st.number_input("Qty", min_value=1, value=1)
    
    if st.button("Add Item", width='stretch'):
        st.session_state.cart.append({
            "name": item_to_add,
            "qty": qty_to_add,
            "price": ITEM_DATA[item_to_add] * qty_to_add
        })

    if st.session_state.cart:
        st.write("---")
        total_price = 0
        summary_parts = []
        
        for i, entry in enumerate(st.session_state.cart):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.write(f"**{entry['qty']}x** {entry['name']}  \n(GHS {entry['price']:.2f})")
            with c2:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
            
            total_price += entry['price']
            summary_parts.append(f"{entry['qty']}x {entry['name']}")
        
        st.write(f"### Total: GHS {total_price:.2f}")
        
        mode = st.selectbox("Payment Mode", ["CASH", "MOMO", "TRANSFER"])
        
        if st.button("Generate Final Row", width='stretch'):
            items_combined = " | ".join(summary_parts)
            disp_year = year if year > 0 else ""
            disp_buyer = buyer if buyer else "-"
            disp_contact = contact if contact else "-"
            formatted_date = date.strftime('%d/%m/%Y')
            
            # Format exactly for pasting
            entry_string = f"{formatted_date},{disp_buyer},{disp_year},{disp_contact},\"{items_combined}\",,,{total_price},{mode}"
            
            st.subheader("Copy this row:")
            st.code(entry_string, language="text")
            
        if st.button("Clear All Items", type="secondary"):
            st.session_state.cart = [] # Fixed the .reset() bug
            st.rerun()
    else:
        st.info("Your cart is empty.")