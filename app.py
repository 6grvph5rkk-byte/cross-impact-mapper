import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Cross-Impact Mapping – pi-studio / MA Designing Education",
    layout="wide",
)

# --------------------------------------------------------------------
# Header & branding
# --------------------------------------------------------------------
st.title("Cross-Impact Mapping Tool – pi-studio / MA Designing Education")

st.markdown(
    """
This is a tool for organisations to explore **factors of influence** and use it in
relationship to **future prospecting**, and in relationship to the  
**MA in Designing Education at Goldsmiths, University of London**.

Cross-impact analysis was originally developed by **Gordon & Helmer (1966)** in futures studies  
and is developed here as a way to explore **prospecting futures** in creative,
educational and organisational contexts.
"""
)

st.markdown("---")

# --------------------------------------------------------------------
# Sidebar settings
# --------------------------------------------------------------------
st.sidebar.header("Settings")

x_centre = st.sidebar.number_input(
    "X-axis centre (Dependence)", value=0.0, step=0.5
)
y_centre = st.sidebar.number_input(
    "Y-axis centre (Influence)", value=0.0, step=0.5
)

st.sidebar.markdown(
    """
Use negative values to indicate *low* and positive values for *high*  
(e.g. from **-10 to +10**).
"""
)

# --------------------------------------------------------------------
# Preset scenarios
# --------------------------------------------------------------------
st.subheader("1. Choose or create your scenario")

st.markdown(
    """
Use the selector below to load an example, or start from a blank template.  
You can then **edit, add or delete** factors as needed.
"""
)

blank_data = pd.DataFrame(
    {
        "Factor": [],
        "Dependence": [],
        "Influence": [],
    }
)

uk_creative = pd.DataFrame(
    {
        "Factor": [
            "AI-everything & automation",
            "Public funding & cultural policy",
            "Cost of living & inflation",
            "Digital platforms & intermediaries",
            "Skills pipeline & training access",
            "Ticket pricing & audience affordability",
        ],
        "Dependence": [-5, 8, 9, 4, 7, 7],
        "Influence": [13, 11, 13, 10, 9, -2],
    }
)

scotland_creative = pd.DataFrame(
    {
        "Factor": [
            "AI-everything & automation (Scotland)",
            "Creative Scotland & local authority funding",
            "Brexit, trade & touring",
            "Cultural values & changing audiences",
            "Local venue & studio viability",
            "Freelance income & precarity",
        ],
        "Dependence": [-5, 8, 10, -4, 7, 9],
        "Influence": [13, 11, 9, 8, -3, -4],
    }
)

scenario_options = {
    "Blank / start from scratch": blank_data,
    "UK Creative Industries": uk_creative,
    "Scottish Creative Industries": scotland_creative,
}

scenario_name = st.selectbox(
    "Load example scenario",
    list(scenario_options.keys()),
    index=1,  # default to UK Creative Industries
)

base_data = scenario_options[scenario_name].copy()

# --------------------------------------------------------------------
# Factor editor
# --------------------------------------------------------------------
st.subheader("2. Edit your factors and scores")

st.markdown(
    """
- **Factor** = name of the driver or element in the system  
- **Dependence** = X-axis score (how much it is influenced by others)  
- **Influence** = Y-axis score (how much it influences others)  

You can **double-click** cells to edit them, and use the bottom row to add more factors.
"""
)

data = st.data_editor(
    base_data,
    num_rows="dynamic",
    use_container_width=True,
    key=f"factor_table_{scenario_name.replace(' ', '_')}",
)

# Ensure numeric types
for col in ["Dependence", "Influence"]:
    data[col] = pd.to_numeric(data[col], errors="coerce")

data = data.dropna(subset=["Factor", "Dependence", "Influence"])

# --------------------------------------------------------------------
# Quadrant classification
# --------------------------------------------------------------------
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
    data["Quadrant"] = data.apply(
        classify_quadrant, axis=1, args=(x_centre, y_centre)
    )
else:
    data["Quadrant"] = []

st.subheader("3. Calculated quadrants")

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

# --------------------------------------------------------------------
# Plot
# --------------------------------------------------------------------
st.subheader("4. Cross-Impact Map")

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

    fig.update_traces(textposition="top center")
    fig.update_layout(
        xaxis_title="Dependence (influenced by others)",
        yaxis_title="Influence (influences others)",
        legend_title="Quadrant",
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------------------
# Reflection
# --------------------------------------------------------------------
st.subheader("5. Reflection")

reflection = st.text_area(
    "What does this map tell you?",
    placeholder=(
        "Write a short reflection on patterns, clusters, tensions or surprises in this map.\n"
        "For example: Which factors are emerging as critical levers? What feels fragile or at risk?"
    ),
    height=150,
)

# --------------------------------------------------------------------
# Export
# --------------------------------------------------------------------
st.subheader("6. Export data and notes")

if data.empty and not reflection.strip():
    st.info("Add some factors or a reflection to enable downloads.")
else:
    # Make sure scenario name is stored
    export_data = data.copy()
    export_data.insert(0, "Scenario", scenario_name)

    csv_bytes = export_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download data as pi-studio CSV",
        data=csv_bytes,
        file_name="pi-studio_cross-impact-data.csv",
        mime="text/csv",
    )

    txt_content = (
        f"Scenario: {scenario_name}\n\n"
        "Reflection:\n"
        f"{reflection.strip() or '(no reflection entered)'}\n\n"
        "Data (CSV format):\n"
        f"{export_data.to_csv(index=False)}"
    )

    st.download_button(
        "Download reflection + data (.txt)",
        data=txt_content,
        file_name="pi-studio_cross-impact-reflection.txt",
        mime="text/plain",
    )

# --------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "*Built by **pi-studio** with **Eudora** and **Prof Mike Waller**.*"
)
