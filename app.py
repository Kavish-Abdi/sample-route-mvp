import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set up page configuration with a modern widescreen layout
st.set_page_config(
    page_title="SampleRoute MVP Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# CUSTOM INJECTED CSS FOR PREMIUM TYPOGRAPHY & INTERACTIVE CARD STYLING
# -------------------------------------------------------------------------
st.markdown("""
    <style>
        /* Import premium serif fonts for headers */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
        
        /* Apply elegant serif typography globally to headers */
        h1, h2, h3, .main-title {
            font-family: 'Playfair Display', 'Times New Roman', Georgia, serif !important;
            color: #1A252C !important;
            font-weight: 700 !important;
        }
        
        /* Custom styled dynamic metric container cards */
        div[data-testid="stMetric"] {
            background-color: #F8F9FA;
            border: 1px solid #E9ECEF;
            padding: 20px 25px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
            transition: all 0.3s ease-in-out;
        }
        
        /* Interactive hover state effect for dashboard cards */
        div[data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
            border-color: #CED4DA;
            background-color: #FFFFFF;
        }
        
        /* Metric Label Styling */
        div[data-testid="stMetricLabel"] > div {
            font-size: 0.95rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            color: #6C757D !important;
            font-weight: 600 !important;
        }
    </style>
""", unsafe_content_type=True)

# -------------------------------------------------------------------------
# CACHED MOCK DATA LAYER (Simulating real-time Pandas pipeline)
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
        'Timestamp': pd.date_range(start='2026-05-01', periods=n_records, freq='H'),
        'Location': np.random.choice(locations, n_records, p=[0.4, 0.3, 0.2, 0.1]),
        'Category': np.random.choice(categories, n_records),
        'Product': np.random.choice(products, n_records),
        'Kitchen': np.random.choice(kitchens, n_records),
        'Dispatched': [1] * n_records,
        'QR_Scanned': np.random.choice([0, 1], n_records, p=[0.83, 0.17]), # ~17% target conversion
        'Rating': np.random.choice([3, 4, 5], n_records, p=[0.1, 0.3, 0.6])
    }
    
    df = pd.DataFrame(data)
    df.loc[df['QR_Scanned'] == 0, 'Rating'] = np.nan
    return df

df_logs = load_mock_data()

