
import pandas as pd
import plotly.express as px
import streamlit as st

# Title and subtitle
st.title("French Spirit - Laduree Dashboard")
st.markdown("### Powered by Taqtics")

# Load the data
file_path = "Performance_Data_For_Lovable.csv"
df = pd.read_csv(file_path)
df['Result'] = pd.to_numeric(df['Result'], errors='coerce')

# Sidebar filters
st.sidebar.header("Global Filters")
countries = st.sidebar.multiselect("Select Country", options=df['Country'].unique(), default=df['Country'].unique())
stores = st.sidebar.multiselect("Select Store", options=df['Store'].unique(), default=df['Store'].unique())
entity_ids = st.sidebar.multiselect("Select Entity Id", options=df['Entity Id'].unique(), default=df['Entity Id'].unique())
statuses = st.sidebar.multiselect("Select Audit Status", options=df['Audit Status'].unique(), default=df['Audit Status'].unique())

# Apply global filters
filtered_df = df[
    (df['Country'].isin(countries)) &
    (df['Store'].isin(stores)) &
    (df['Entity Id'].isin(entity_ids)) &
    (df['Audit Status'].isin(statuses))
]


# ------------------ Interactive Overall Bell Curve with Audit Status ------------------
st.subheader("📊 Interactive Overall Bell Curve with Audit Status")
st.markdown("This chart shows employee distribution by performance score, color-coded by Audit Status.")

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


# ------------------ Cumulative Responses Chart ------------------
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

# ------------------ Country-wise Charts ------------------
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

# ------------------ Store-wise Charts ------------------
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


# Country-wise Drilldown
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

# Store-wise Dropdown View
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



# ------------------ Iceberg Chart (Cumulative + Drilldowns) ------------------
st.subheader("🧊 Iceberg Chart – Audit Status Breakdown")

# Cumulative Iceberg
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
    yaxis_title="",
    height=350,
    legend_title="Audit Status"
)
st.plotly_chart(fig_iceberg)

# Country Drilldown
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

# Store Drilldown
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
