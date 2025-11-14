import dash
from dash import html
import dash_bootstrap_components as dbc
# === Initialize App with Dash Pages ===
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# === Custom CSS (same style as your predict-only app) ===
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>TCO 材料分类</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #87CEEB;
                margin: 0;
                font-family: Arial, sans-serif;
                overflow-x: hidden;
            }
            /* Header */
            .header {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: white;
                color: black;
                padding: 15px 30px;
                font-size: 26px;
                font-weight: 900;
                border-bottom: 2px solid #ccc;
                z-index: 1000;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .home-btn {
                text-decoration: none;
                color: black;
                font-weight: 900;
            }
            .nav-right {
                display: flex;
                gap: 15px;
            }
            .predict-btn {
                text-decoration: none;
                background-color: #007BFF;
                color: white !important;
                padding: 8px 18px;
                border-radius: 12px;
                font-size: 18px;
                font-weight: 600;
            }
            .predict-btn:hover {
                background-color: #0056b3;
            }
            /* Content area (keeps pages inside header/footer) */
            .content {
                margin-top: 70px;
                margin-bottom: 90px;
                padding: 0px;
                min-height: calc(100vh - 100px);
                box-sizing: border-box;
                overflow-y: auto;
            }
            /* Footer */
            .footer {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: white;
                color: black;
                text-align: center;
                padding: 10px;
                border-top: 2px solid #ccc;
                z-index: 1000;
            }
        </style>
    </head>
    <body>
        <div class="content">
            {%app_entry%}
        </div>
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
"""
# === Layout ===
app.layout = dash.page_container
if __name__ == "__main__":
    app.run(debug=True)