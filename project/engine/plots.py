# File: plots.py
# Author: Dawson Maska (dawsonwm@bu.edu), 12/8/2025
# Description: Define all of our plots here so as to not clutter views.py (I looked at examples to help write these plots I'm not great with plotly)


import plotly.graph_objects as go


def win_loss_plot(results):
    bot1 = results["bot1"]
    bot2 = results["bot2"]

    names = [bot1["name"], bot2["name"]]

    fig = go.Figure()

    fig.add_bar(
        name="Wins",
        x=names,
        y=[bot1["wins"], bot2["wins"]],
        marker_color="#2ecc71",
    )
    fig.add_bar(
        name="Losses",
        x=names,
        y=[bot1["losses"], bot2["losses"]],
        marker_color="#e74c3c",
    )
    fig.add_bar(
        name="Draws",
        x=names,
        y=[bot1["draws"], bot2["draws"]],
        marker_color="#f1c40f",
    )

    fig.update_layout(
        barmode="stack",
        title="Win / Loss / Draw",
        template="plotly_dark",

        autosize=False,
        width=588,
        height=500,

        margin=dict(l=100, r=100, t=80, b=80),
        showlegend=False,  
    )

    fig.update_xaxes(
        automargin=True,
    )

    return fig








def win_rate_plot(results):
    def win_rate(bot):
        total = bot["wins"] + bot["losses"] + bot["draws"]
        return (bot["wins"] / total) * 100 if total else 0

    fig = go.Figure(
        data=[
            go.Bar(
                x=[results["bot1"]["name"], results["bot2"]["name"]],
                y=[
                    win_rate(results["bot1"]),
                    win_rate(results["bot2"]),
                ],
                marker_color=["#2ecc71", "#3498db"],
            )
        ]
    )

    fig.update_layout(
        title="Win Rate (%)",
        yaxis=dict(range=[0, 100]),
        template="plotly_dark",
    )
    return fig


def avg_turns_plot(results):
    fig = go.Figure(
        data=[
            go.Bar(
                x=[results["bot1"]["name"], results["bot2"]["name"]],
                y=[
                    results["bot1"]["avg_turns"],
                    results["bot2"]["avg_turns"],
                ],
                marker_color=["#9b59b6", "#e67e22"],
            )
        ]
    )

    fig.update_layout(
        title="Average Survival Turns",
        template="plotly_dark",
    )
    return fig


def avg_apples_plot(results):
    fig = go.Figure(
        data=[
            go.Bar(
                x=[results["bot1"]["name"], results["bot2"]["name"]],
                y=[
                    results["bot1"]["avg_apples"],
                    results["bot2"]["avg_apples"],
                ],
                marker_color=["#f39c12", "#e74c3c"],
            )
        ]
    )

    fig.update_layout(
        title="Average Apples Eaten",
        template="plotly_dark",
    )
    return fig
