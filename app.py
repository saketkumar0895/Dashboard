import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# 1. Enable pages and load Bootstrap theme
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

# 2. Build a Navbar that links to each registered page
navbar = dbc.Navbar(
    dbc.Container([
        # Brand / Title
        html.A(
            dbc.Row([
                dbc.Col(html.H2("CLINICAL DASHBOARD", className="text-white mb-0")),
                dbc.Col(
                    html.Small(
                        "Designed for Vibe Coding Event",
                        className="text-light"
                    )
                )
            ], className="g-0 align-items-center"),
            href="/",
            style={"textDecoration": "none"}
        ),

        # Nav links (use exact matching to highlight active page)
        dbc.Nav(
            [
                dbc.NavLink(page["name"],
                            href=page["path"],
                            active="exact",
                            className="mx-1")
                for page in dash.page_registry.values()
                if page["module"].startswith("pages.")
            ],
            pills=True
        )
    ]),
    color="dark",
    dark=True,
    sticky="top",
    className="mb-4"
)

# 3. App layout: Navbar + page container
app.layout = html.Div([
    dcc.Location(id="url"),   # needed for pathname detection
    navbar,
    dash.page_container       # <-- this is where pages get rendered
])

if __name__ == "__main__":
    app.run(debug=True)