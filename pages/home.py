import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

dash.register_page(__name__, path="/")

layout = html.Div(
    style={
        "height": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "margin": "0",
        "padding": "0",
        "boxSizing": "border-box",  # Include padding and borders in size calculations
        "overflow": "hidden",
    },
    children=[
        # Header Section with Language Button
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
                html.A(
                    "TCO Classifier",
                    href="/",
                    className="home-btn",
                ),
                # Middle: Language toggle
                html.Div(
                    style={"display": "flex", "alignItems": "center", "gap": "10px"},
                    children=[
                        dbc.Button(
                            [html.Span("🇺🇸 English")],
                            href="/",
                            color="primary",
                            className="mx-1",
                            style={"fontWeight": "bold"}
                        ),
                        dbc.Button(
                            [html.Span("🇨🇳 中文")],
                            href="/home-zh",
                            color="light",
                            className="mx-1",
                            style={"fontWeight": "normal"}
                        )
                    ]
                ),
                # Right: (empty, or add exit button if needed)
                html.Div()  # Empty div to keep spacing
            ],
        ),

        # Content Section (70%)
        html.Div(
            style={
                "flex": "5.5",  # 70% of viewport height
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
            },
            children=[
                dbc.Row(
                    align="center",
                    className="h-100 d-flex align-items-center justify-content-center",
                    style={"margin": "0", "width": "100%"},
                    children=[
                        # ✅ Left side (Image)
                        dbc.Col(
                            html.Div(
                                html.Img(
                                    src="/assets/pic1.png",
                                    style={
                                        "max-width": "80%",
                                        "height": "auto",
                                        "display": "block",
                                        "margin": "0 auto"
                                    }
                                ),
                                style={"text-align": "center"}
                            ),
                            width=6
                        ),
                        # ✅ Right side (Text)
                        dbc.Col(
                            html.Div(
                                [
                                    html.H2(
                                        "AI TCO Material Classifier",
                                        style={
                                            "font-weight": "bold",
                                            "margin-bottom": "15px",
                                            "font-size": "32px"
                                        }
                                    ),
                                    html.P(
                                        """
                                        This project leverages the power of XGBoost to accurately classify Transparent Conductive Oxide (TCO) materials used in solar cells, including AZO, FTO, ITO, MZO, and ZnO.
                                        By analyzing four key optical properties Absorbance, Transmission, Optical Density, and Wavelength the model provides fast and reliable material predictions.
                                        Designed to support renewable energy research, this AI-driven tool reduces the need for time-consuming physical experiments and helps researchers and engineers accelerate innovation in solar cell technology.
                                        """,
                                        className="main-text",
                                        style={
                                            "font-size": "18px",
                                            "text-align": "justify",
                                            "max-width": "800px",
                                            "margin": "0 auto"
                                        }
                                    ),
                                dbc.Row(
                                    justify="center",
                                    className="mt-4",
                                    children=[
                                        # Column for Classify Material Button and Description
                                        dbc.Col(
                                            children=[
                                                # Button
                                                dbc.Button(
                                                    "⚡ Classify Material",
                                                    href="/predict",  # Link to the Classify page
                                                    color="primary",
                                                    className="w-100 mb-2",  # Add margin below to separate button and description
                                                    style={
                                                        "padding": "10px 10px",
                                                        "font-size": "20px",
                                                        "font-weight": "600",
                                                        "display": "flex",
                                                        "justify-content": "center",
                                                        "align-items": "center"
                                                    }
                                                ),
                                                # Description
                                                html.Div(
                                                    "Enter optical properties to predict the TCO material.",
                                                    style={"font-size": "14px", "color": "#555", "textAlign": "center"}
                                                )
                                            ],
                                            width=6  # Adjust width of the first column
                                        ),
                                        # Column for Visualize Transmission Button and Description
                                        dbc.Col(
                                            children=[
                                                # Button
                                                dbc.Button(
                                                    "📊 Visualize Transmission",
                                                    href="/visualize",  # Link to the Visualize page
                                                    color="primary",
                                                    className="w-100 mb-2",
                                                    style={
                                                        "padding": "10px 10px",
                                                        "font-size": "20px",
                                                        "font-weight": "600",
                                                        "display": "flex",
                                                        "justify-content": "center",
                                                        "align-items": "center"
                                                    }
                                                ),
                                                # Description
                                                html.Div(
                                                    "Enter materials name and select wavelength range to view the transmission curve.",
                                                    style={"font-size": "14px", "color": "#555", "textAlign": "center"}
                                                )
                                            ],
                                            width=6  # Adjust width of the second column
                                        )
                                    ]
                                )
                                ],
                                style={"text-align": "center"}
                            ),
                            width=6
                        )
                    ]
                )
            ]
        ),
        # Footer Section (30%)
        html.Div(
            style={
                "flex": "4",  # White frame with 30% height
                "backgroundColor": "white",
                "display": "flex",
                "flexDirection": "column",
                "padding": "0",  # Remove padding
                "margin": "0",  # Remove margin
                "width": "100%",  # Ensure full width
                "boxSizing": "border-box",  # Account for padding
            },
            children=[
                # First Row (Images - 55% of height)
                html.Div(
                    style={
                        "flex": "5.5",
                        "display": "flex",
                        "justifyContent": "space-evenly",
                        "alignItems": "center"
                    },
                    children=[
                        html.Div(
                            html.Img(
                                src=f"/assets/photo{i}.png",
                                style={
                                    "maxHeight": "90%",
                                    "maxWidth": "90%",
                                }
                            ),
                            style={"flex": "1", "textAlign": "center"}  # Take equal space for each image
                        ) for i in range(1, 8)  # Loop to generate all 7 images
                    ]
                ),

                # Second Row (Names - 15% of height)
                html.Div(
                    style={
                        "flex": "1.5",
                        "display": "flex",
                        "justifyContent": "space-evenly",
                        "alignItems": "center"
                    },
                    children=[
                        html.Div(
                            html.P(person["name"], style={"fontWeight": "bold", "margin": "0"}),
                            style={"flex": "1", "textAlign": "center"}
                        ) for person in [
                            {"name": "Camelia Dorody"},
                            {"name": "Norhazwani Md Yunos"},
                            {"name": "Hasrul Nisham Rosly"},
                            {"name": "Ong Ke Sheng"},
                            {"name": "Chengyoushi Xu"},
                            {"name": "Manzoore Elahi M. Soudagar"},
                            {"name": "Feng Zheng Jie"}
                        ]
                    ]
                ),

                # Third Row (Roles - 15% of height)
                html.Div(
                    style={
                        "flex": "1.5",
                        "display": "flex",
                        "justifyContent": "space-evenly",
                        "alignItems": "center",
                        "fontStyle": "italic",
                    },
                    children=[
                        html.Div(
                            html.P(person["role"], style={"margin": "0"}),
                            style={"flex": "1", "textAlign": "center"}
                        ) for person in [
                            {"role": "Semiconductor Project Leader"},
                            {"role": "Main Supervisor"},
                            {"role": "Co-Supervisor"},
                            {"role": "Developer"},
                            {"role": "Technical Coordinator"},
                            {"role": "Semiconductor Experimental Specialist"},
                            {"role": "Strategic Advisor"}
                        ]
                    ]
                ),

                # Fourth Row (Company and Location - 15% of height)
                html.Div(
                    style={
                        "flex": "1.5",
                        "display": "flex",
                        "justifyContent": "space-evenly",
                        "alignItems": "center",
                    },
                    children=[
                        html.Div(
                            html.P(
                                [html.Span(person["company"], style={"color": "black"}), html.Br(), person["location"]],
                                style={"margin": "0"}
                            ),
                            style={"flex": "1", "textAlign": "center"}
                        ) for person in [
                            {"company": "Zhejiang Xingyu Co., Ltd. China", "location": ""},
                            {"company": "Universiti Teknikal Malaysia Melaka", "location": ""},
                            {"company": "Universiti Teknikal Malaysia Melaka", "location": ""},
                            {"company": "Universiti Teknikal Malaysia Melaka", "location": ""},
                            {"company": "Lishui University China", "location": ""},
                            {"company": "Lishui University China", "location": ""},
                            {"company": "Zhejiang Xingyu Co., Ltd. China", "location": ""}
                        ]
                    ]
                )
            ]
        )
    ]
)