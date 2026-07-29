import sys
import os
import re
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PAGE_PATH = BASE_DIR / "pages" / "1_Ekspansi_Industri.py"
OUT_DIR = BASE_DIR / "tools" / "streamlittopdf"
VISUALS_DIR = OUT_DIR / "visuals"
VISUALS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Read the original Streamlit file
with open(PAGE_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# 2. Patch the code to Light Theme (White Background) and remove st.cache_data
# Replace colors
code = code.replace("#1E1E1E", "#FFFFFF")
code = code.replace("background-color: #262730", "background-color: #FFFFFF")
code = code.replace("color='white'", "color='black'")
code = code.replace("labelColor='white'", "labelColor='black'")
code = code.replace("titleColor='white'", "titleColor='black'")
code = code.replace("color='#ECEFF1'", "color='#212121'")
code = code.replace("color: #ECEFF1", "color: #212121")
code = code.replace("color: #E0E0E0", "color: #212121")
code = code.replace("color='#E0E0E0'", "color='#212121'")
code = code.replace("labelColor='#B0BEC5'", "labelColor='#424242'")
code = code.replace("titleColor='#B0BEC5'", "titleColor='#424242'")
code = code.replace("gridColor='#333333'", "gridColor='#E0E0E0'")
code = code.replace("color: #A0AEC0", "color: #424242")
code = code.replace("color: #718096", "color: #424242")
code = code.replace("color: #FFFFFF", "color: #000000")
code = code.replace("border: 1px solid #333", "border: 1px solid #E0E0E0")
code = code.replace("border-top: 1px solid #333", "border-top: 1px solid #E0E0E0")
code = code.replace("font=dict(color=\"#ECEFF1\"", "font=dict(color=\"black\"")

# For Plotly
code = code.replace("bgcolor='rgba(0,0,0,0)'", "bgcolor='white'")
code = code.replace("st.stop()", "pass")

# Write patched code to a temporary file
patched_file = OUT_DIR / "_temp_patched_page.py"
with open(patched_file, "w", encoding="utf-8") as f:
    f.write(code)

print("Created patched file.")

class SidebarMock:
    def __init__(self, mock):
        self.mock = mock
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def __getattr__(self, name):
        def dummy(*args, **kwargs): pass
        return dummy

class MockStreamlit:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.md_lines = []
        self.chart_counter = 0
        self.altair_queue = []
        self.sidebar = SidebarMock(self)

    def set_page_config(self, *args, **kwargs): pass
    def cache_data(self, func=None, **kwargs): 
        if func: return func
        return lambda f: f
    
    def markdown(self, text, **kwargs):
        self.md_lines.append(text + "\n")
    def title(self, text, **kwargs):
        self.md_lines.append(f"# {text}\n")
    def header(self, text, **kwargs):
        self.md_lines.append(f"## {text}\n")
    def subheader(self, text, **kwargs):
        self.md_lines.append(f"### {text}\n")
    def caption(self, text, **kwargs):
        self.md_lines.append(f"*{text}*\n")
    def write(self, *args, **kwargs):
        for arg in args:
            self.md_lines.append(str(arg) + "\n")
            
    def dataframe(self, df, **kwargs):
        try:
            self.md_lines.append("\n" + df.to_markdown(index=False) + "\n")
        except: pass
    def table(self, df, **kwargs):
        try:
            self.md_lines.append("\n" + df.to_markdown() + "\n")
        except: pass

    def altair_chart(self, chart, **kwargs):
        self.chart_counter += 1
        path = self.output_dir / f"visuals/chart_full_{self.chart_counter}.png"
        try:
            chart.save(str(path))
            self.md_lines.append(f"![Chart {self.chart_counter}](visuals/chart_full_{self.chart_counter}.png)\n")
        except Exception as e:
            self.md_lines.append(f"> [!WARNING]\n> Failed to save Altair chart: {e}\n")

    def plotly_chart(self, fig, **kwargs):
        self.chart_counter += 1
        path = self.output_dir / f"visuals/chart_full_{self.chart_counter}.png"
        try:
            fig.write_image(str(path))
            self.md_lines.append(f"![Chart {self.chart_counter}](visuals/chart_full_{self.chart_counter}.png)\n")
        except Exception as e:
            self.md_lines.append(f"> [!WARNING]\n> Failed to save Plotly chart: {e}\n")

    def expander(self, label, **kwargs):
        class Expander:
            def __init__(self, mock, label):
                self.mock = mock
                self.label = label
            def __enter__(self):
                self.mock.md_lines.append(f"\n**{self.label}**\n")
                return self
            def __exit__(self, *args): pass
        return Expander(self, label)

    def columns(self, spec):
        class Col:
            def __init__(self, mock): self.mock = mock
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def __getattr__(self, name):
                if name in ['altair_chart', 'plotly_chart', 'markdown', 'metric']:
                    return getattr(self.mock, name)
                def dummy(*args, **kwargs): pass
                return dummy
            
            def altair_chart(self, chart, **kwargs):
                self.mock.altair_queue.append(chart)
                if len(self.mock.altair_queue) == 3:
                    import altair as alt
                    from pathlib import Path
                    c1, c2, c3 = self.mock.altair_queue
                    row = alt.hconcat(c1, c2, c3, spacing=20).configure_view(stroke=None).configure_axis(grid=True, gridColor='#E0E0E0').configure_title(color='black').configure(background='white')
                    self.mock.altair_queue = []
                    self.mock.chart_counter += 1
                    path = self.mock.output_dir / f"visuals/chart_full_{self.mock.chart_counter}.png"
                    row.save(str(path))
                    self.mock.md_lines.append(f"![Chart {self.mock.chart_counter}](visuals/chart_full_{self.mock.chart_counter}.png)\n")
            def plotly_chart(self, fig, **kwargs):
                self.mock.plotly_chart(fig, **kwargs)
            def metric(self, label, value, **kwargs):
                self.mock.md_lines.append(f"**{label}**: {value}\n")
            def markdown(self, *args, **kwargs):
                self.mock.markdown(*args, **kwargs)
        
        if type(spec) == int:
            return [Col(self) for _ in range(spec)]
        return [Col(self) for _ in spec]

    def selectbox(self, label, options, format_func=None, **kwargs):
        return list(options)[0] if type(options) == dict else options[0]

    def warning(self, msg, **kwargs):
        self.md_lines.append(f"> [!WARNING]\n> {msg}\n")
    def info(self, msg, **kwargs):
        self.md_lines.append(f"> [!NOTE]\n> {msg}\n")
    def error(self, msg, **kwargs):
        self.md_lines.append(f"> [!ERROR]\n> {msg}\n")
    def success(self, msg, **kwargs):
        self.md_lines.append(f"> [!SUCCESS]\n> {msg}\n")
    def html(self, msg, **kwargs): pass
    def __getattr__(self, name):
        def dummy(*args, **kwargs): pass
        return dummy

import sys
mock_st = MockStreamlit(OUT_DIR)
sys.modules['streamlit'] = mock_st
sys.path.insert(0, str(os.path.abspath('../../')))

try:
    import _temp_patched_page
except Exception as e:
    import traceback
    print(f"Error running patched page: {e}")
    traceback.print_exc()

# Save the captured markdown
final_md = "".join(mock_st.md_lines)
with open(OUT_DIR / "chapter_1_full.md", "w", encoding="utf-8") as f:
    f.write(final_md)

print("Extraction Full Complete!")
