import streamlit as st
import plotly.express as px
import pandas as pd

# Streamlit page config
st.set_page_config(page_title="ESG Dashboard", layout="wide")
st.title("Environmental & Financial Insights Dashboard")

# Load data
df = pd.read_csv('dataset.csv')

# 1. Bar chart: Number of companies per Industry and Country
industry_counts = df.groupby(['Industry', 'Country']).size().reset_index(name='Company Count')
fig_bar = px.bar(
    industry_counts,
    x='Industry', y='Company Count', color='Country', barmode='group',
    title='Number of Companies per Industry and Country', template='plotly_white'
)
fig_bar.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_bar, use_container_width=True)

# 2. Box plots: CO2 Emissions by Industry within each Segment
segment_order = ['Large Corporate', 'Medium Corporate', 'Small Corporate']
df['Segment'] = pd.Categorical(df['Segment'], categories=segment_order, ordered=True)
for segment in segment_order:
    st.subheader(f'CO₂ Emissions by Industry – Segment: {segment}')
    df_seg = df[df['Segment'] == segment]
    industry_order = (
        df_seg.groupby('Industry')['CO2 (tons)'].median().sort_values(ascending=False).index.tolist()
    )
    fig_co2 = px.box(
        df_seg,
        x='Industry', y='CO2 (tons)', color='Industry',
        category_orders={'Industry': industry_order},
        title=f'{segment}', labels={'CO2 (tons)': 'CO₂ (tons)'},
        template='plotly_white'
    )
    fig_co2.update_layout(xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig_co2, use_container_width=True)

# 3. Scatter plot: CO2 vs Financed Amount by Industry
st.subheader('CO₂ vs Financed Amount by Industry')
fig_scatter = px.scatter(
    df,
    x='Financed Amount', y='CO2 (tons)', color='Industry',
    hover_data=['Country', 'Segment'], title='',
    labels={'Financed Amount':'Financed Amount (USD)', 'CO2 (tons)':'CO₂ (tons)'},
    template='plotly_white'
)
st.plotly_chart(fig_scatter, use_container_width=True)

# 4. Heatmap: Environmental Risk Averages by Country
st.subheader('Environmental Risk Heatmap')
risk_avg = df.groupby('Country')[['Flood Risk', 'Water Stress', 'Drought Risk']].mean().round(2).reset_index()
risk_matrix = risk_avg.set_index('Country')
fig_risk = px.imshow(
    risk_matrix,
    text_auto=True,
    color_continuous_scale='YlGnBu',
    labels=dict(color='Avg Risk Score'),
    x=risk_matrix.columns, y=risk_matrix.index,
    title='Environmental Risk Averages by Country'
)
st.plotly_chart(fig_risk, use_container_width=True)

# 5. Scatter plot: Water Usage vs Water Stress by Country
st.subheader('Water Usage vs Water Stress by Country')
fig_water = px.scatter(
    df,
    x='Water Stress', y='Water Usage (thousand m3)', color='Country',
    hover_data=['Industry', 'Segment', 'Financed Amount'],
    labels={'Water Stress':'Water Stress Score', 'Water Usage (thousand m3)':'Water Usage (000 m³)'},
    template='plotly_white'
)
fig_water.update_traces(marker=dict(size=8, opacity=0.6))
st.plotly_chart(fig_water, use_container_width=True)
