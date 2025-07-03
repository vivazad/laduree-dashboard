
# ------------------ Google SSO (Optional Advanced) ------------------
# To implement Google Sign-In, you would need:
# - A Streamlit-compatible auth handler (e.g., streamlit-authenticator, custom OAuth2)
# - Setup Google OAuth in Google Cloud Console
# - Deploy to a secure environment (Streamlit sharing doesn’t support secure SSO directly)
# Consider using Streamlit Community + Firebase/Auth0 for full auth control

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

# Load the data from CSV (fixed for Streamlit deployment)
df = pd.read_csv("Performance_Data_For_Lovable.csv")
df['Result'] = pd.to_numeric(df['Result'], errors='coerce')

# =========================================
# 📊 ANALYTICS SECTION (Bell Curves, Trends)
# =========================================

st.title("French Spirit - Laduree Dashboard")
st.markdown("### Powered by Taqtics")

# Sidebar filters
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

# Interactive Overall Bell Curve with Audit Status
st.subheader("📊 Interactive Overall Bell Curve with Audit Status")
fig_audit = px.histogram(
    df,
    x="Result",
    nbins=20,
    color="Audit Status",
    hover_data=["Employee Name", "Store", "Entity Id", "Country"],
    labels={"Result": "Performance Score"},
    title="Overall Distribution by Audit Status"
)
fig_audit.update_layout(bargap=0.1)
st.plotly_chart(fig_audit)

# Cumulative Responses Chart
st.subheader("📈 Cumulative Response Distribution")
cumulative_df = df.sort_values('Result')
cumulative_df['Cumulative Count'] = range(1, len(cumulative_df) + 1)
fig_cum = px.line(
    cumulative_df,
    x='Result',
    y='Cumulative Count',
    title='Cumulative Distribution of Performance Scores',
    labels={'Result': 'Performance Score', 'Cumulative Count': 'Number of Employees'},
    markers=True
)
st.plotly_chart(fig_cum)

# Country-wise Bell Curves
st.subheader("🌍 Country-wise Performance Bell Curves")
for country in sorted(df['Country'].dropna().unique()):
    st.markdown(f"#### {country}")
    country_df = df[df['Country'] == country]
    fig_country = px.histogram(
        country_df,
        x="Result",
        nbins=20,
        color="Audit Status",
        hover_data=["Store", "Entity Id", "Employee Name"],
        title=f"{country} - Performance Distribution",
        labels={"Result": "Performance Score"}
    )
    fig_country.update_layout(bargap=0.1)
    st.plotly_chart(fig_country)

# Store-wise Bell Curves
st.subheader("🏬 Store-wise Performance Bell Curves")
for store in sorted(df['Store'].dropna().unique()):
    st.markdown(f"#### {store}")
    store_df = df[df['Store'] == store]
    fig_store = px.histogram(
        store_df,
        x="Result",
        nbins=20,
        color="Audit Status",
        hover_data=["Country", "Entity Id", "Employee Name"],
        title=f"{store} - Performance Distribution",
        labels={"Result": "Performance Score"}
    )
    fig_store.update_layout(bargap=0.1)
    st.plotly_chart(fig_store)

# =========================================
# 🧊 ICEBERG CHARTS SECTION
# =========================================

# Iceberg Chart – Cumulative
st.subheader("🧊 Iceberg Chart – Cumulative Audit Status")
audit_order = ['Below Expectation', 'Needs Improvement', 'Meets Expectation', 'Outstanding']
df['Audit Status'] = pd.Categorical(df['Audit Status'], categories=audit_order, ordered=True)
iceberg_data = df['Audit Status'].value_counts().reindex(audit_order).fillna(0)

colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']
fig_iceberg = go.Figure()
for i, status in enumerate(audit_order):
    fig_iceberg.add_trace(go.Bar(
        y=["Cumulative"],
        x=[iceberg_data[status]],
        name=status,
        orientation='h',
        marker=dict(color=colors[i])
    ))

fig_iceberg.update_layout(
    barmode='stack',
    title="Cumulative Audit Status Distribution (Iceberg Chart)",
    xaxis_title="Number of Employees",
    height=350,
    legend_title="Audit Status"
)
st.plotly_chart(fig_iceberg)

# Country-wise Icebergs
st.subheader("🌍 Iceberg by Country")
for country in sorted(df['Country'].dropna().unique()):
    st.markdown(f"**{country}**")
    country_df = df[df['Country'] == country]
    country_data = country_df['Audit Status'].value_counts().reindex(audit_order).fillna(0)

    fig_country = go.Figure()
    for i, status in enumerate(audit_order):
        fig_country.add_trace(go.Bar(
            y=[country],
            x=[country_data[status]],
            name=status,
            orientation='h',
            marker=dict(color=colors[i])
        ))
    fig_country.update_layout(
        barmode='stack',
        height=300,
        margin=dict(t=30),
        showlegend=False
    )
    st.plotly_chart(fig_country)

# Store-wise Icebergs
st.subheader("🏬 Iceberg by Store")
for store in sorted(df['Store'].dropna().unique()):
    st.markdown(f"**{store}**")
    store_df = df[df['Store'] == store]
    store_data = store_df['Audit Status'].value_counts().reindex(audit_order).fillna(0)

    fig_store = go.Figure()
    for i, status in enumerate(audit_order):
        fig_store.add_trace(go.Bar(
            y=[store],
            x=[store_data[status]],
            name=status,
            orientation='h',
            marker=dict(color=colors[i])
        ))
    fig_store.update_layout(
        barmode='stack',
        height=300,
        margin=dict(t=30),
        showlegend=False
    )
    st.plotly_chart(fig_store)



# ------------------ Stacked Area Chart (Replaces Iceberg) ------------------
st.subheader("🧊 Stacked Area Chart – Audit Status Distribution")

# Reapply filters
area_countries = st.multiselect("🌍 Filter by Country", options=df['Country'].unique(), default=df['Country'].unique())
area_stores = st.multiselect("🏬 Filter by Store", options=df['Store'].unique(), default=df['Store'].unique())
area_statuses = st.multiselect("🎯 Filter by Audit Status", options=df['Audit Status'].unique(), default=df['Audit Status'].unique())

area_df = df[
    (df['Country'].isin(area_countries)) &
    (df['Store'].isin(area_stores)) &
    (df['Audit Status'].isin(area_statuses))
]

# Count by status and performance bins
area_df['Score Bin'] = pd.cut(area_df['Result'], bins=20)
grouped = area_df.groupby(['Score Bin', 'Audit Status']).size().reset_index(name='Count')
grouped['Score Mid'] = grouped['Score Bin'].apply(lambda x: x.mid)

# Pivot to wide format for stacked area
pivot = grouped.pivot(index='Score Mid', columns='Audit Status', values='Count').fillna(0)
pivot = pivot[['Below Expectation', 'Needs Improvement', 'Meets Expectation', 'Outstanding']].fillna(0)

fig_area = go.Figure()
colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']
for i, status in enumerate(pivot.columns):
    fig_area.add_trace(go.Scatter(
        x=pivot.index,
        y=pivot[status],
        stackgroup='one',
        name=status,
        line=dict(width=0.5),
        mode='lines',
        fillcolor=colors[i]
    ))

fig_area.update_layout(
    title="Stacked Area Chart – Performance by Audit Status",
    xaxis_title="Performance Score",
    yaxis_title="Number of Employees",
    legend_title="Audit Status"
)
st.plotly_chart(fig_area)
