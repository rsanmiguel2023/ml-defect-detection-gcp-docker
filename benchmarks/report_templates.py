"""
Reusable Markdown template helpers for benchmark reports.
"""

import textwrap
from pathlib import Path

import pandas as pd


def heading(title: str, level: int = 2) -> str:
    return f"{'#' * level} {title}"


def paragraph(text: str) -> str:
    return textwrap.dedent(text).strip()


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def image(markdown_path: str, filesystem_path: str, alt_text: str) -> str:
    if Path(filesystem_path).exists():
        return f"![{alt_text}]({markdown_path})"

    return "_Chart not available._"


def dataframe_to_markdown(df: pd.DataFrame | None) -> str:
    if df is None or df.empty:
        return "_No benchmark data available._"

    cleaned_df = df.copy()
    cleaned_df = cleaned_df.fillna("")

    return cleaned_df.to_markdown(index=False)


def markdown_table(rows: list[tuple[str, object]]) -> str:
    table = ["| Property | Value |", "|---|---|"]

    for key, value in rows:
        table.append(f"| {key} | {value if value not in [None, ''] else 'N/A'} |")

    return "\n".join(table)


def code_block(content: str, language: str = "text") -> str:
    fence = "```"
    return f"{fence}{language}\n{content.strip()}\n{fence}"
