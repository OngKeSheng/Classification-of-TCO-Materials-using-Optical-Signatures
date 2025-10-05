import dash
from dash import html
import dash_bootstrap_components as dbc

# === Initialize App with Dash Pages ===
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# === Import predict page AFTER app exists ===
from pages import predict

# Register callbacks for predict page
predict.register_callbacks(app)



# === Custom CSS (same style as your predict-only app) ===
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>TCO Classifier</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #87CEEB; /* Sky Blue */
                margin: 0;
                font-family: Arial, sans-serif;
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
                gap: 15px; /* space between buttons */
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
            }

            .content {
                margin-top: 100px;
                margin-bottom: 80px;
                padding: 20px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <a href="/" class="home-btn">TCO Classifier</a>
            <div class="nav-right">
                <a href="/predict" class="predict-btn">Classify</a>
                <a href="/lookup" class="predict-btn">Lookup</a>
            </div>
        </div>
        {%app_entry%}
        <div class="footer">
            © 2025 TCO Classifier | Built with XGBoost & Dash
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
