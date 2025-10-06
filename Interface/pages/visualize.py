import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/visualize", name="Visualize")

# === Load real CSV data ===
df = pd.read_csv("TCO.csv")

# Ensure numeric sorting (important for smooth lines)
df = df.sort_values(by="Wavelength")

# Get unique materials
materials = df["Material"].unique()

# === Layout ===
layout = dbc.Container(
    [
        html.H2("Transmission Visualization", className="text-center mt-4 mb-4"),

        dbc.Row([
            dbc.Col([
                html.Label("Select Material:", style={"font-weight": "bold"}),
                dcc.Dropdown(
                    id="material-dropdown",
                    options=[{"label": m, "value": m} for m in materials],
                    placeholder="Select a material",
                    style={"width": "100%"}
                ),
            ], width=4),
        ], justify="center"),

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.Label("Select Wavelength Range (nm):", style={"font-weight": "bold"}),
                dcc.RangeSlider(
                    id="range-slider",
                    min=300,
                    max=800,
                    step=1,
                    value=[400, 700],
                    marks={i: str(i) for i in range(300, 801, 100)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], width=8),
        ], justify="center"),

        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Button("Show Graph", id="show-graph-btn", color="primary", size="lg"),
                width="auto"
            )
        ], justify="center"),

        html.Br(),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id="transmission-graph"),
                width=10
            )
        ], justify="center"),
    ],
    fluid=True,
)

# === Callback ===
@dash.callback(
    Output("transmission-graph", "figure"),
    Input("show-graph-btn", "n_clicks"),
    State("material-dropdown", "value"),
    State("range-slider", "value"),
    prevent_initial_call=True
)
def update_graph(n_clicks, material, range_values):
    if not material:
        return px.line(title="Please select a material.")

    # Filter data for selected material
    subset = df[df["Material"] == material]

    # Apply wavelength range
    filtered = subset[
        (subset["Wavelength"] >= range_values[0]) &
        (subset["Wavelength"] <= range_values[1])
    ]

    # Create smooth line graph
    fig = px.line(
        filtered,
        x="Wavelength",
        y="Transmission",
        title=f"Transmission vs Wavelength for {material} ({range_values[0]}–{range_values[1]} nm)",
        template="plotly_white",
    )

    # Style adjustments
    fig.update_traces(line=dict(color="#007BFF", width=3))
    fig.update_layout(
        title_x=0.5,
        title_font_size=20,
        xaxis_title="Wavelength (nm)",
        yaxis_title="Transmission (%)",
        margin=dict(l=60, r=60, t=60, b=60)
    )

    return fig
