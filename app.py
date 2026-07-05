import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# Set up page configuration with a modern widescreen layout
st.set_page_config(
    page_title="SampleRoute MVP Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# CUSTOM INJECTED CSS FOR DARK MODE & PREMIUM TYPOGRAPHY
# -------------------------------------------------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
        
        h1, h2, h3, .main-title {
            font-family: 'Playfair Display', 'Times New Roman', Georgia, serif !important;
            color: #FFFFFF !important; 
            font-weight: 700 !important;
        }
        
        div[data-testid="stMetric"] {
            background-color: #1E1E1E !important;
            border: 1px solid #333333 !important;
            padding: 20px 25px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease-in-out;
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 15px rgba(0, 204, 150, 0.15); /* Adds a futuristic neon-green glow on hover */
            border-color: #00CC96 !important;
            background-color: #252525 !important;
        }
        
        div[data-testid="stMetricLabel"] > div {
            font-size: 0.95rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            color: #B0B0B0 !important; 
            font-weight: 600 !important;
        }
        
        div[data-testid="stMetricValue"] > div {
            color: #FFFFFF !important; 
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# CACHED MOCK DATA LAYER
# -------------------------------------------------------------------------
@st.cache_data
def load_mock_data():
    np.random.seed(42)
    n_records = 600
    
    locations = ['JLT', 'Dubai Marina', 'Business Bay', 'Downtown Dubai']
    categories = ['Vegan/Plant-Based', 'Keto/Low-Carb', 'Corporate Lunch', 'General']
    products = ['Organic Protein Bar', 'Keto Electrolyte Drink', 'Premium Cold Brew', 'Baked Veggie Chips']
    kitchens = ['CloudKit JLT 1', 'Marina Ghost Eats', 'BizBay Central Kitchen', 'Downtown Gourmet Lab']
    
    data = {
        'Timestamp': pd.date_range(start='2026-05-01', periods=n_records, freq='h'),
        'Location': np.random.choice(locations, n_records, p=[0.4, 0.3, 0.2, 0.1]),
        'Category': np.random.choice(categories, n_records),
        'Product': np.random.choice(products, n_records),
        'Kitchen': np.random.choice(kitchens, n_records),
        'Dispatched': [1] * n_records,
        'QR_Scanned': np.random.choice([0, 1], n_records, p=[0.83, 0.17]), 
        'Rating': np.random.choice([3, 4, 5], n_records, p=[0.1, 0.3, 0.6])
    }
    
    df = pd.DataFrame(data)
    df.loc[df['QR_Scanned'] == 0, 'Rating'] = np.nan
    return df

df_logs = load_mock_data()

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# -------------------------------------------------------------------------
# SIDEBAR APPLICATION CONTROLS & LOGO
# -------------------------------------------------------------------------
try:
    if os.path.exists('logo.png'):
        st.sidebar.image('logo.png', use_container_width=True)
    elif os.path.exists('logo.jpg'):
        st.sidebar.image('logo.jpg', use_container_width=True)
except Exception:
    pass

st.sidebar.title("📦 SampleRoute Portal")
st.sidebar.markdown("---")

portal_view = st.sidebar.radio(
    "Select Platform Dashboard View:",
    [
        "🌐 The Vision (Genesis)", 
        "🚀 FMCG Brand Portal", 
        "🍳 Cloud Kitchen Portal",
        "🧠 AI Demand Forecaster",
        "⚙️ System Architecture"
    ]
)

# Pushing the author info to the very bottom
st.sidebar.markdown("---")
st.sidebar.markdown("<br><br><br><br><br>", unsafe_allow_html=True) # Adds vertical space
st.sidebar.caption("Individual assignment done by Syed Ali Kavish Abdi")
st.sidebar.caption("MGB Term 3 | Section B")

# -------------------------------------------------------------------------
# PAGE 0: THE VISION (LANDING PAGE)
# -------------------------------------------------------------------------
if "The Vision (Genesis)" in portal_view:
    st.title("SampleRoute: The Blue Ocean of Product Sampling")
    st.markdown("##### *Transforming Independent Cloud Kitchens into Highly Targeted Micro-Distribution Networks.*")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("❌ The Legacy Ecosystem")
        st.markdown("""
        * **Monopoly Control:** Tech giants lock out mid-tier FMCG brands.
        * **Scattergun Marketing:** Traditional retail sampling wastes spend on the wrong demographic.
        * **Data Black Holes:** Brands hand out free samples but rarely capture consumer feedback.
        """)
        
    with col2:
        st.success("🟢 The SampleRoute Node Network")
        st.markdown("""
        * **Spatial Monetization:** Utilizing the empty space in standard food delivery bags.
        * **Hyper-Targeting:** Injecting samples directly into specific consumer diets (e.g., Vegan snacks to JLT).
        * **Zero-Party Data Generation:** Gamified QR codes capture high-fidelity behavioral data.
        """)
        
    st.markdown("---")
    st.subheader("🔄 Automated Workflow Topology")
    st.info("📦 **Brand Deploys Inventory** ➡️ 🍳 **Node Injects Sample** ➡️ 📱 **Consumer Scans UI** ➡️ 📊 **Data Aggregated in Real-Time**")

# -------------------------------------------------------------------------
# PAGE 1: FMCG BRAND PORTAL 
# -------------------------------------------------------------------------
elif "FMCG Brand Portal" in portal_view:
    st.title("FMCG Brand Analytics Portal")
    st.markdown("##### *Live Campaign ROI & Zero-Party Data Strategy Insights*")
    st.markdown("---")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_product = st.selectbox("Select Active Packaged Food Campaign:", df_logs['Product'].unique())
    with col_f2:
        selected_loc = st.multiselect("Filter Target Delivery Zones:", df_logs['Location'].unique(), default=df_logs['Location'].unique())
        
    filtered_df = df_logs[(df_logs['Product'] == selected_product) & (df_logs['Location'].isin(selected_loc))]
    
    total_dispatched = filtered_df['Dispatched'].sum()
    total_scans = filtered_df['QR_Scanned'].sum()
    scan_rate = (total_scans / total_dispatched * 100) if total_dispatched > 0 else 0.0
    avg_rating = filtered_df['Rating'].mean()
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Samples Dispatched", value=f"{total_dispatched:,}")
    m2.metric(label="Zero-Party QR Scans", value=f"{total_scans:,}")
    m3.metric(label="Conversion Rate", value=f"{scan_rate:.1f}%")
    m4.metric(label="Avg Consumer Rating", value=f"⭐ {avg_rating:.1f}/5.0" if not np.isnan(avg_rating) else "N/A")
    
    st.markdown("---")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader("📍 Geofenced Delivery Penetration")
        loc_counts = filtered_df.groupby('Location')['Dispatched'].sum().reset_index()
        fig_loc = px.bar(loc_counts, x='Location', y='Dispatched', 
                         color='Location', title=f"Sample Dispatches: {selected_product}",
                         color_discrete_sequence=px.colors.qualitative.Pastel,
                         template="plotly_dark")
        fig_loc.update_layout(showlegend=False)
        st.plotly_chart(fig_loc, use_container_width=True)
        
    with col_c2:
        st.subheader("🎯 Loop Closure Conversion Analysis")
        scan_counts = filtered_df['QR_Scanned'].map({1: 'Scanned (Feedback Saved)', 0: 'Unscanned Space'}).value_counts().reset_index()
        scan_counts.columns = ['Status', 'Count']
        fig_pie = px.pie(scan_counts, values='Count', names='Status', 
                         color='Status', color_discrete_map={'Scanned (Feedback Saved)': '#00CC96', 'Unscanned Space': '#444444'},
                         hole=0.4, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.subheader("📥 Export Zero-Party Consumer Data")
    
    csv_data = convert_df_to_csv(filtered_df)
    st.download_button(
        label="Download Active Campaign CSV",
        data=csv_data,
        file_name=f"{selected_product.replace(' ', '_')}_SampleRoute_Data.csv",
        mime='text/csv',
    )

# -------------------------------------------------------------------------
# PAGE 2: CLOUD KITCHEN PORTAL
# -------------------------------------------------------------------------
elif "Cloud Kitchen Portal" in portal_view:
    st.title("Independent Cloud Kitchen Portal")
    st.markdown("##### *Monetizing Underutilized Empty Delivery Bag Space*")
    st.markdown("---")
    
    selected_kitchen = st.selectbox("Select Active Cloud Kitchen Branch:", df_logs['Kitchen'].unique())
    kitchen_df = df_logs[df_logs['Kitchen'] == selected_kitchen]
    
    k_dispatched = kitchen_df['Dispatched'].sum()
    payout_per_sample = 0.87  
    total_earnings = k_dispatched * payout_per_sample
    
    allocated_stock = 750
    remaining_stock = allocated_stock - k_dispatched
    
    km1, km2, km3 = st.columns(3)
    km1.metric(label="Samples Injected in Food Bags", value=f"{k_dispatched:,} Deliveries")
    km2.metric(label="Net Passive Revenue Earned", value=f"AED {total_earnings:,.2f}")
    km3.metric(label="Remaining On-Site Sample Inventory", value=f"{remaining_stock} Units", delta=f"-{k_dispatched} units dispatched")
    
    st.markdown("---")
    
    st.subheader("📋 Live Real-Time Bagging Integration Logs")
    kitchen_display_df = kitchen_df[['Timestamp', 'Product', 'Location', 'QR_Scanned']].copy()
    kitchen_display_df['QR_Scanned'] = kitchen_display_df['QR_Scanned'].map({1: "✅ Completed Scan", 0: "⏳ In-Transit / Pending"})
    kitchen_display_df.columns = ['Timestamp (GST)', 'Injected Product Sample', 'Geographic Market', 'Status Loop']
    
    st.dataframe(kitchen_display_df.sort_values(by='Timestamp (GST)', ascending=False).head(12), use_container_width=True)

# -------------------------------------------------------------------------
# PAGE 3: AI DEMAND FORECASTER 
# -------------------------------------------------------------------------
elif "AI Demand Forecaster" in portal_view:
    st.title("AI Demand Forecaster & Unit Economics")
    st.markdown("##### *Interactive Scalability Sandbox*")
    st.markdown("---")
    
    st.markdown("Use the parameters below to run simulated revenue models based on the SampleRoute algorithm.")
    
    col_slider, col_chart = st.columns([1.2, 2])
    
    with col_slider:
        st.subheader("⚙️ Scenario Parameters")
        volume = st.slider("Target Sample Volume (Monthly)", min_value=10000, max_value=500000, value=120000, step=10000)
        cps = st.slider("Cost Per Sample (CPS) Billed to Brand (AED)", min_value=1.0, max_value=5.0, value=2.5, step=0.1)
        kitchen_share = st.slider("Kitchen Revenue Share %", min_value=10, max_value=50, value=35, step=1)
        
        gross_revenue = volume * cps
        payout_to_kitchens = gross_revenue * (kitchen_share / 100)
        platform_gross_profit = gross_revenue - payout_to_kitchens
        
    with col_chart:
        st.subheader("📈 Projected Yield Outcomes")
        c1, c2, c3 = st.columns(3)
        c1.metric("Gross Revenue", f"AED {gross_revenue:,.0f}")
        c2.metric("Kitchen Payouts", f"AED {payout_to_kitchens:,.0f}")
        c3.metric("Platform Gross Profit", f"AED {platform_gross_profit:,.0f}")
        
        chart_data = pd.DataFrame({
            "Category": ["Platform Gross Profit", "Cloud Kitchen Payouts"],
            "Amount (AED)": [platform_gross_profit, payout_to_kitchens]
        })
        
        fig_finance = px.pie(chart_data, values="Amount (AED)", names="Category", 
                             title="Revenue Split Architecture",
                             color="Category", color_discrete_map={"Platform Gross Profit": "#00CC96", "Cloud Kitchen Payouts": "#333333"},
                             hole=0.5, template="plotly_dark")
        st.plotly_chart(fig_finance, use_container_width=True)

# -------------------------------------------------------------------------
# PAGE 4: SYSTEM ARCHITECTURE
# -------------------------------------------------------------------------
elif "System Architecture" in portal_view:
    st.title("⚙️ System Architecture & Tech Stack")
    st.markdown("##### *How SampleRoute is built to scale.*")
    st.markdown("---")
    
    st.markdown("""
    To ensure seamless integration with our B2B partners without disrupting kitchen operations, SampleRoute utilizes a modern, asset-light tech stack:
    
    * **Frontend Dashboard:** Built on Python & Streamlit for rapid iteration and real-time data visualization.
    * **Data Aggregation:** Pandas & NumPy power the data cleaning and transformation pipeline.
    * **Data Visualization:** Plotly enables responsive, interactive geographic and financial charts.
    * **QR Loop Infrastructure:** Unique generated QR codes linked to customized, gamified survey forms capturing zero-party data and instantly updating the cloud database.
    """)
    
    with st.expander("View Code Deployment Structure"):
        st.code("""
        ├── app.py                 # Main Streamlit Application
        ├── requirements.txt       # Dependencies (pandas, streamlit, plotly)
        ├── logo.png               # Brand Assets
        └── README.md              # Documentation
        """, language="bash")
