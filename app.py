import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import sqlite3
import os

# Configure Page
st.set_page_config(page_title="Fraud Detection System", page_icon="💳", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        color: #fff;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
    }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('creditcard_sample.csv')
        return df
    except:
        return None

@st.cache_resource
def load_model():
    try:
        return joblib.load('fraud_model.pkl')
    except:
        return None

def log_prediction(time, amount, predicted_class):
    conn = sqlite3.connect('fraud_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (time, amount, predicted_class)
        VALUES (?, ?, ?)
    ''', (time, amount, int(predicted_class)))
    conn.commit()
    conn.close()

df = load_data()
model = load_model()

# Header
st.title("💳 Real-time Credit Card Fraud Detection")
st.markdown("Advanced machine learning system to detect fraudulent transactions.")

page = st.sidebar.radio("Navigation", ["📈 Dashboard", "🔍 Test Transaction"])

if page == "📈 Dashboard":
    if df is not None:
        st.header("Transaction Analysis")
        
        frauds = len(df[df['Class'] == 1])
        legit = len(df[df['Class'] == 0])
        
        col1, col2, col3 = st.columns(3)
        col1.markdown(f'<div class="metric-card"><h3 style="color:#94a3b8;">Sample Size</h3><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="metric-card"><h3 style="color:#ff416c;">Fraudulent</h3><h2>{frauds}</h2></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="metric-card"><h3 style="color:#00b09b;">Legitimate</h3><h2>{legit}</h2></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Transaction Amount Distribution")
            fig1 = px.box(df, x="Class", y="Amount", color="Class", 
                          template="plotly_dark", 
                          color_discrete_sequence=['#00b09b', '#ff416c'],
                          labels={"Class": "0: Legit, 1: Fraud"})
            # scale y axis to log to see better
            fig1.update_yaxes(type="log")
            st.plotly_chart(fig1, use_container_width=True)
            
        with col_chart2:
            st.subheader("Time vs Amount (Fraud focus)")
            fig2 = px.scatter(df, x="Time", y="Amount", color="Class", 
                              template="plotly_dark", opacity=0.7,
                              color_discrete_sequence=['#00b09b', '#ff416c'])
            st.plotly_chart(fig2, use_container_width=True)
            
    else:
        st.warning("Please run the `prepare_deployment.py` script first to generate sample data.")

elif page == "🔍 Test Transaction":
    st.header("Test a Custom Transaction")
    st.markdown("Input mock transaction features to see the model's prediction.")
    
    if model is None:
        st.error("Model not found! Run `prepare_deployment.py`.")
    else:
        with st.form("test_form"):
            col1, col2 = st.columns(2)
            with col1:
                time = st.number_input("Time (seconds from start)", value=0.0)
                amount = st.number_input("Transaction Amount ($)", value=150.0)
                v1 = st.number_input("V1 (PCA Feature)", value=-1.3)
                v2 = st.number_input("V2 (PCA Feature)", value=0.9)
            with col2:
                v3 = st.number_input("V3 (PCA Feature)", value=1.1)
                v4 = st.number_input("V4 (PCA Feature)", value=-0.5)
                v5 = st.number_input("V5 (PCA Feature)", value=0.3)
                st.markdown("<br><br>", unsafe_allow_html=True)
                submit = st.form_submit_button("Detect Fraud")
                
        if submit:
            # We need 30 features in total. For this mock UI, we will fill the rest with 0
            features = [time, v1, v2, v3, v4, v5] + [0]*23 + [amount]
            
            prediction = model.predict([features])[0]
            probability = model.predict_proba([features])[0][1]
            
            # Log to SQLite
            log_prediction(time, amount, prediction)
            
            if prediction == 1:
                st.markdown(f"""
                <div style="background: rgba(255, 65, 108, 0.1); padding: 30px; border-radius: 15px; border: 1px solid #ff416c; text-align: center;">
                    <h1 style="color: #ff416c; margin:0;">🚨 FRAUD DETECTED</h1>
                    <p style="margin-top:10px; font-size:1.2rem;">Confidence: {probability*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(0, 176, 155, 0.1); padding: 30px; border-radius: 15px; border: 1px solid #00b09b; text-align: center;">
                    <h1 style="color: #00b09b; margin:0;">✅ LEGITIMATE TRANSACTION</h1>
                    <p style="margin-top:10px; font-size:1.2rem;">Fraud Probability: {probability*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
