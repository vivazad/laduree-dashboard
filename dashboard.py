
import pandas as pd
import plotly.express as px
import streamlit as st

# Title and subtitle
st.title("French Spirit - Laduree Dashboard")
st.markdown("### Powered by Taqtics")

# Load the data
file_path = "Performance_Data_For_Lovable.csv"
df = pd.read_csv(file_path)

# Convert types if needed
df['Result'] = pd.to_numeric(df['Result'], errors='coerce')

# Sidebar filters
st.sidebar.header("Filter Options")
countries = st.sidebar.multiselect("Select Country", options=df['Country'].unique(), default=df['Country'].unique())
stores = st.sidebar.multiselect("Select Store", options=df['Store'].unique(), default=df['Store'].unique())
entity_ids = st.sidebar.multiselect("Select Entity Id", options=df['Entity Id'].unique(), default=df['Entity Id'].unique())
statuses = st.sidebar.multiselect("Select Audit Status", options=df['Audit Status'].unique(), default=df['Audit Status'].unique())

# Apply filters
filtered_df = df[
    (df['Country'].isin(countries)) &
    (df['Store'].isin(stores)) &
    (df['Entity Id'].isin(entity_ids)) &
    (df['Audit Status'].isin(statuses))
]

# Overall Bell Curve
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

# Country-wise Bell Curve
st.subheader("Country-wise Bell Curve")
fig_country = px.histogram(
    filtered_df,
    x="Result",
    nbins=20,
    facet_col="Country",
    color="Store",
    hover_data=["Entity Id", "Audit Status", "Employee Name"],
    labels={"Result": "Performance Score"}
)
fig_country.update_layout(bargap=0.1)
st.plotly_chart(fig_country)

# Store-wise Bell Curve
st.subheader("Store-wise Bell Curve")
fig_store = px.histogram(
    filtered_df,
    x="Result",
    nbins=20,
    facet_col="Store",
    color="Audit Status",
    hover_data=["Country", "Entity Id", "Employee Name"],
    labels={"Result": "Performance Score"}
)
fig_store.update_layout(bargap=0.1)
st.plotly_chart(fig_store)