# -------------------------------------------------------------------------
# SIDEBAR APPLICATION CONTROLS
# -------------------------------------------------------------------------
st.sidebar.title("📦 SampleRoute Portal")
st.sidebar.markdown("---")
portal_view = st.sidebar.radio(
    "Select Platform Dashboard View:",
    ["🚀 FMCG Brand Portal", "🍳 Cloud Kitchen Portal"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎓 Academic Information")
st.sidebar.caption("**Course:** Entrepreneurship Project")
st.sidebar.caption("**Institution:** SP Jain School of Global Management")
st.sidebar.caption("**Location Focus:** Dubai Hubs")

# -------------------------------------------------------------------------
# VIEW 1: FMCG BRAND PORTAL
# -------------------------------------------------------------------------
if "FMCG Brand Portal" in portal_view:
    st.title("FMCG Brand Analytics Portal")
    st.markdown("##### *Live Campaign ROI & Zero-Party Data Strategy Insights*")
    st.markdown("---")
    
    # Dynamic Filtering Row
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_product = st.selectbox("Select Active Packaged Food Campaign:", df_logs['Product'].unique())
    with col_f2:
        selected_loc = st.multiselect("Filter Target Delivery Zones:", df_logs['Location'].unique(), default=df_logs['Location'].unique())
        
    filtered_df = df_logs[(df_logs['Product'] == selected_product) & (df_logs['Location'].isin(selected_loc))]
    
    # Calculate Core Live Metrics
    total_dispatched = filtered_df['Dispatched'].sum()
    total_scans = filtered_df['QR_Scanned'].sum()
    scan_rate = (total_scans / total_dispatched * 100) if total_dispatched > 0 else 0.0
    avg_rating = filtered_df['Rating'].mean()
    
    # Interactive Metrics Cards (Hover animations applied via CSS)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Samples Dispatched", value=f"{total_dispatched:,}")
    m2.metric(label="Zero-Party QR Scans", value=f"{total_scans:,}")
    m3.metric(label="Conversion Rate", value=f"{scan_rate:.1f}%")
    m4.metric(label="Avg Consumer Rating", value=f"⭐ {avg_rating:.1f}/5.0" if not np.isnan(avg_rating) else "N/A")
    
    st.markdown("---")
    
    # Data Visualization Layout
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader("📍 Geofenced Delivery Penetration")
        loc_counts = filtered_df.groupby('Location')['Dispatched'].sum().reset_index()
        fig_loc = px.bar(loc_counts, x='Location', y='Dispatched', 
                         color='Location', title=f"Sample Dispatches: {selected_product}",
                         color_discrete_sequence=px.colors.qualitative.Muted,
                         template="plotly_white")
        fig_loc.update_layout(showlegend=False)
        st.plotly_chart(fig_loc, use_container_width=True)
        
    with col_c2:
        st.subheader("🎯 Loop Closure Conversion Analysis")
        scan_counts = filtered_df['QR_Scanned'].map({1: 'Scanned (Feedback Saved)', 0: 'Unscanned Space'}).value_counts().reset_index()
        scan_counts.columns = ['Status', 'Count']
        fig_pie = px.pie(scan_counts, values='Count', names='Status', 
                         color='Status', color_discrete_map={'Scanned (Feedback Saved)': '#1A252C', 'Unscanned Space': '#E9ECEF'},
                         hole=0.4, template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)

# -------------------------------------------------------------------------
# VIEW 2: CLOUD KITCHEN PORTAL
# -------------------------------------------------------------------------
else:
    st.title("Independent Cloud Kitchen Portal")
    st.markdown("##### *Monetizing Underutilized Empty Delivery Bag Space*")
    st.markdown("---")
    
    selected_kitchen = st.selectbox("Select Active Cloud Kitchen Branch:", df_logs['Kitchen'].unique())
    kitchen_df = df_logs[df_logs['Kitchen'] == selected_kitchen]
    
    # Calculate Yield Metrics
    k_dispatched = kitchen_df['Dispatched'].sum()
    payout_per_sample = 0.87  # Operational contract payout calculated in Appendix A
    total_earnings = k_dispatched * payout_per_sample
    
    allocated_stock = 750
    remaining_stock = allocated_stock - k_dispatched
    
    # Operational Cards
    km1, km2, km3 = st.columns(3)
    km1.metric(label="Samples Injected in Food Bags", value=f"{k_dispatched:,} Deliveries")
    km2.metric(label="Net Passive Revenue Earned", value=f"AED {total_earnings:,.2f}")
    km3.metric(label="Remaining On-Site Sample Inventory", value=f"{remaining_stock} Units", delta=f"-{k_dispatched} units dispatched")
    
    st.markdown("---")
    
    # Dynamic Data Table Filter
    st.subheader("📋 Live Real-Time Bagging Integration Logs")
    kitchen_display_df = kitchen_df[['Timestamp', 'Product', 'Location', 'QR_Scanned']].copy()
    kitchen_display_df['QR_Scanned'] = kitchen_display_df['QR_Scanned'].map({1: "✅ Completed Scan", 0: "⏳ In-Transit / Pending"})
    kitchen_display_df.columns = ['Timestamp (GST)', 'Injected Product Sample', 'Geographic Market', 'Status Loop']
    
    st.dataframe(kitchen_display_df.sort_values(by='Timestamp (GST)', ascending=False).head(12), use_container_width=True)
    
    st.info("💡 **Operational Directive:** To optimize efficiency, match target labels directly onto food bag delivery receipts prior to final packaging seals.")
