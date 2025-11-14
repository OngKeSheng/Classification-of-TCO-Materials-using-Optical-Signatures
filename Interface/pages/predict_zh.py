import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import joblib
import numpy as np

pipeline = joblib.load("xgb_pipeline_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

dash.register_page(__name__, path="/predict-zh")

layout = html.Div(
    style={
        "backgroundImage": "url('/assets/pic2.png')",
        "backgroundSize": "cover",
        "backgroundPosition": "center",
        "height": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "padding": "20px",
    },
    children=[
        html.Div(
            className="header",
            children=[
                # Left: Home button
                html.A("TCO 材料分类", href="/home-zh", className="home-btn"),

                # Middle: Language toggle
                html.Div(
                    style={"display": "flex", "alignItems": "center", "gap": "10px"},
                    children=[
                        dbc.Button("🇺🇸 English", href="/predict", color="light", className="mx-1"),
                        dbc.Button("🇨🇳 中文", href="/predict-zh", color="primary", className="mx-1"),
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
        dcc.Store(id="raw-wavelength"),
        dcc.Store(id="raw-absorbance"),
        dcc.Store(id="raw-transmission"),
        dcc.Store(id="raw-optical_density"),
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
                html.H2("🔍 从光学性质分类TCO材料", style={"textAlign": "center", "marginBottom": "20px"}),
                dbc.InputGroup([
                    dbc.InputGroupText("📏 波长 (nm)"),
                    dbc.Input(id="wavelength", type="number", min=300, max=800, step="any", placeholder="输入波长"),
                    dbc.InputGroupText("300–800"),
                ], className="mb-3"),
                dbc.InputGroup([
                    dbc.InputGroupText("🧪 吸光度"),
                    dbc.Input(id="absorbance", type="number", min=0, max=1, step="any", placeholder="输入吸光度"),
                    dbc.InputGroupText("0–1"),
                ], className="mb-3"),
                dbc.InputGroup([
                    dbc.InputGroupText("🔁 透射率 (%)"),
                    dbc.Input(id="transmission", type="number", min=0, max=100, step="any", placeholder="输入透射率"),
                    dbc.InputGroupText("0–100"),
                ], className="mb-3"),
                dbc.InputGroup([
                    dbc.InputGroupText("💡 光密度"),
                    dbc.Input(id="optical_density", type="number", min=0, max=100000, step="any", placeholder="输入光密度"),
                    dbc.InputGroupText("0–100000"),
                ], className="mb-3"),
                dbc.Button("🚀 分类材料", id="predict-btn", color="primary", className="mt-3 w-100"),
                html.Div(id="prediction-output", className="mt-3", style={"textAlign": "center"}),
            ]
        )
    ]
)

def register_callbacks(app):
    # -------------------------
    # Client-side callbacks
    # -------------------------
    app.clientside_callback(
        """
        function(val){
            if (val === null || val === undefined || val === '') {
                return [null, val];
            }
            var num = Number(val);
            if (isNaN(num)) {
                return [val, val];
            }
            var raw = num;
            var clamped = num;
            if (num < 300) clamped = 300;
            if (num > 800) clamped = 800;
            return [raw, clamped];
        }
        """,
        [Output("raw-wavelength", "data"), Output("wavelength", "value")],
        [Input("wavelength", "value")]
    )
    app.clientside_callback(
        """
        function(val){
            if (val === null || val === undefined || val === '') {
                return [null, val];
            }
            var num = Number(val);
            if (isNaN(num)) {
                return [val, val];
            }
            var raw = num;
            var clamped = num;
            if (num < 0) clamped = 0;
            if (num > 1) clamped = 1;
            return [raw, clamped];
        }
        """,
        [Output("raw-absorbance", "data"), Output("absorbance", "value")],
        [Input("absorbance", "value")]
    )
    app.clientside_callback(
        """
        function(val){
            if (val === null || val === undefined || val === '') {
                return [null, val];
            }
            var num = Number(val);
            if (isNaN(num)) {
                return [val, val];
            }
            var raw = num;
            var clamped = num;
            if (num < 0) clamped = 0;
            if (num > 100) clamped = 100;
            return [raw, clamped];
        }
        """,
        [Output("raw-transmission", "data"), Output("transmission", "value")],
        [Input("transmission", "value")]
    )
    app.clientside_callback(
        """
        function(val){
            if (val === null || val === undefined || val === '') {
                return [null, val];
            }
            var num = Number(val);
            if (isNaN(num)) {
                return [val, val];
            }
            var raw = num;
            var clamped = num;
            if (num < 0) clamped = 0;
            if (num > 100000) clamped = 100000;
            return [raw, clamped];
        }
        """,
        [Output("raw-optical_density", "data"), Output("optical_density", "value")],
        [Input("optical_density", "value")]
    )

    # -------------------------
    # Server-side prediction callback
    # -------------------------
    @app.callback(
        Output("prediction-output", "children"),
        Input("predict-btn", "n_clicks"),
        State("wavelength", "value"),
        State("absorbance", "value"),
        State("transmission", "value"),
        State("optical_density", "value"),
        State("raw-wavelength", "data"),
        State("raw-absorbance", "data"),
        State("raw-transmission", "data"),
        State("raw-optical_density", "data"),
        prevent_initial_call=True,
    )
    def predict_material(n_clicks,
                         wavelength, absorbance, transmission, optical_density,
                         raw_wavelength, raw_absorbance, raw_transmission, raw_optical_density):
        try:
            w = raw_wavelength if raw_wavelength is not None else wavelength
            a = raw_absorbance if raw_absorbance is not None else absorbance
            t = raw_transmission if raw_transmission is not None else transmission
            od = raw_optical_density if raw_optical_density is not None else optical_density

            missing = [name for name, val in [
                ("波长", w),
                ("吸光度", a),
                ("透射率 (%)", t),
                ("光密度", od)
            ] if val in (None, "")]

            if missing:
                return dbc.Alert(f"请输入有效的值用于: {', '.join(missing)}", color="danger")

            w = float(w); a = float(a); t = float(t); od = float(od)

            input_data = np.array([[w, a, t, od]])

            prediction = pipeline.predict(input_data)[0]
            material = label_encoder.inverse_transform([prediction])[0]

            proba = pipeline.predict_proba(input_data)[0]
            classes = label_encoder.classes_

            colors = ["primary", "success", "warning", "danger", "info"]
            progress_bars = []
            for i, (cls, p) in enumerate(zip(classes, proba)):
                progress_bars.append(
                    html.Div([
                        html.Strong(f"{cls}: {p*100:.2f}%"),
                        dbc.Progress(value=p*100, color=colors[i % len(colors)], striped=True, animated=True, className="mb-3")
                    ])
                )

            return html.Div([
                dbc.Alert(f"预测材料: {material}", color="success"),
                html.H5("分类概率:", style={"marginTop": "15px"}),
                html.Div(progress_bars)
            ])

        except Exception as e:
            return dbc.Alert(f"错误: {str(e)}", color="danger")