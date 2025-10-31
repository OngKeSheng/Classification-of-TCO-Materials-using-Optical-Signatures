# lookup.py
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path="/lookup")

# Load dataset
df = pd.read_csv("TCO.csv")

layout = html.Div(
    style={
        "backgroundImage": "url('/assets/pic2.png')",
        "backgroundSize": "cover",
        "backgroundPosition": "center",
        "height": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
    },
    children=[
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "40px",
                "borderRadius": "15px",
                "boxShadow": "0px 4px 15px rgba(0, 0, 0, 0.2)",
                "width": "800px",
                "maxWidth": "90%",
            },
            children=[
                html.H2("📖 Lookup TCO Material Data", style={"textAlign": "center", "marginBottom": "20px"}),

                # Dropdown Material
                dbc.InputGroup([
                    dbc.InputGroupText("🧩 Material"),
                    dcc.Dropdown(
                        id="material-dropdown",
                        options=[{"label": m, "value": m} for m in df["Material"].unique()],
                        placeholder="Choose a material",
                        style={"width": "100%"}
                    ),
                ], className="mb-3"),

                # Wavelength Input
                dbc.InputGroup([
                    dbc.InputGroupText("📏 Wavelength (nm)"),
                    dbc.Input(id="wavelength-input", type="number", min=300, max=800, step="any",
                              placeholder="Enter wavelength"),
                    dbc.InputGroupText("300–800"),
                ], className="mb-3"),

                # Search Button
                dbc.Button("🔎 Search", id="search-btn", color="primary", className="mt-3 w-100"),

                # Output
                html.Div(id="lookup-output", className="mt-4", style={"textAlign": "center"}),
            ]
        )
    ]
)

# Callback
@dash.callback(
    Output("lookup-output", "children"),
    Input("search-btn", "n_clicks"),
    State("material-dropdown", "value"),
    State("wavelength-input", "value"),
)
def lookup_data(n_clicks, material, wavelength):
    if not n_clicks:
        return ""
    if not material or wavelength is None:
        return dbc.Alert("⚠️ Please select a material and enter a wavelength.", color="warning")

    # Filter dataset
    result = df[(df["Material"] == material) & (df["Wavelength"] == wavelength)]

    if result.empty:
        return dbc.Alert(f"No data found for {material} at {wavelength} nm.", color="danger")

    row = result.iloc[0]

    # Show results inside green alert (like predict.py)
    return dbc.Alert(
        html.Div([
            html.H5(f"Material Properties for {material} at {wavelength} nm", className="mb-3"),
            html.Div(f"Absorbance: {row['AbsorptionRate']:.4f}", className="mb-2"),
            html.Div(f"Transmission: {row['Transmission']:.4f}", className="mb-2"),
            html.Div(f"Optical Density: {row['OpticalDensity']:.4f}", className="mb-2"),
        ]),
        color="success",
        style={"textAlign": "left"}
    )
