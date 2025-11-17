import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/home-zh")

layout = html.Div(
    style={
        "height": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "margin": "0",
        "padding": "0",
        "boxSizing": "border-box",
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
                    "TCO 材料分类",
                    href="/home-zh",
                    className="home-btn",
                ),
                # Middle: Language toggle
                html.Div(
                    style={"display": "flex", "alignItems": "center", "gap": "10px"},
                    children=[
                        dbc.Button(
                            [html.Span("🇺🇸 English")],
                            href="/",
                            color="light",
                            className="mx-1",
                            style={"fontWeight": "normal"}
                        ),
                        dbc.Button(
                            [html.Span("🇨🇳 中文")],
                            href="/home-zh",
                            color="primary",
                            className="mx-1",
                            style={"fontWeight": "bold"}
                        )
                    ]
                ),
                # Right: (empty, or add exit button if needed)
                html.Div()  # Empty div to keep spacing
            ],
        ),

        # Content Section
        html.Div(
            style={
                "flex": "5.5",
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
                        dbc.Col(
                            html.Div(
                                [
                                    html.H2(
                                        "AI TCO材料分类器",
                                        style={
                                            "font-weight": "bold",
                                            "margin-bottom": "15px",
                                            "font-size": "32px"
                                        }
                                    ),
                                    html.P(
                                        """
                                        本项目利用XGBoost强大的能力，准确分类用于太阳能电池的透明导电氧化物（TCO）材料，包括AZO、FTO、ITO、MZO和ZnO。
                                        通过分析四个关键光学属性：吸光度、透射率、光密度和波长，模型能够快速可靠地进行材料预测。
                                        该AI工具旨在支持可再生能源研究，减少耗时的物理实验，帮助研究人员和工程师加速太阳能电池技术创新。
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
                                            dbc.Col(
                                                children=[
                                                    dbc.Button(
                                                        "⚡ 材料分类",
                                                        href="/predict-zh",
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
                                                    html.Div(
                                                        "输入光学属性以预测TCO材料。",
                                                        style={"font-size": "14px", "color": "#555", "textAlign": "center"}
                                                    )
                                                ],
                                                width=6
                                            ),
                                            dbc.Col(
                                                children=[
                                                    dbc.Button(
                                                        "📊 透射率可视化",
                                                        href="/visualize-zh",
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
                                                    html.Div(
                                                        "输入材料名称并选择波长范围以查看透射率曲线。",
                                                        style={"font-size": "14px", "color": "#555", "textAlign": "center"}
                                                    )
                                                ],
                                                width=6
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
        # Footer Section
        html.Div(
            style={
                "flex": "4",
                "backgroundColor": "white",
                "display": "flex",
                "flexDirection": "column",
                "padding": "0",
                "margin": "0",
                "width": "100%",
                "boxSizing": "border-box",
            },
            children=[
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
                            style={"flex": "1", "textAlign": "center"}
                        ) for i in range(1, 8)
                    ]
                ),
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
                            {"role": "半导体项目负责人"},
                            {"role": "主导师"},
                            {"role": "协助导师"},
                            {"role": "开发者"},
                            {"role": "技术协调员"},
                            {"role": "半导体实验专家"},
                            {"role": "战略顾问"}
                        ]
                    ]
                ),
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
                            {"company": "浙江兴宇股份有限公司 中国", "location": ""},
                            {"company": "马来西亚马六甲技术大学", "location": ""},
                            {"company": "马来西亚马六甲技术大学", "location": ""},
                            {"company": "马来西亚马六甲技术大学", "location": ""},
                            {"company": "中国丽水学院", "location": ""},
                            {"company": "中国丽水学院", "location": ""},
                            {"company": "浙江兴宇股份有限公司 中国", "location": ""}
                        ]
                    ]
                )
            ]
        )
    ]
)