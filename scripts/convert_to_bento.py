import re
import os

source_file = r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\pages\12_Infografis_Summary.py"
target_file = r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\pages\13_Infografis_Fakta.py"

with open(source_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. We want all the data loading logic.
# The data loading starts at `# --- Data Loading ---`
# It goes all the way down, mixed with `render_infographic_row` and `st.markdown`.
# We can just keep the whole file, but replace the `render_infographic_row` definition and calls.
# And we strip out `st.set_page_config`, `render_sidebar()`, and old `st.markdown` for badges.

lines = content.split('\n')
new_lines = []

in_old_css = False
for line in lines:
    if 'st.set_page_config(' in line:
        new_lines.append('st.set_page_config(')
        new_lines.append('    page_title="Infografis: Temuan Utama",')
        new_lines.append('    page_icon="📊",')
        new_lines.append('    layout="wide",')
        new_lines.append('    initial_sidebar_state="expanded"')
        new_lines.append(')')
        continue
    
    if 'page_title=' in line and 'Infografis Summary' in line:
        continue
    if 'page_icon=' in line and 'Celios China' in line:
        continue
    if 'layout=' in line and 'wide' in line:
        continue
    if 'initial_sidebar_state=' in line:
        continue
        
    if line.strip() == 'render_sidebar()':
        new_lines.append('render_sidebar()')
        new_lines.append('')
        # Inject our CSS and Bento Grid function here
        new_lines.append('''
st.markdown("""
<style>
    .bento-container {
        background-color: #1A3C2A;
        padding: 30px;
        border-radius: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: white;
    }
    .bento-title {
        text-align: center; font-size: 2.8rem; font-weight: 800; margin-bottom: 30px;
        color: #E8F5E9; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .category-badge {
        background-color: #F9A825; color: #212121; padding: 12px 30px;
        border-radius: 30px; font-size: 1.2rem; font-weight: 700;
        text-align: center; margin: 35px auto 20px auto; width: fit-content;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .bento-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px; margin-bottom: 20px;
    }
    .bento-card {
        background-color: #FFFFFF; border-radius: 16px; padding: 24px;
        text-align: center; color: #212121; box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        transition: transform 0.2s ease-in-out; display: flex; flex-direction: column;
        justify-content: flex-start;
    }
    .bento-card:hover { transform: translateY(-5px); }
    .card-title { font-size: 1rem; font-weight: 600; color: #424242; margin-bottom: 12px; line-height: 1.3; }
    .card-value { font-size: 2.5rem; font-weight: 900; color: #2E7D32; margin: 10px 0; line-height: 1.1; }
    .card-desc { font-size: 0.85rem; color: #757575; margin-top: 10px; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="bento-container"><div class="bento-title">Fakta Keras & Temuan Utama</div>', unsafe_allow_html=True)

def render_bento_category(title):
    st.markdown(f'</div><div class="category-badge">{title}</div><div class="bento-grid">', unsafe_allow_html=True)

def render_bento_card(title, value, description):
    st.markdown(f"""
        <div class="bento-card">
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
            <div class="card-desc">{description}</div>
        </div>
    """, unsafe_allow_html=True)

def render_infographic_row(icon, key_indicator, title, unit, label_start, val_start, label_end, val_end, delta_pct, recommendation, color_theme="gray", reverse_delta=True):
    render_bento_card(f"{icon} {key_indicator}", f"{val_end} {unit}", recommendation)
    
def render_insight_box(title, body, border_color=""):
    pass # Ignore insight boxes for Bento UI
''')
        continue
        
    if '<style>' in line and 'main-title' in lines[lines.index(line)+1]:
        in_old_css = True
        continue
    if '</style>' in line and in_old_css:
        in_old_css = False
        continue
    if in_old_css:
        continue
        
    if 'st.markdown(\'<h1 class="main-title"' in line:
        continue
    if 'st.markdown(\'<p class="sub-title"' in line:
        continue
    if 'poster_container =' in line:
        continue
    if 'st.markdown("<div style=\\'height: 20px;' in line:
        continue
        
    if 'def render_infographic_row(' in line:
        # We already injected a replacement for this
        in_func = True
        continue
    
    if 'def render_insight_box(' in line:
        in_func = True
        continue
        
    if 'st.markdown(\'<div class="sector-badge"' in line:
        # Extract the category name from the HTML
        match = re.search(r'>([^<]+)</div>', line)
        if match:
            cat_name = match.group(1)
            new_lines.append(f'render_bento_category("{cat_name}")')
        continue
        
    # Skip the old top hero cards
    if 'c_h1, c_h2, c_h3, c_h4 = st.columns(4)' in line:
        continue
    if 'with c_h1:' in line or 'with c_h2:' in line or 'with c_h3:' in line or 'with c_h4:' in line:
        continue
    if '<div class="summary-card">' in line:
        continue
    if '<div class="card-label">' in line:
        continue
    if '<div class="card-value"' in line:
        continue
    if '<div class="card-unit">' in line:
        continue
    if '</div>' in line and ('c_h1' in str(new_lines[-5:]) or 'summary-card' in str(new_lines[-5:])): # heuristics to drop old cards
        # We will handle hero cards differently or just skip them since they are covered in the detailed rows
        pass

    new_lines.append(line)

# Close the bento-container at the end
new_lines.append('st.markdown("</div></div>", unsafe_allow_html=True)')

# A quick clean up of skipped blocks
final_lines = []
skip_block = False
for line in new_lines:
    if 'def render_infographic_row(' in line and 'icon, key_indicator' not in line: # old one
        skip_block = True
    if skip_block and 'def render_insight_box' in line:
        pass
    if skip_block and '# --- Data Loading ---' in line:
        skip_block = False
        
    if not skip_block:
        final_lines.append(line)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(final_lines))

print("Conversion complete!")
