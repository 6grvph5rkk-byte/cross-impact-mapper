import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cross-Impact Mapping Tool",
    layout="wide",
)

st.title("Cross-Impact Mapping / Analysis Tool")

st.markdown(
    """
This tool lets you create your own **cross-impact map**:

1. Add the **factors** or drivers in your system.  
2. Score each on:
   - **Dependence** (X-axis – how much it is influenced by others)
   - **Influence** (Y-axis – how much it influences others)  
3. The app automatically assigns **quadrants** and plots them.

You can use positive / negative scores (e.g. -10 to +10) or any numeric scale you like.
"""
)

# --- Sidebar controls ---------------------------------------------------------

st.sidebar.header("Settings")

# Centre thresholds for quadrants (usually 0)
x_centre = st.sidebar.number_input("X-axis centre (Dependence)", value=0.0, step=0.5)
y_centre = st.sidebar.number_input("Y-axis centre (Influence)", value=0.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.markdown("**Tip:** Use negative values for “low” and positive for “high”, "
                    "e.g. from -10 to +10.")

# --- Initial example data -----------------------------------------------------

default_data = pd.DataFrame(
    {
        "Factor": [
            "AI-everything & automation",
            "Public funding & policy",
            "Cost of living & inflation",
            "Ticket pricing & affordability",
        ],
        "Dependence": [-5, 8, 9, 7],
        "Influence": [13, 11, 13, -3],
    }
)

st.subheader("1. Edit your factors and scores")

st.markdown(
    """
Use the table below to **add, remove or edit rows**.  
- *Factor* = name of the driver  
- *Dependence* = X-axis score  
- *Influence* = Y-axis score  
"""
)

data = st.data_editor(
    default_data,
    num_rows="dynamic",
    use_container_width=True,
    key="factor_table",
)

# Ensure numeric types
for col in ["Dependence", "Influence"]:
    data[col] = pd.to_numeric(data[col], errors="coerce")

data = data.dropna(subset=["Factor", "Dependence", "Influence"])

# --- Assign quadrants ---------------------------------------------------------

def classify_quadrant(row, x0, y0):
    x = row["Dependence"]
    y = row["Influence"]
    if x < x0 and y > y0:
        return "Active"
    elif x >= x0 and y > y0:
        return "Critical"
    elif x >= x0 and y <= y0:
        return "Passive"
    else:
        return "Inactive"

if not data.empty:
    data["Quadrant"] = data.apply(classify_quadrant, axis=1, args=(x_centre, y_centre))
else:
    data["Quadrant"] = []

st.subheader("2. Calculated quadrants")

st.markdown(
    """
Quadrants are assigned using the centre values from the sidebar:

- **Active** – high Influence, low Dependence  
- **Critical** – high Influence, high Dependence  
- **Passive** – low Influence, high Dependence  
- **Inactive** – low Influence, low Dependence  
"""
)

st.dataframe(data, use_container_width=True)

# --- Plot ---------------------------------------------------------------------

st.subheader("3. Cross-Impact Map")

if data.empty:
    st.info("Add at least one factor with numeric scores to see the chart.")
else:
    fig = px.scatter(
        data,
        x="Dependence",
        y="Influence",
        color="Quadrant",
        text="Factor",
        color_discrete_map={
            "Active": "#1b9e77",
            "Critical": "#d95f02",
            "Passive": "#7570b3",
            "Inactive": "#e6ab02",
        },
        height=650,
    )

    # Add quadrant cross-hairs
    fig.add_vline(x=x_centre, line_width=1, line_color="black")
    fig.add_hline(y=y_centre, line_width=1, line_color="black")

    # Tidy labels
    fig.update_traces(textposition="top center")
    fig.update_layout(
        xaxis_title="Dependence (influenced by others)",
        yaxis_title="Influence (influences others)",
        legend_title="Quadrant",
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Download -----------------------------------------------------------------

st.subheader("4. Export your data")

csv = data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download factor table as CSV",
    data=csv,
    file_name="cross_impact_factors.csv",
    mime="text/csv",
)
