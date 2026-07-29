import streamlit as st
import pandas as pd
import scipy.stats as stats
import textwrap

def render_spss_crosstab(df, x_options, y_options, title, hypothesis_text, key_prefix="", y_is_negative=False, interp_sig=None, interp_insig=None, exec_sig=None, exec_insig=None):
    """
    Menghasilkan komponen UI Streamlit berupa SPSS-Style Crosstabulation, 
    Dynamic Selectors, dan Executive Summary secara modular dan 100% konsisten.
    """
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(f"#### {title}")
    st.markdown(hypothesis_text)

    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        st.markdown("##### Variabel Independen (X)")
        x_col = st.selectbox("Pilih Indikator (X):", list(x_options.keys()), format_func=lambda x: x_options[x], key=f'x_{key_prefix}')

    with col_sel2:
        st.markdown("##### Variabel Dependen (Y)")
        y_col = st.selectbox("Pilih Indikator (Y):", list(y_options.keys()), format_func=lambda x: y_options[x], key=f'y_{key_prefix}')

    df_clean = df.dropna(subset=[x_col, y_col]).copy()
    
    # --- 1. Calculation (Binning) ---
    x_threshold = df_clean[x_col].median()
    y_threshold = df_clean[y_col].median()

    label_x_low = f"Rendah (<{x_threshold:,.1f})"
    label_x_high = f"Tinggi (≥{x_threshold:,.1f})"
    
    if y_is_negative:
        label_y_low = f"Rendah (<{y_threshold:,.1f})"
        label_y_high = f"Tinggi/Parah (≥{y_threshold:,.1f})"
    else:
        label_y_low = f"Kritis (<{y_threshold:,.1f})"
        label_y_high = f"Baik (≥{y_threshold:,.1f})"

    df_clean["X_Label"] = df_clean[x_col].apply(lambda x: label_x_high if x >= x_threshold else label_x_low)
    df_clean["Y_Label"] = df_clean[y_col].apply(lambda x: label_y_high if x >= y_threshold else label_y_low)

    cats_x = [label_x_low, label_x_high]
    cats_y = [label_y_low, label_y_high]
    crosstab = pd.crosstab(df_clean["X_Label"], df_clean["Y_Label"]).reindex(index=cats_x, columns=cats_y, fill_value=0)

    try:
        chi2, p, dof, expected = stats.chi2_contingency(crosstab)
        expected_df = pd.DataFrame(expected, index=crosstab.index, columns=crosstab.columns)
    except Exception:
        chi2, p, dof = 0, 1.0, 1
        expected_df = pd.DataFrame([[0,0],[0,0]], index=crosstab.index, columns=crosstab.columns)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("### Detail Uji Statistik (Chi-Square & Odds Ratio)")
    st.caption("Tabel-tabel di bawah ini adalah output standar SPSS yang menyajikan bukti statistik formal.")

    # --- A. Case Processing Summary ---
    st.markdown("##### Case Processing Summary")
    total_cases = len(df)
    valid_cases = len(df_clean)
    missing_cases = total_cases - valid_cases

    columns_case = pd.MultiIndex.from_product([["Cases"], ["Valid", "Missing", "Total"], ["N", "Percent"]])
    interaction_label = f"{x_options[x_col]} * {y_options[y_col]}"
    
    if total_cases > 0:
        row_data = [
            valid_cases, f"{valid_cases/total_cases*100:.1f}%",
            missing_cases, f"{missing_cases/total_cases*100:.1f}%",
            total_cases, "100.0%"
        ]
    else:
        row_data = [0, "0.0%", 0, "0.0%", 0, "0.0%"]

    case_summary = pd.DataFrame([row_data], index=[interaction_label], columns=columns_case)
    st.table(case_summary)

    # --- B. Crosstabulation ---
    st.markdown(f"##### {interaction_label} Crosstabulation")
    row_indices = []
    for x_cat in cats_x:
        row_indices.extend([(x_cat, "Count"), (x_cat, "Expected Count")])
    row_indices.extend([("Total", "Count"), ("Total", "Expected Count")])

    rows = []
    for x_cat in cats_x:
        counts = crosstab.loc[x_cat].tolist()
        exps = expected_df.loc[x_cat].tolist()
        rows.append(counts + [sum(counts)])
        rows.append([f"{v:.1f}" for v in exps] + [f"{sum(exps):.1f}"])

    total_counts = crosstab.sum().tolist()
    total_exps = expected_df.sum().tolist()
    rows.append(total_counts + [sum(total_counts)])
    rows.append([f"{v:.1f}" for v in total_exps] + [f"{sum(total_exps):.1f}"])

    multi_index = pd.MultiIndex.from_tuples(row_indices, names=[x_options[x_col], ""])
    spss_crosstab = pd.DataFrame(rows, index=multi_index, columns=cats_y + ["Total"])
    st.table(spss_crosstab)

    # --- C. Chi-Square Tests ---
    st.markdown("##### Chi-Square Tests")
    try:
        g, p_g, dof_g, exp_g = stats.chi2_contingency(crosstab, lambda_="log-likelihood")
    except:
        g, p_g = 0, 1.0
        
    x_codes = df_clean["X_Label"].replace({label_x_low: 0, label_x_high: 1})
    y_codes = df_clean["Y_Label"].replace({label_y_low: 1, label_y_high: 0})
    
    if len(df_clean) > 2 and x_codes.nunique() > 1 and y_codes.nunique() > 1:
        try:
            r, p_corr = stats.pearsonr(x_codes, y_codes)
            lbl_val = (valid_cases - 1) * (r**2)
        except:
            r, p_corr, lbl_val = 0, 1.0, 0
    else:
        r, p_corr, lbl_val = 0, 1.0, 0

    p_fmt = "< 0.001" if p < 0.001 else f"{p:.4f}"
    p_tbl = "< 0.001" if p < 0.001 else f"{p:.3f}"
    p_g_tbl = "< 0.001" if p_g < 0.001 else f"{p_g:.3f}"
    p_corr_tbl = "< 0.001" if p_corr < 0.001 else f"{p_corr:.3f}"

    chi_data = [
        [f"{chi2:.3f}", str(dof), p_tbl],
        [f"{g:.3f}", str(dof), p_g_tbl],
        [f"{lbl_val:.3f}", "1", p_corr_tbl],
        [str(valid_cases), "", ""]
    ]
    chi_df = pd.DataFrame(chi_data, index=["Pearson Chi-Square", "Likelihood Ratio", "Linear-by-Linear Association", "N of Valid Cases"], columns=["Value", "df", "Asymp. Sig. (2-sided)"])
    st.markdown(f"**{interaction_label}**")
    st.table(chi_df)

    # --- D. Hypothesis & Risk Summary ---
    st.markdown("### Ringkasan Uji Hipotesis")
    is_significant = p < 0.05
    status_text = "SIGNIFIKAN (Ada Hubungan)" if is_significant else "TIDAK SIGNIFIKAN (Arah Terlihat)"
    order_color = "#4CAF50" if is_significant else "#F44336" 
    bg_color = "rgba(76, 175, 80, 0.1)" if is_significant else "rgba(244, 67, 54, 0.1)"

    try:
        if y_is_negative:
            a = crosstab.loc[label_x_high, label_y_high]
            b = crosstab.loc[label_x_high, label_y_low]
            c = crosstab.loc[label_x_low, label_y_high]
            d = crosstab.loc[label_x_low, label_y_low]
        else:
            a = crosstab.loc[label_x_high, label_y_low]
            b = crosstab.loc[label_x_high, label_y_high]
            c = crosstab.loc[label_x_low, label_y_low]
            d = crosstab.loc[label_x_low, label_y_high]
        odds_ratio = (a * d) / (b * c) if (b * c) > 0 else 0
    except:
        odds_ratio = 0

    col_res1, col_res2 = st.columns([1, 1.5])
    with col_res1:
        st.markdown(f'''
        <div style="border: 2px solid {order_color}; padding: 15px; border-radius: 5px; background-color: {bg_color}; margin-bottom: 10px;">
            <h4 style="color: {order_color}; margin: 0 0 10px 0; text-transform: uppercase;">Result: {status_text}</h4>
            <p style="margin: 0; font-family: monospace;">
                P-Value    : {p_fmt}<br>
                Chi-Square : {chi2:.3f}<br>
                df         : {dof}
            </p>
        </div>
        ''', unsafe_allow_html=True)
        if odds_ratio == 0:
            st.markdown("**Odds Ratio (Risk Estimate):** `Infinite`")
        else:
            st.markdown(f"**Odds Ratio (Risk Estimate):** `{odds_ratio:.3f}`")

    with col_res2:
        if is_significant:
            text_to_show = interp_sig if interp_sig else "Analisis ini didasarkan pada metode Chi-Square. Nilai Odds Ratio menunjukkan rasio peluang antara kelompok Tinggi (X) dan Rendah (X) terhadap outcome variabel Y secara signifikan."
        else:
            text_to_show = interp_insig if interp_insig else "Meskipun tidak signifikan secara statistik (P ≥ 0.05), analisis Chi-Square tetap menyajikan arah distribusi probabilitas antar kelompok variabel."
            
        st.markdown(f'''
        <div style="background:#1E1E1E; padding:14px; border-radius:10px; border-left:5px solid {order_color}; height: 100%;">
            <b>Statistik Interpretasi:</b><br><br>
            {text_to_show}
        </div>
        ''', unsafe_allow_html=True)

    # --- E. Executive Summary of All Combinations ---
    st.markdown("---")
    st.markdown("### Ringkasan Seluruh Skenario")
    summary_data = []
    for k_x, v_x in x_options.items():
        for k_y, v_y in y_options.items():
            df_temp = df.dropna(subset=[k_x, k_y]).copy()
            if len(df_temp) == 0: continue
            med_x = df_temp[k_x].median()
            med_y = df_temp[k_y].median()
            lbl_x_h = f"Tinggi (≥{med_x:,.1f})"
            lbl_x_l = f"Rendah (<{med_x:,.1f})"
            if y_is_negative:
                lbl_y_l = f"Rendah (<{med_y:,.1f})"
                lbl_y_h = f"Tinggi/Parah (≥{med_y:,.1f})"
            else:
                lbl_y_h = f"Baik (≥{med_y:,.1f})"
                lbl_y_l = f"Kritis (<{med_y:,.1f})"
                
            s_x = df_temp[k_x].apply(lambda val: lbl_x_h if val >= med_x else lbl_x_l)
            s_y = df_temp[k_y].apply(lambda val: lbl_y_h if val >= med_y else lbl_y_l)
            ct = pd.crosstab(s_x, s_y).reindex(index=[lbl_x_l, lbl_x_h], columns=[lbl_y_l, lbl_y_h], fill_value=0)
            try:
                c2_val, pv_val, dof_val, exp_val = stats.chi2_contingency(ct)
            except:
                c2_val, pv_val, dof_val = 0, 1, 0
            try:
                if y_is_negative:
                    aa = ct.loc[lbl_x_h, lbl_y_h]
                    bb = ct.loc[lbl_x_h, lbl_y_l]
                    cc = ct.loc[lbl_x_l, lbl_y_h]
                    dd = ct.loc[lbl_x_l, lbl_y_l]
                else:
                    aa = ct.loc[lbl_x_h, lbl_y_l]
                    bb = ct.loc[lbl_x_h, lbl_y_h]
                    cc = ct.loc[lbl_x_l, lbl_y_l]
                    dd = ct.loc[lbl_x_l, lbl_y_h]
                or_v = (aa * dd) / (bb * cc) if (bb * cc) > 0 else 0
            except:
                or_v = 0
            sig_status = "🟢 SIGNIFIKAN" if pv_val < 0.05 else "🔴 TIDAK SIGNIFIKAN"
            pv_disp = "< 0.001" if pv_val < 0.001 else f"{pv_val:.3f}"
            summary_data.append({
                "X": v_x, "Y": v_y, "Chi-Square": f"{c2_val:.3f}",
                "P-Value": pv_disp, "Odds Ratio": f"{or_v:.2f}",
                "Status": sig_status
            })

    if summary_data:
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)
        
        sig_count = sum(1 for row in summary_data if "🟢 SIGNIFIKAN" in row["Status"])
        total_scenarios = len(summary_data)
        
        if sig_count > 0:
            exec_narrative = exec_sig if exec_sig else f"Dari {total_scenarios} skenario pengujian, terdapat {sig_count} skenario yang terbukti SIGNIFIKAN."
            bg_color_sum = "rgba(229, 57, 53, 0.15)"
            border_color_sum = "#E53935"
        else:
            exec_narrative = exec_insig if exec_insig else f"Dari {total_scenarios} skenario pengujian, seluruhnya menunjukkan status TIDAK SIGNIFIKAN."
            bg_color_sum = "rgba(255, 152, 0, 0.15)"
            border_color_sum = "#FF9800"

        st.markdown(f'''
        <div style="background-color: {bg_color_sum}; padding:18px; border-radius:8px; border-left:6px solid {border_color_sum}; margin-top: 15px; margin-bottom: 25px;">
            <b style="color: {border_color_sum}; font-size: 1.05rem;">Pembedahan Realitas Ekologis:</b><br><br>
            <div style="color: #E0E0E0; font-size: 0.95rem; line-height: 1.6;">
        {exec_narrative}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    return x_col, y_col, df_clean
