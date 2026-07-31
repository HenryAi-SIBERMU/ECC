import sys
import os
import pandas as pd
from pathlib import Path
import json
import unittest.mock as mock

# Add project root to path
ROOT = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT))

VIS_DIR = ROOT / "tools" / "streamlittopdf" / "visuals_bab3"
VIS_DIR.mkdir(parents=True, exist_ok=True)

md_output = []
chart_counter = 0

class MockStreamlit:
    components = mock.MagicMock()
    components.v1 = mock.MagicMock()

    class column_config:
        def TextColumn(*args, **kwargs): pass
        def NumberColumn(*args, **kwargs): pass

    class SessionState(dict):
        def __getattr__(self, item):
            try: return self[item]
            except KeyError: raise AttributeError(item)
        def __setattr__(self, key, value):
            self[key] = value

    sidebar = None
    session_state = SessionState()
    
    def __init__(self):
        self.sidebar = self
        self.session_state = MockStreamlit.session_state

    def markdown(self, text, *args, **kwargs):
        md_output.append(str(text))
    def header(self, text, *args, **kwargs):
        md_output.append(f"## {text}")
    def subheader(self, text, *args, **kwargs):
        md_output.append(f"### {text}")
    def caption(self, text, *args, **kwargs):
        md_output.append(f"> {text}")
    def error(self, text, *args, **kwargs):
        md_output.append(f"> ERROR: {text}")
    def info(self, text, *args, **kwargs):
        md_output.append(f"> INFO: {text}")
    def success(self, text, *args, **kwargs):
        md_output.append(f"> SUCCESS: {text}")
    def warning(self, text, *args, **kwargs):
        md_output.append(f"> WARNING: {text}")
    def dataframe(self, data, *args, **kwargs):
        if isinstance(data, pd.DataFrame):
            md_output.append(data.to_markdown(index=False))
    def table(self, data, *args, **kwargs):
        if isinstance(data, pd.DataFrame):
            md_output.append(data.to_markdown(index=False))
        else:
            md_output.append(pd.DataFrame(data).to_markdown(index=False))
    def plotly_chart(self, fig, *args, **kwargs):
        global chart_counter
        chart_counter += 1
        filename = f"chart_{chart_counter}.png"
        path = VIS_DIR / filename
        fig.write_image(str(path), width=800, height=450, scale=2)
        md_output.append(f"\n![Chart](visuals_bab3/{filename})\n")
    def altair_chart(self, chart, *args, **kwargs):
        global chart_counter
        chart_counter += 1
        filename = f"chart_{chart_counter}.png"
        path = VIS_DIR / filename
        try:
            chart.save(str(path), format='png', scale_factor=2.0)
            md_output.append(f"\n![Chart](visuals_bab3/{filename})\n")
        except Exception as e:
            md_output.append(f"> Altair chart save failed: {e}")
    
    # UI mocks
    def set_page_config(self, *args, **kwargs): pass
    def columns(self, spec):
        if isinstance(spec, int):
            return [MockStreamlit() for _ in range(spec)]
        return [MockStreamlit() for _ in spec]
    def expander(self, label, *args, **kwargs):
        md_output.append(f"\n<details><summary>{label}</summary>\n")
        class ExpanderCtx:
            def __enter__(self): return MockStreamlit()
            def __exit__(self, *args, **kwargs): md_output.append("\n</details>\n")
        return ExpanderCtx()
    def tabs(self, labels):
        return [MockStreamlit() for _ in labels]
    def selectbox(self, label, options, *args, **kwargs):
        # Always return the first option to simulate one path
        if isinstance(options, dict):
            return list(options.keys())[0]
        return options[0]
    def cache_data(self, func=None, *args, **kwargs):
        if func: return func
        def wrapper(f): return f
        return wrapper
    def stop(self): pass
    
    def __enter__(self): return self
    def __exit__(self, *args, **kwargs): pass
    
    def __getattr__(self, name):
        def dummy(*args, **kwargs):
            return MockStreamlit()
        return dummy

st = MockStreamlit()
sys.modules['streamlit'] = st
sys.modules['streamlit.components'] = mock.MagicMock()
sys.modules['streamlit.components.v1'] = mock.MagicMock()

# Run the page
import importlib.util
spec = importlib.util.spec_from_file_location("page_module", str(ROOT / "pages" / "3_Beban_Kesehatan.py"))
page_module = importlib.util.module_from_spec(spec)
# Change directory so relative paths in page work
os.chdir(str(ROOT))
spec.loader.exec_module(page_module)

out_md = "\n\n".join(md_output)
with open("tools/streamlittopdf/chapter_3.md", "w", encoding="utf-8") as f:
    f.write(out_md)

print("Extraction completed using mock Streamlit!")
