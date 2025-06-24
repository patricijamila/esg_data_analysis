import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.io as pio

st.set_page_config(page_title="ESG Dashboard", layout="wide")
st.title("Environmental & Financial Insights")

df = pd.read_csv('dataset.csv')

fig = px.bar(
    industry_counts,
    x="Industry",
    y="Company Count",
    color="Country",
    barmode="group",
    title="Number of Companies per Industry and Country",
    template="plotly_white"
)
fig.update_layout(xaxis_tickangle=-45)
fig.show()


# Define your desired segment order
segment_order = ["Large Corporate", "Medium Corporate", "Small Corporate"]

# Ensure Segment column is treated as ordered categorical
df["Segment"] = pd.Categorical(df["Segment"], categories=segment_order, ordered=True)

# Loop through each segment in the specified order
for segment in segment_order:
    df_segment = df[df["Segment"] == segment]

    # Sort industries by median CO₂ for this segment
    industry_order = (
        df_segment.groupby("Industry")["CO2 (tons)"]
        .median()
        .sort_values(ascending=False)
        .index.tolist()
    )

    # Create box plot
    fig = px.box(
        df_segment,
        x="Industry",
        y="CO2 (tons)",
        color="Industry",
        title=f"CO₂ Emissions by Industry – Segment: {segment}",
        labels={"CO2 (tons)": "CO₂ (tons)"},
        category_orders={
            "Industry": industry_order
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False
    )

    fig.show()

# Create scatter plot
fig = px.scatter(
    df,
    x="Financed Amount",
    y="CO2 (tons)",
    color="Industry",           # Or use Segment
    hover_data=["Country", "Segment", "Industry"],
    title="CO₂ vs Financed Amount by Industry",
    labels={
        "Financed Amount": "Financed Amount",
        "CO2 (tons)": "CO₂ Emissions (tons)",
        "Water Usage (thousand m3)": "Water Usage (000 m³)"
    },
    size_max=25
)

fig.update_layout(
    template="plotly_white"
)

fig.show()

#Group by country and calculate average risk values
risk_avg = df.groupby("Country")[["Flood Risk", "Water Stress", "Drought Risk"]].mean().reset_index()

# Melt to long format for heatmap
risk_melted = risk_avg.melt(
    id_vars="Country",
    value_vars=["Flood Risk", "Water Stress", "Drought Risk"],
    var_name="Risk Type",
    value_name="Average Risk"
)

# Round average risk values for cleaner labels
risk_melted["Average Risk"] = risk_melted["Average Risk"].round(2)


fig = px.density_heatmap(
    risk_melted,
    x="Risk Type",
    y="Country",
    z="Average Risk",
    color_continuous_scale="YlGnBu",
    text_auto=True,
    title="Environmental Risk Averages by Country",
    labels={"Average Risk": "Avg Risk Score"},
    template="plotly_white"
)

fig.update_layout(
    height=600,
    coloraxis_colorbar=dict(title=None)  # Remove colorbar title
)

fig.show()

fig = px.scatter(
    df,
    x="Water Stress",
    y="Water Usage (thousand m3)",
    color="Country",
    hover_data=["Industry", "Segment", "Financed Amount"],
    title="💧 Water Usage vs. Water Stress by Country",
    labels={
        "Water Stress": "Water Stress Score",
        "Water Usage (thousand m3)": "Water Usage (thousand m³)"
    },
    template="plotly_white"
)

fig.update_traces(marker=dict(size=8, opacity=0.6))
fig.update_layout(height=600)
fig.show()