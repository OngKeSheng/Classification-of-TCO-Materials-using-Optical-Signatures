import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

layout = html.Div(
    style={
        "height": "100vh",           
        "margin": "0",               
        "padding": "0",              
        "overflow": "hidden"         
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
                                "max-width": "80%",   # 👈 Adjust image size here
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
                                    "max-width": "800px",   # 👈 Control width of text box
                                    "margin": "0 auto"      # Center inside column
                                }
                            ),

                            dbc.Button(
                                "🚀 Let's Get Started",
                                href="/predict",
                                color="success",
                                className="mt-3",
                                style={
                                    "font-size": "18px",
                                    "padding": "10px 20px",
                                    "border-radius": "10px"
                                }
                            )
                        ],
                        style={"text-align": "center"}  # ✅ keeps text centered
                    ),
                    width=6
                )
            ]
        )
    ]
)
