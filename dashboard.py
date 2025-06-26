
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------- Branding Layout ----------
from PIL import Image
col1, col2 = st.columns([1, 1])
with col1:
    st.image("taqtics_logo.png", width=180)
with col2:
    st.image("laduree_logo.png", width=140)

st.markdown("""<h2 style='text-align: center; color: #6A5ACD;'>French Spirit - Laduree Dashboard</h2>
<p style='text-align: center; color: gray;'>Powered by Taqtics</p>""", unsafe_allow_html=True)

# ---------- Load Data ----------
file_path = "Performance_Data_For_Lovable.csv"
df = pd.read_csv(file_path)
df['Result'] = pd.to_numeric(df['Result'], errors='coerce')

# ---------- Sidebar Filters ----------
st.sidebar.header("Global Filters")
countries = st.sidebar.multiselect("Select Country", options=df['Country'].unique(), default=df['Country'].unique())
stores = st.sidebar.multiselect("Select Store", options=df['Store'].unique(), default=df['Store'].unique())
entity_ids = st.sidebar.multiselect("Select Entity Id", options=df['Entity Id'].unique(), default=df['Entity Id'].unique())
statuses = st.sidebar.multiselect("Select Audit Status", options=df['Audit Status'].unique(), default=df['Audit Status'].unique())

filtered_df = df[
    (df['Country'].isin(countries)) &
    (df['Store'].isin(stores)) &
    (df['Entity Id'].isin(entity_ids)) &
    (df['Audit Status'].isin(statuses))
]

# ---------- Overall Bell Curve ----------
st.subheader("Overall Bell Curve of Performance Scores")
fig_overall = px.histogram(
    filtered_df,
    x="Result",
    nbins=20,
    color="Country",
    hover_data=["Store", "Entity Id", "Audit Status", "Employee Name"],
    labels={"Result": "Performance Score"}
)
fig_overall.update_layout(bargap=0.1)
st.plotly_chart(fig_overall)

# ---------- Country Drilldown ----------
st.subheader("Country-wise Bell Curve and Drilldown")
selected_country = st.selectbox("Select Country for Drilldown", sorted(df['Country'].dropna().unique()))
country_df = df[df['Country'] == selected_country]

fig_country = px.histogram(
    country_df,
    x="Result",
    nbins=20,
    color="Store",
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

# ---------- Store Drilldown ----------
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
