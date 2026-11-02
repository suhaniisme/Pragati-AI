import streamlit as st
import pandas as pd
import urllib.parse
from backend.ml_engine import PragatiMLEngine
from backend.ai_copilot import PragatiAICopilot
from backend.campaign_engine import PragatiCampaignEngine

st.set_page_config(
    page_title="Paytm Pragati AI - Merchant Copilot",
    page_icon="💙",
    layout="wide"
)

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/24/Paytm_Logo.png", width=180)
st.sidebar.title("Paytm Pragati AI 🚀")
st.sidebar.subheader("Merchant Operating System")
st.sidebar.success("🟢 Local Offline Engine Active")

# Backend Engines
ml_engine = PragatiMLEngine()
ai_copilot = PragatiAICopilot()
campaign_engine = PragatiCampaignEngine()

kpis = ml_engine.get_kpis()

st.title("💙 Paytm Pragati AI — Merchant Growth Copilot")
st.caption("AI-Powered Business Intelligence, Soundbox Chatbot & Vision Receipt Processing")

# KPI Header
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Historical Sales", f"₹{kpis.get('total_sales', 0):,}")
col2.metric("7-Day Revenue", f"₹{kpis.get('recent_7_days_revenue', 0):,}")
col3.metric("Daily Avg Revenue", f"₹{kpis.get('avg_daily_sales', 0):,}")
col4.metric("Total Footfall", f"{kpis.get('total_footfall', 0):,}")

st.divider()

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Sales Prediction", 
    "🎙️ Soundbox Chatbot", 
    "📸 Vision Bill & Dispatch", 
    "🚀 1-Click QR Campaign"
])

# TAB 1: PREDICTIONS
with tab1:
    st.header("7-Day Sales & Demand Forecast")
    if st.button("Generate Forecast", type="primary"):
        predictions_df = ml_engine.predict_next_7_days()
        st.dataframe(predictions_df, use_container_width=True)
        st.line_chart(predictions_df.set_index("Date")["Predicted_Revenue"])

# TAB 2: SOUNDBOX CHATBOT
with tab2:
    st.header("Paytm Soundbox AI Chatbot 🔊")
    st.caption("Conversational Assistant for Store Management")

    if "soundbox_chat" not in st.session_state:
        st.session_state.soundbox_chat = [
            {"role": "assistant", "content": "Namaste! Main aapka Paytm Soundbox assistant hoon. Aaj ke dhandhe ya stock ke baare mein kuch bhi poochein!"}
        ]

    # Container forces history to render ABOVE the chat input box
    chat_container = st.container()

    user_input = st.chat_input("Ask Soundbox Assistant...")

    if user_input:
        st.session_state.soundbox_chat.append({"role": "user", "content": user_input})
        reply = ai_copilot.voice_soundbox_assistant(
            user_speech_text=user_input,
            conversation_history=st.session_state.soundbox_chat[:-1],
            kpis=kpis
        )
        st.session_state.soundbox_chat.append({"role": "assistant", "content": reply})

    with chat_container:
        for message in st.session_state.soundbox_chat:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    st.write("")
    if st.button("Clear Conversation History"):
        st.session_state.soundbox_chat = []
        st.rerun()

# TAB 3: RECEIPT SCANNER & DISPATCH (EXCEL / TEXT / WHATSAPP / GMAIL)
with tab3:
    st.header("Visual Receipt Scanner & Auto-Dispatch 📸")
    uploaded_file = st.file_uploader("Upload receipt image:", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Bill", width=280)
        
        if st.button("Scan & Extract Details", type="primary"):
            with st.spinner("Scanning bill details..."):
                bytes_data = uploaded_file.getvalue()
                extracted_text = ai_copilot.analyze_bill_or_inventory_image(bytes_data)
                st.session_state["last_receipt_text"] = extracted_text

    if "last_receipt_text" in st.session_state:
        st.subheader("🧾 Extracted Receipt Data")
        receipt_content = st.session_state["last_receipt_text"]
        st.markdown(receipt_content)

        st.divider()
        st.subheader("📤 Export & Dispatch Copy")

        col_fmt, col_dest = st.columns(2)
        with col_fmt:
            export_format = st.radio("Select Export Format:", ["Normal Text", "Excel Spreadsheet"])
        
        with col_dest:
            dispatch_channel = st.radio("Dispatch Via:", ["WhatsApp", "Email (Gmail)"])

        # Input field starts completely blank with placeholder hint
        if dispatch_channel == "WhatsApp":
            recipient_contact = st.text_input(
                "Enter Mobile Number (with country code):",
                value="",
                placeholder="e.g. 919876543210"
            )
        else:
            recipient_contact = st.text_input(
                "Enter Recipient Email Address:",
                value="",
                placeholder="e.g. customer@gmail.com"
            )

        # Download Buttons
        if export_format == "Excel Spreadsheet":
            excel_bytes = ai_copilot.generate_excel_bytes(receipt_content)
            st.download_button(
                label="📥 Download Excel File (.xlsx)",
                data=excel_bytes,
                file_name="receipt_details.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.download_button(
                label="📥 Download Text File (.txt)",
                data=receipt_content,
                file_name="receipt_details.txt",
                mime="text/plain"
            )

        # Dispatch Triggers
        if recipient_contact.strip():
            encoded_msg = urllib.parse.quote(f"Paytm Pragati AI - Receipt Details:\n\n{receipt_content}")
            
            if dispatch_channel == "WhatsApp":
                clean_phone = "".join([c for c in recipient_contact if c.isdigit()])
                wa_url = f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_msg}"
                st.link_button("📲 Send via WhatsApp", wa_url)
            
            elif dispatch_channel == "Email (Gmail)":
                subject = urllib.parse.quote("Paytm Pragati AI - Receipt Details")
                gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipient_contact}&su={subject}&body={encoded_msg}"
                st.link_button("✉️ Open & Send via Gmail", gmail_url)

# TAB 4: CAMPAIGNS
with tab4:
    st.header("1-Click Paytm QR Cashback Campaign Generator 🏷️")
    product_name = st.text_input("Product Name:", value="Basmati Rice 5kg")
    discount = st.slider("Cashback %:", 5, 50, 10)
    
    if st.button("Generate Campaign"):
        with st.spinner("Generating marketing copy..."):
            campaign_output = campaign_engine.generate_paytm_qr_offer(product_name, discount)
            st.markdown(campaign_output)