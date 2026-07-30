import sys
import os
import glob
from pathlib import Path

BASE_DIR = Path(r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2").resolve()
OUT_DIR = BASE_DIR / "tools" / "streamlittopdf"
VISUALS_DIR = OUT_DIR / "visuals"
VISUALS_DIR.mkdir(parents=True, exist_ok=True)

class MockModule:
    def __getattr__(self, name):
        return self
    def __call__(self, *args, **kwargs): 
        return self

sys.modules['folium'] = MockModule()
sys.modules['streamlit_folium'] = MockModule()
sys.modules['pydeck'] = MockModule()

class MockStreamlit:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.md_lines = []
        self.chart_counter = 0
        self.sidebar = self

    def set_page_config(self, *args, **kwargs): pass
    def cache_data(self, func=None, **kwargs): 
        if func: return func
        return lambda f: f
    
    def markdown(self, text, **kwargs):
        self.md_lines.append(str(text) + "\n\n")
    def title(self, text, **kwargs):
        self.md_lines.append(f"# {text}\n\n")
    def header(self, text, **kwargs):
        self.md_lines.append(f"## {text}\n\n")
    def subheader(self, text, **kwargs):
        self.md_lines.append(f"### {text}\n\n")
    def caption(self, text, **kwargs):
        self.md_lines.append(f"*{text}*\n\n")
    def write(self, *args, **kwargs):
        for arg in args:
            self.md_lines.append(str(arg) + "\n\n")
            
    def dataframe(self, df, **kwargs):
        try:
            self.md_lines.append("\n" + df.to_markdown(index=False) + "\n\n")
        except: pass
    def table(self, df, **kwargs):
        try:
            self.md_lines.append("\n" + df.to_markdown() + "\n\n")
        except: pass

    def altair_chart(self, chart, **kwargs):
        self.chart_counter += 1
        path = self.output_dir / f"visuals/chart_full_{self.chapter_num}_{self.chart_counter}.png"
        try:
            print(f"Saving altair chart {self.chart_counter}")
            chart.save(str(path))
            self.md_lines.append(f"![Chart {self.chart_counter}](visuals/chart_full_{self.chapter_num}_{self.chart_counter}.png)\n\n")
        except Exception as e:
            self.md_lines.append(f"> [!WARNING]\n> Failed to save Altair chart: {e}\n\n")

    def plotly_chart(self, fig, **kwargs):
        self.chart_counter += 1
        path = self.output_dir / f"visuals/chart_full_{self.chapter_num}_{self.chart_counter}.png"
        try:
            print(f"Saving plotly chart {self.chart_counter}")
            fig.write_image(str(path))
            self.md_lines.append(f"![Chart {self.chart_counter}](visuals/chart_full_{self.chapter_num}_{self.chart_counter}.png)\n\n")
        except Exception as e:
            self.md_lines.append(f"> [!WARNING]\n> Failed to save Plotly chart: {e}\n\n")

    def expander(self, label, **kwargs):
        class Expander:
            def __init__(self, mock, label):
                self.mock = mock
                self.label = label
            def __enter__(self):
                self.mock.md_lines.append(f"\n**{self.label}**\n\n")
                return self
            def __exit__(self, *args): pass
        return Expander(self, label)
        
    def tabs(self, tab_names):
        class Tab:
            def __init__(self, mock, name):
                self.mock = mock
                self.name = name
            def __enter__(self):
                self.mock.md_lines.append(f"\n**Tab: {self.name}**\n\n")
                return self
            def __exit__(self, *args): pass
            def __getattr__(self, name):
                if name in ['altair_chart', 'plotly_chart', 'markdown', 'metric', 'dataframe', 'table', 'write', 'columns']:
                    return getattr(self.mock, name)
                def dummy(*args, **kwargs): pass
                return dummy
        return [Tab(self, name) for name in tab_names]

    def columns(self, spec):
        class Col:
            def __init__(self, mock): self.mock = mock
            def markdown(self, *args, **kwargs): self.mock.markdown(*args, **kwargs)
            def altair_chart(self, chart, **kwargs): self.mock.altair_chart(chart, **kwargs)
            def plotly_chart(self, fig, **kwargs): self.mock.plotly_chart(fig, **kwargs)
            def metric(self, label, value, delta=None, **kwargs):
                self.mock.md_lines.append(f"**{label}**: {value} {f'({delta})' if delta else ''}\n\n")
            def dataframe(self, *args, **kwargs): self.mock.dataframe(*args, **kwargs)
            def table(self, *args, **kwargs): self.mock.table(*args, **kwargs)
            def write(self, *args, **kwargs): self.mock.write(*args, **kwargs)
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def __getattr__(self, name):
                def dummy(*args, **kwargs): pass
                return dummy
        
        if type(spec) == int:
            return [Col(self) for _ in range(spec)]
        return [Col(self) for _ in spec]

    def selectbox(self, label, options, format_func=None, **kwargs):
        return list(options)[0] if type(options) == dict else options[0]
        
    def multiselect(self, label, options, default=None, **kwargs):
        if default: return default
        return [list(options)[0]] if type(options) == dict else [options[0]]
        
    def checkbox(self, label, value=False, **kwargs):
        return value

    def warning(self, msg, **kwargs):
        self.md_lines.append(f"> [!WARNING]\n> {msg}\n\n")
    def info(self, msg, **kwargs):
        self.md_lines.append(f"> [!NOTE]\n> {msg}\n\n")
    def error(self, msg, **kwargs):
        self.md_lines.append(f"> [!ERROR]\n> {msg}\n\n")
    def success(self, msg, **kwargs):
        self.md_lines.append(f"> [!SUCCESS]\n> {msg}\n\n")
    def divider(self):
        self.md_lines.append("---\n\n")
        
    def pydeck_chart(self, *args, **kwargs): pass
    def components(self): return MockModule()
    
    def __getattr__(self, name):
        def dummy(*args, **kwargs): pass
        return dummy


sys.modules['streamlit'] = MockStreamlit(OUT_DIR)
sys.path.insert(0, str(BASE_DIR))
import streamlit as st
import traceback

for page_path in sorted(glob.glob(str(BASE_DIR / "pages" / "[1-9]_*.py"))):
    filename = os.path.basename(page_path)
    chapter_num = filename.split("_")[0]
    
    st.chapter_num = chapter_num
    
    with open(page_path, "r", encoding="utf-8") as f:
        code = f.read()

    code = code.replace("#1E1E1E", "#FFFFFF")
    code = code.replace("background-color: #262730", "background-color: #FFFFFF")
    code = code.replace("color='white'", "color='black'")
    code = code.replace("labelColor='white'", "labelColor='black'")
    code = code.replace("titleColor='white'", "titleColor='black'")
    code = code.replace("bgcolor='rgba(0,0,0,0)'", "bgcolor='white'")
    code = code.replace("st.stop()", "pass")
    code = code.replace("from src.components.sidebar import render_sidebar", "")
    code = code.replace("render_sidebar()", "")

    original_file = str(page_path).replace("\\\\", "/")
    code = f"__file__ = r'{original_file}'\n" + code

    patched_file = OUT_DIR / f"_temp_patched_page_{chapter_num}.py"
    with open(patched_file, "w", encoding="utf-8") as f:
        f.write(code)

    st.md_lines = []
    
    try:
        print(f"Executing {filename}...")
        exec(code, {'__file__': original_file, 'st': st, 'streamlit': st})
    except Exception as e:
        print(f"Error executing {filename}: {e}")
        traceback.print_exc()
        
    final_md = "".join(st.md_lines)
    # Post processing cleanup
    final_md = final_md.replace("<div style='height: 10px;'></div>", "")
    final_md = final_md.replace("<br>", "\n")
    
    out_md = OUT_DIR / f"chapter_{chapter_num}.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(final_md)
    print(f"Generated {out_md.name} from {filename}")

print("Extraction Full Complete!")
