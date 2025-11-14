import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Dash App Initialization
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# App Layout
app.layout = html.Div([
    # Store for language preference
    dcc.Store(id="language-store", data="en"),  # Default language is English

    # Language toggle buttons
    html.Div(
        id="language-selector",
        style={"display": "flex", "justifyContent": "center", "margin-bottom": "20px"},
        children=[
            dbc.Button(
                "English",
                id="english-button",
                color="primary",  # Default to blue
                className="mx-2", # Margin for spacing
                active=True,
                style={"font-weight": "bold"}
            ),
            dbc.Button(
                "中文",
                id="chinese-button",
                color="light",  # Default to white for inactive
                className="mx-2",
                active=False
            ),
        ]
    ),

    # Main content (language-sensitive)
    html.Div(id="content", className="content-container")
])

# Callback to toggle the language and update button styles
@app.callback(
    [
        Output("language-store", "data"),  # Update selected language in the dcc.Store
        Output("english-button", "color"),
        Output("english-button", "active"),
        Output("english-button", "style"),
        Output("chinese-button", "color"),
        Output("chinese-button", "active"),
        Output("chinese-button", "style"),
    ],
    Input("english-button", "n_clicks"),
    Input("chinese-button", "n_clicks"),
    State("language-store", "data")
)
def toggle_language(english_clicks, chinese_clicks, current_language):
    # Default button styles
    button_active_style = {"font-weight": "bold"}
    button_inactive_style = {"font-weight": "normal"}
    
    # Detect which language button was clicked
    context = dash.callback_context  # Get callback context to identify trigger
    if not context.triggered:
        return "en", "primary", True, button_active_style, "light", False, button_inactive_style

    triggered_id = context.triggered[0]["prop_id"].split(".")[0]
    
    if triggered_id == "english-button" and current_language != "en":
        return (
            "en",              # Language is English
            "primary",         # English button color -> blue
            True,              # English button active
            button_active_style,
            "light",           # Chinese button color -> white
            False,             # Chinese button inactive
            button_inactive_style
        )
    elif triggered_id == "chinese-button" and current_language != "zh":
        return (
            "zh",              # Language is Chinese
            "light",           # English button color -> white
            False,             # English button inactive
            button_inactive_style,
            "primary",         # Chinese button color -> blue
            True,              # Chinese button active
            button_active_style
        )
    
    # Return current state if no changes
    return (
        current_language,
        "primary" if current_language == "en" else "light",
        current_language == "en",
        button_active_style if current_language == "en" else button_inactive_style,
        "primary" if current_language == "zh" else "light",
        current_language == "zh",
        button_active_style if current_language == "zh" else button_inactive_style
    )

# Callback to dynamically change content based on language selection
@app.callback(
    Output("content", "children"),
    Input("language-store", "data")
)
def update_content(language):
    if language == "en":
        return html.Div([
            html.H1("Welcome to TCO Material Classifier"),
            html.P("Enter optical properties to predict TCO materials."),
        ])
    elif language == "zh":
        return html.Div([
            html.H1("欢迎使用TCO材料分类器"),
            html.P("输入光学特性以预测TCO材料。"),
        ])

# Run App
if __name__ == "__main__":
    app.run(debug=True, port=8000)