import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/visualize-zh")

# === Load dataset ===
df = pd.read_csv("TCO.csv")

# === Layout ===
layout = html.Div(
    style={
        "backgroundImage": "url('/assets/pic2.png')",
        "backgroundSize": "cover",
        "backgroundPosition": "center",
        "minHeight": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "padding": "20px",
    },
    children=[
        # Header Section (Only for Home Page)
        html.Div(
            className="header",
            style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "width": "100%",
                "height": "70px",
                "backgroundColor": "white",
                "borderBottom": "1px solid #eee",
                "padding": "0 30px",
            },
            children=[
                # Left: Home button
                html.A("TCO 材料分类", href="/home-zh", className="home-btn"),

                # Middle: Language toggle
                html.Div(
                    style={"display": "flex", "alignItems": "center", "gap": "10px"},
                    children=[
                        dbc.Button("🇺🇸 English", href="/visualize", color="light", className="mx-1"),
                        dbc.Button("🇨🇳 中文", href="/visualize-zh", color="primary", className="mx-1"),
                    ],
                ),

                # Right: Exit button
                html.A(
                    href="/home-zh",  # <-- Change here
                    className="exit-btn",
                    children=html.Img(
                        src="/assets/exit.svg",
                        alt="退出",
                        className="exit-icon",
                    ),
                ),
            ],
        ),

        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "40px",
                "borderRadius": "15px",
                "boxShadow": "0px 4px 15px rgba(0, 0, 0, 0.2)",
                "width": "850px",
                "maxWidth": "95%",
                "fontFamily": "'Poppins', 'Segoe UI', sans-serif",
            },
            children=[
                html.H2(
                    "📈 透射率图表",
                    style={
                        "textAlign": "center",
                        "marginBottom": "25px",
                        "fontWeight": "600",
                        "color": "#1F2937",
                    },
                ),

                # === Material dropdown with grey background label ===
                dbc.InputGroup([
                    dbc.InputGroupText("🧩 材料"),
                    dcc.Dropdown(
                        id="material-dropdown",
                        options=[{"label": m, "value": m} for m in df["Material"].unique()],
                        placeholder="请选择一种材料",
                        style={"width": "100%"},
                    ),
                ], className="mb-4"),

                html.Label(
                    "📏 选择波长范围 (nm)",
                    style={"fontWeight": "600", "fontSize": "16px"},
                ),
                dcc.RangeSlider(
                    id="range-slider",
                    min=300,
                    max=800,
                    step=1,
                    value=[400, 700],
                    marks={300: '300', 800: '800'},
                    tooltip={"placement": "bottom", "always_visible": True},
                    allowCross=False,
                    className="custom-range-slider",
                ),

                dbc.Button(
                    "🎨 显示图表",
                    id="show-graph-btn",
                    color="primary",
                    className="mt-4 w-100",
                    style={"fontWeight": "600"},
                ),

                html.Div(id="transmission-graph-container-zh", className="mt-4"),
            ],
        )
    ]
)

# === Callback ===
@dash.callback(
    Output("transmission-graph-container-zh", "children"),
    Input("show-graph-btn", "n_clicks"),
    State("material-dropdown", "value"),
    State("range-slider", "value"),
    prevent_initial_call=True
)
def update_graph(n_clicks, material, range_values):
    if not material:
        return dbc.Alert("⚠️ 请在显示图表之前选择一种材料。", color="warning")

    subset = df[df["Material"] == material]
    filtered = subset[
        (subset["Wavelength"] >= range_values[0]) &
        (subset["Wavelength"] <= range_values[1])
    ]

    if filtered.empty:
        return dbc.Alert("所选范围内无可用数据。", color="danger")

    # --- Create smooth line with filled area ---
    fig = px.area(
        filtered,
        x="Wavelength",
        y="Transmission",
        title=f"透射率与波长关系图： {material} ({range_values[0]}–{range_values[1]} nm)",
        template="plotly_white",
    )

    # --- Aesthetic enhancements ---
    fig.update_traces(
        line=dict(color="#007BFF", width=3),
        fill="tozeroy",
        fillcolor="rgba(0, 123, 255, 0.15)"
    )

    fig.update_layout(
        title_x=0.5,
        title_font=dict(size=22, family="Poppins, Segoe UI, sans-serif", color="#1F2937"),
        xaxis_title="波长 (nm)",
        yaxis_title="透射率 (%)",
        xaxis=dict(
            title_font=dict(size=16, family="Poppins, Segoe UI, sans-serif"),
            tickfont=dict(size=12, family="Poppins, Segoe UI, sans-serif"),
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title_font=dict(size=16, family="Poppins, Segoe UI, sans-serif"),
            tickfont=dict(size=12, family="Poppins, Segoe UI, sans-serif"),
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=50, r=50, t=70, b=60),
        height=500,
        plot_bgcolor="white",   # white top area
        paper_bgcolor="white",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Poppins, Segoe UI, sans-serif"
        ),
        showlegend=False,
        transition_duration=600,
    )

    return dcc.Graph(
        figure=fig,
        style={
            "borderRadius": "10px",
            "boxShadow": "0px 4px 15px rgba(0, 0, 0, 0.1)",
            "backgroundColor": "white",
        },
        config={"displayModeBar": False}
    )
