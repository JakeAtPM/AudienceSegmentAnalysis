import plotly.graph_objects as go
import plotly.io as pio

def register_custom_plotly_template():
    reporting_template = go.layout.Template(
    layout=dict(
        font=dict(family="IBM Plex Sans, Segoe UI, sans-serif", color="#0C0C3E"),
        paper_bgcolor="#F0F4F8",
        plot_bgcolor="#F0F4F8",
        title=dict(font=dict(color="#0C0C3E", size=24)),
        colorway=["#4A90E2", "#0C0C3E", "#7F8C8D", "#BDC3C7", "#3498DB"],
        xaxis=dict(
            color="#0C0C3E",
            gridcolor="#D1D5DB",
            zerolinecolor="#D1D5DB",
            title_font=dict(size=16, color="#0C0C3E"),
            tickfont=dict(size=13)
        ),
        yaxis=dict(
            color="#0C0C3E",
            gridcolor="#D1D5DB",
            zerolinecolor="#D1D5DB",
            title_font=dict(size=16, color="#0C0C3E"),
            tickfont=dict(size=13)
        ),
        legend=dict(
            bgcolor="#F0F4F8",
            font=dict(color="#0C0C3E")
        ),
        hoverlabel=dict(
            bgcolor="#4A90E2",
            font=dict(family="IBM Plex Sans, Segoe UI, sans-serif", color="#FFFFFF"),
            bordercolor="#0C0C3E"
        )
    )
    )
    
    pio.templates["reporting_theme"] = reporting_template
    pio.templates.default = "reporting_theme"