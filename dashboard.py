
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Load data
file_path = "Performance_Data_For_Lovable.csv"
df = pd.read_csv(file_path)
df['Result'] = pd.to_numeric(df['Result'], errors='coerce')

# Sidebar filters
st.sidebar.header("Global Filters")
countries = st.sidebar.multiselect("Select Country", options=df['Country'].unique(), default=df['Country'].unique())
stores = st.sidebar.multiselect("Select Store", options=df['Store'].unique(), default=df['Store'].unique())
entity_ids = st.sidebar.multiselect("Select Entity Id", options=df['Entity Id'].unique(), default=df['Entity Id'].unique())
statuses = st.sidebar.multiselect("Select Audit Status", options=df['Audit Status'].unique(), default=df['Audit Status'].unique())

# Apply filters
df = df[
    (df['Country'].isin(countries)) &
    (df['Store'].isin(stores)) &
    (df['Entity Id'].isin(entity_ids)) &
    (df['Audit Status'].isin(statuses))
]

# Pastel color map
color_discrete_map = {
    "Below Expectation": "#FF9999",
    "Needs Improvement": "#ADD8E6",
    "Meets Expectation": "#90EE90",
    "Outstanding": "#77DD77"
}

# --------- Main Audit Status Interactive Chart ---------
st.subheader("📊 Interactive Overall Bell Curve with Audit Status")
fig_audit = px.histogram(
    df,
    x="Result",
    nbins=20,
    color="Audit Status",
    color_discrete_map=color_discrete_map,
    hover_data=["Employee Name", "Store", "Entity Id", "Country"],
    labels={"Result": "Performance Score"},
    title="Overall Distribution by Audit Status"
)
fig_audit.update_layout(bargap=0.1)
st.plotly_chart(fig_audit)

# --------- Cumulative Line Chart ---------
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

# --------- Country Bell Curves ---------
st.subheader("🌍 Country-wise Performance Bell Curves")
for country in sorted(df['Country'].dropna().unique()):
    st.markdown(f"#### {country}")
    country_df = df[df['Country'] == country]
    fig_country = px.histogram(
        country_df,
        x="Result",
        nbins=20,
        color="Audit Status",
        color_discrete_map=color_discrete_map,
        hover_data=["Store", "Entity Id", "Employee Name"],
        title=f"{country} - Performance Distribution",
        labels={"Result": "Performance Score"}
    )
    fig_country.update_layout(bargap=0.1)
    st.plotly_chart(fig_country)

# --------- Store Bell Curves ---------
st.subheader("🏬 Store-wise Performance Bell Curves")
for store in sorted(df['Store'].dropna().unique()):
    st.markdown(f"#### {store}")
    store_df = df[df['Store'] == store]
    fig_store = px.histogram(
        store_df,
        x="Result",
        nbins=20,
        color="Audit Status",
        color_discrete_map=color_discrete_map,
        hover_data=["Country", "Entity Id", "Employee Name"],
        title=f"{store} - Performance Distribution",
        labels={"Result": "Performance Score"}
    )
    fig_store.update_layout(bargap=0.1)
    st.plotly_chart(fig_store)

# --------- Stacked Area Chart: Overall ---------
st.subheader("📊 Cumulative Stacked Area Chart by Audit Status")
cumulative_area_df = df.copy()
cumulative_area_df['Result Bin'] = pd.cut(cumulative_area_df['Result'], bins=20)

area_data = cumulative_area_df.groupby(['Result Bin', 'Audit Status']).size().reset_index(name='Count')
area_pivot = area_data.pivot(index='Result Bin', columns='Audit Status', values='Count').fillna(0)
area_pivot = area_pivot.cumsum()

fig_area = go.Figure()
for status in area_pivot.columns:
    fig_area.add_trace(go.Scatter(
        x=area_pivot.index.astype(str),
        y=area_pivot[status],
        stackgroup='one',
        name=status,
        mode='lines',
        line=dict(color=color_discrete_map.get(status))
    ))
fig_area.update_layout(
    title='Cumulative Stacked Area Chart by Audit Status',
    xaxis_title='Performance Score Ranges',
    yaxis_title='Cumulative Responses',
    hovermode='x unified'
)
st.plotly_chart(fig_area)

# --------- Country-wise Stacked Area Chart ---------
st.subheader("🌍 Stacked Area Chart by Country")
for country in sorted(df['Country'].dropna().unique()):
    st.markdown(f"#### {country}")
    country_df = df[df['Country'] == country]
    if not country_df.empty:
        country_df['Result Bin'] = pd.cut(country_df['Result'], bins=20)
        area_country = country_df.groupby(['Result Bin', 'Audit Status']).size().reset_index(name='Count')
        area_pivot_country = area_country.pivot(index='Result Bin', columns='Audit Status', values='Count').fillna(0)
        area_pivot_country = area_pivot_country.cumsum()

        fig_country_area = go.Figure()
        for status in area_pivot_country.columns:
            fig_country_area.add_trace(go.Scatter(
                x=area_pivot_country.index.astype(str),
                y=area_pivot_country[status],
                stackgroup='one',
                name=status,
                mode='lines',
                line=dict(color=color_discrete_map.get(status))
            ))
        fig_country_area.update_layout(
            title=f'Cumulative Audit Status by Score Range in {country}',
            xaxis_title='Performance Score Ranges',
            yaxis_title='Cumulative Responses',
            hovermode='x unified'
        )
        st.plotly_chart(fig_country_area)

# --------- Store-wise Stacked Area Chart ---------
st.subheader("🏬 Stacked Area Chart by Store")
for store in sorted(df['Store'].dropna().unique()):
    st.markdown(f"#### {store}")
    store_df = df[df['Store'] == store]
    if not store_df.empty:
        store_df['Result Bin'] = pd.cut(store_df['Result'], bins=20)
        area_store = store_df.groupby(['Result Bin', 'Audit Status']).size().reset_index(name='Count')
        area_pivot_store = area_store.pivot(index='Result Bin', columns='Audit Status', values='Count').fillna(0)
        area_pivot_store = area_pivot_store.cumsum()

        fig_store_area = go.Figure()
        for status in area_pivot_store.columns:
            fig_store_area.add_trace(go.Scatter(
                x=area_pivot_store.index.astype(str),
                y=area_pivot_store[status],
                stackgroup='one',
                name=status,
                mode='lines',
                line=dict(color=color_discrete_map.get(status))
            ))
        fig_store_area.update_layout(
            title=f'Cumulative Audit Status by Score Range in {store}',
            xaxis_title='Performance Score Ranges',
            yaxis_title='Cumulative Responses',
            hovermode='x unified'
        )
        st.plotly_chart(fig_store_area)
