
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import numpy as np
from scipy.stats import norm

# ------------------ Branding Header ------------------
col1, col2 = st.columns([1, 1])
with col1:
    st.image("taqtics_logo.png", width=180)
with col2:
    st.image("laduree_logo.png", width=140)

st.markdown("""<h2 style='text-align: center; color: #6A5ACD;'>French Spirit - Laduree Dashboard</h2>
<p style='text-align: center; color: gray;'>Powered by Taqtics</p>""", unsafe_allow_html=True)

# ------------------ Load Data ------------------
file_path = "Performance_Data_For_Lovable.csv"
df = pd.read_csv(file_path)
df['Result'] = pd.to_numeric(df['Result'], errors='coerce')

# ------------------ Sidebar Filters ------------------
st.sidebar.header("Filters")
countries = st.sidebar.multiselect("Select Country", options=df['Country'].unique(), default=df['Country'].unique())
stores = st.sidebar.multiselect("Select Store", options=df['Store'].unique(), default=df['Store'].unique())

filtered_df = df[
    (df['Country'].isin(countries)) &
    (df['Store'].isin(stores))
]

# ------------------ Audit Status Explanation ------------------

# ------------------ New Charts ------------------
st.subheader("📊 Store-wise Count by Audit Status")
fig_store_audit_status = px.bar(
    df.groupby(['Store', 'Audit Status']).size().reset_index(name='Count'),
    x="Store",
    y="Count",
    color="Audit Status",
    barmode="stack",
    title="Store-wise Count by Audit Status",
    labels={"Count": "Number of Employees"}
)
fig_store_audit_status.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_store_audit_status)

st.subheader("🏆 Top & Bottom Stores by Country")

# Calculate Top and Bottom Stores
store_avg = df.groupby(['Country', 'Store'])['Result'].mean().reset_index()
top_stores = store_avg.sort_values(['Country', 'Result'], ascending=[True, False]).groupby('Country').head(1)
bottom_stores = store_avg.sort_values(['Country', 'Result'], ascending=[True, True]).groupby('Country').head(1)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Top Store per Country**")
    st.dataframe(top_stores.rename(columns={'Result': 'Average Score'}).round(2))
with col2:
    st.markdown("**Bottom Store per Country**")
    st.dataframe(bottom_stores.rename(columns={'Result': 'Average Score'}).round(2))

st.markdown("""
### Audit Status Legend
- **Outstanding**: Exceptional performance (above 85%)
- **Good**: Solid performance (70%–85%)
- **Needs Improvement**: Below expectations (below 70%)
""")

# ------------------ Overall Bell Curve ------------------
st.subheader("Overall Bell Curve of Performance Scores")
fig_overall = px.histogram(
    filtered_df,
    x="Result",
    nbins=20,
    color="Audit Status",
    hover_data=["Store", "Entity Id", "Employee Name", "Country"],
    labels={"Result": "Performance Score"}
)
fig_overall.update_layout(bargap=0.1)
st.plotly_chart(fig_overall)

# ------------------ Country Drilldown ------------------
st.subheader("Country-wise Bell Curve and Drilldown")
selected_country = st.selectbox("Select Country for Drilldown", sorted(df['Country'].dropna().unique()))
country_df = df[df['Country'] == selected_country]

fig_country = px.histogram(
    country_df,
    x="Result",
    nbins=20,
    color="Audit Status",
    hover_data=["Entity Id", "Audit Status", "Employee Name"],
    labels={"Result": "Performance Score"},
    title=f"Performance Bell Curve for {selected_country}"
)
fig_country.update_layout(bargap=0.1)
st.plotly_chart(fig_country)

st.markdown(f"### Employees in {selected_country}")
st.dataframe(country_df[[
    "Employee Name", "Store", "Entity Id", "Audit Status", "Result"
]].sort_values(by="Result", ascending=False))

# ------------------ Store Drilldown ------------------
st.subheader("Store-wise Bell Curve")
selected_store = st.selectbox("Select Store", sorted(df['Store'].dropna().unique()))
store_df = df[df['Store'] == selected_store]

fig_store = px.histogram(
    store_df,
    x="Result",
    nbins=20,
    color="Audit Status",
    hover_data=["Country", "Entity Id", "Employee Name"],
    labels={"Result": "Performance Score"},
    title=f"Performance Bell Curve for {selected_store}"
)
fig_store.update_layout(bargap=0.1)
st.plotly_chart(fig_store)

# ------------------ Probability Distribution Chart ------------------
st.subheader("Probability Density of Performance Scores")

mean_score = filtered_df['Result'].mean()
std_dev = filtered_df['Result'].std()

x = np.linspace(filtered_df['Result'].min(), filtered_df['Result'].max(), 500)
pdf_y = norm.pdf(x, mean_score, std_dev)

fig_pdf = go.Figure()
fig_pdf.add_trace(go.Scatter(x=x, y=pdf_y, mode='lines', name='PDF'))
fig_pdf.add_vline(x=mean_score, line_dash='dash', line_color='green', annotation_text='Mean', annotation_position='top left')
fig_pdf.update_layout(title='Probability Density Function (PDF) of Performance Scores',
                      xaxis_title='Performance Score',
                      yaxis_title='Probability Density')
st.plotly_chart(fig_pdf)

st.markdown(f"""**Mean Score:** {mean_score:.2f}  
**Standard Deviation:** {std_dev:.2f}""")

# ------------------ New Graph: Country vs Score by Audit Status ------------------
st.subheader("Score Distribution by Country and Audit Status")
fig_country_status = px.strip(
    filtered_df,
    x="Country",
    y="Result",
    color="Audit Status",
    hover_data=["Employee Name", "Store", "Entity Id"],
    stripmode="overlay",
    labels={"Result": "Performance Score"},
    title="Performance Scores by Country Grouped by Audit Status"
)
fig_country_status.update_layout(yaxis=dict(range=[0, 100]))
st.plotly_chart(fig_country_status)
