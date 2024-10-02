"""Longitudinal ORM Class."""
import json
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import LONGTEXT
import pandas as pd
import plotly.express as px
from hdash.db.db_base import Base


class Longitudinal(Base):
    """Longitudinal ORM Class."""

    __tablename__ = "longitudinal"

    atlas_id = Column(String(255), primary_key=True)
    label = Column(String(255))
    content = Column(LONGTEXT)
    content_plotly = Column(LONGTEXT)

    def __repr__(self):
        """Get summary."""
        return f"<Longitudinal({self.label})>"

    def get_content(self):
        """Get Content."""
        return self.content

    def has_data(self):
        """Get Data Status."""
        return len(self.content) > 0

    def get_html_plotly(self):
        """Get Plotly Fig Dump."""
        plotly_df = pd.DataFrame(json.loads(self.content_plotly))

        plotly_df["delta"] = plotly_df["Finish"] - plotly_df["Start"]
        fig = px.timeline(
            plotly_df,
            text="Event",
            x_start="Start",
            x_end="Finish",
            y="Grouping",
            color="Grouping",
            hover_data=["Event", "Samples", "Location"],
            range_x=["0", "100"],
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
        fig.update_traces(insidetextanchor="middle", textangle=20)

        for d in fig.data:
            filt = plotly_df["Grouping"] == d.name
            d.x = plotly_df[filt]["delta"].tolist()

        return fig.to_html(full_html=False)
