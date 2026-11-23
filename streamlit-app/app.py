import base64
import mimetypes
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Discrete Math Final Project", layout="wide")

html_path = Path(__file__).resolve().parent.parent / "index.html"
html = html_path.read_text(encoding="utf-8")
project_dir = html_path.parent


def embed_local_asset(match: re.Match[str]) -> str:
    asset_name = match.group("path")
    if asset_name.startswith(("http:", "https:", "data:", "//", "/")):
        return match.group(0)

    asset_path = project_dir / asset_name
    content_type = mimetypes.guess_type(asset_path.name)[0]
    if content_type is None:
        raise ValueError(f"Cannot determine the content type for {asset_path.name}")

    encoded = base64.b64encode(asset_path.read_bytes()).decode("ascii")
    return (
        f'{match.group("prefix")}data:{content_type};base64,{encoded}'
        f'{match.group("quote")}'
    )


html = re.sub(
    r'(?P<prefix>src=["\'])(?P<path>[^"\']+)(?P<quote>["\'])',
    embed_local_asset,
    html,
)
components.html(html, height=1000, scrolling=True)
