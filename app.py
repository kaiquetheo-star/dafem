# -*- coding: utf-8 -*-
"""
DaFem — Dashboard de Análise de Feminicídio
Equipe: Squad de Dados — Fora FB! · Dados: FBSP + IBGE
Deploy: https://github.com/kaiquetheo-star/dafem
"""
import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ══════════════════════════════════ CONFIG ══════════════════════════════════

st.set_page_config(
    page_title="DaFem — Feminicídio no Brasil",
    page_icon="🕯️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════ DESIGN TOKENS ═══════════════════════════

BG = "#0D0F12"
SURFACE = "#16181D"
BORDER = "#26292F"
ACCENT = "#9D70F5"
ACCENT_DEEP = "#6B3FD4"
CORAL = "#FF6B6B"
AMBER = "#FFB347"
POSITIVE = "#34d399"
TEXT = "#E8EAEF"
MUTED = "#71767F"
FONT_DISPLAY = "Space Grotesk"
FONT_BODY = "Inter"

# Back-compat aliases used in chart colors
CARD = SURFACE
ACCENT_DIM = ACCENT_DEEP
ALERT = AMBER
DANGER = CORAL

PLOTLY_LAYOUT = dict(
    paper_bgcolor=BG,
    plot_bgcolor=BG,
    font=dict(family=f"{FONT_BODY}, sans-serif", size=13, color=MUTED),
    margin=dict(l=48, r=24, t=48, b=40),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        font=dict(family=f"{FONT_BODY}, sans-serif", size=12, color=MUTED),
        bgcolor="rgba(0,0,0,0)",
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.03)",
        zeroline=False,
        showline=False,
        tickfont=dict(size=12, color=MUTED),
        title_font=dict(size=12, color=MUTED),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.03)",
        zeroline=False,
        showline=False,
        tickfont=dict(size=12, color=MUTED),
        title_font=dict(size=12, color=MUTED),
    ),
    hoverlabel=dict(
        bgcolor=SURFACE,
        bordercolor=BORDER,
        font=dict(family=f"{FONT_BODY}, sans-serif", color=TEXT, size=13),
    ),
    hovermode="closest",
)

# Style-only payload for st.html (event container). Markdown strips <style> and
# dumps the rules as visible text — never inject CSS via st.markdown.
CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {{
    --bg: {BG};
    --surface: {SURFACE};
    --border: {BORDER};
    --accent: {ACCENT};
    --accent-deep: {ACCENT_DEEP};
    --coral: {CORAL};
    --amber: {AMBER};
    --text: {TEXT};
    --muted: {MUTED};
    --font-display: '{FONT_DISPLAY}', system-ui, sans-serif;
    --font-body: '{FONT_BODY}', system-ui, sans-serif;
}}

@keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to {{ opacity: 1; transform: none; }}
}}

.stApp {{
    background: var(--bg);
    font-family: var(--font-body);
    color: var(--text);
}}

#MainMenu, header, footer {{
    visibility: hidden;
}}

div[data-testid="stAppViewContainer"] > .main .block-container {{
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
    max-width: 1200px;
}}

/* ── Sidebar ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: var(--surface);
    border-right: 1px solid var(--border);
}}

section[data-testid="stSidebar"] > div:first-child {{
    padding-top: 0.5rem;
}}

section[data-testid="stSidebar"] * {{
    font-family: var(--font-body);
}}

.nav-brand {{
    padding: 20px 8px 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 12px;
}}

.nav-brand .brand-mark {{
    display: flex;
    align-items: baseline;
    gap: 8px;
}}

.nav-brand h1 {{
    font-family: var(--font-display);
    font-size: 26px;
    font-weight: 700;
    color: var(--text);
    margin: 0;
    letter-spacing: -0.4px;
}}

.nav-brand .brand-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent);
    display: inline-block;
    flex-shrink: 0;
    margin-bottom: 4px;
}}

.nav-brand p {{
    font-size: 12px;
    color: var(--muted);
    margin: 8px 0 0;
    line-height: 1.45;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] {{
    gap: 4px;
    padding: 0 4px;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 10px 14px !important;
    margin: 0 !important;
    transition: background 0.15s ease, border-color 0.15s ease;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
    background: rgba(157, 112, 245, 0.08);
    border-color: rgba(157, 112, 245, 0.2);
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
    background: rgba(157, 112, 245, 0.12);
    border-color: rgba(157, 112, 245, 0.35);
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label p {{
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: var(--text) !important;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {{
    color: var(--accent) !important;
    font-weight: 600 !important;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {{
    display: none;
}}

.nav-sources {{
    padding: 16px 12px;
    border-top: 1px solid var(--border);
    margin-top: 24px;
    font-size: 11px;
    color: var(--muted);
    line-height: 1.55;
}}

.nav-sources strong {{
    color: var(--text);
    font-weight: 600;
}}

/* ── Hero ─────────────────────────────────────────────────── */
.hero {{
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(157, 112, 245, 0.14), transparent 55%),
        radial-gradient(ellipse 50% 40% at 90% 100%, rgba(107, 63, 212, 0.08), transparent 50%),
        var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 36px 40px 32px;
    margin-bottom: 20px;
    animation: slideUp 0.45s ease-out both;
}}

.hero-label {{
    font-family: var(--font-body);
    font-size: 13px;
    font-weight: 500;
    color: var(--muted);
    margin-bottom: 8px;
}}

.hero-value {{
    font-family: var(--font-display);
    font-size: 64px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    line-height: 1;
    letter-spacing: -1.5px;
    color: var(--coral);
    margin: 0 0 12px;
}}

.hero-context {{
    font-family: var(--font-body);
    font-size: 16px;
    color: var(--text);
    line-height: 1.5;
    max-width: 560px;
    margin: 0;
}}

.hero-context em {{
    font-style: normal;
    color: var(--coral);
    font-weight: 600;
}}

/* ── Metric cards ─────────────────────────────────────────── */
.metric-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
    animation: slideUp 0.4s ease-out both;
}}

.metric-card.tall {{
    padding: 28px 22px;
}}

.metric-card.compact {{
    padding: 16px 20px;
}}

.metric-card:nth-child(1) {{ animation-delay: 0.05s; }}
.metric-card:nth-child(2) {{ animation-delay: 0.1s; }}
.metric-card:nth-child(3) {{ animation-delay: 0.15s; }}
.metric-card:nth-child(4) {{ animation-delay: 0.2s; }}

.metric-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
}}

.metric-card.violet::before {{ background: var(--accent); }}
.metric-card.orange::before,
.metric-card.amber::before {{ background: var(--amber); }}
.metric-card.red::before,
.metric-card.coral::before {{ background: var(--coral); }}
.metric-card.green::before {{ background: {POSITIVE}; }}

.metric-label {{
    font-family: var(--font-body);
    font-size: 12px;
    font-weight: 500;
    color: var(--muted);
    margin-bottom: 8px;
    line-height: 1.35;
}}

.metric-value {{
    font-family: var(--font-display);
    font-size: 36px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
    color: var(--text);
    letter-spacing: -0.6px;
}}

.metric-card.tall .metric-value {{
    font-size: 42px;
}}

.metric-delta {{
    font-family: var(--font-body);
    font-size: 13px;
    font-weight: 500;
    margin-top: 6px;
}}

.metric-delta.up {{ color: var(--coral); }}
.metric-delta.down {{ color: {POSITIVE}; }}
.metric-delta.neutral {{ color: var(--muted); }}

/* ── Section headers ──────────────────────────────────────── */
.section-title {{
    font-family: var(--font-display);
    font-size: 26px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.4px;
    margin: 40px 0 8px 0;
    line-height: 1.25;
}}

.section-sub {{
    font-family: var(--font-body);
    font-size: 15px;
    color: var(--muted);
    margin-bottom: 20px;
    line-height: 1.55;
    max-width: 720px;
}}

.rank-label {{
    font-family: var(--font-body);
    font-size: 13px;
    font-weight: 600;
    color: var(--muted);
    margin: 0 0 10px;
}}

/* ── Finding callout ──────────────────────────────────────── */
.finding {{
    background: rgba(157, 112, 245, 0.08);
    border: 1px solid rgba(157, 112, 245, 0.22);
    border-left: 3px solid var(--accent);
    border-radius: 0 12px 12px 0;
    padding: 20px 24px;
    margin: 20px 0;
    font-family: var(--font-body);
    font-size: 15px;
    color: var(--text);
    line-height: 1.65;
    animation: slideUp 0.4s ease-out 0.12s both;
}}

.finding.alert {{
    background: rgba(255, 107, 107, 0.06);
    border-color: rgba(255, 107, 107, 0.25);
    border-left-color: var(--coral);
}}

.finding strong {{
    color: var(--accent);
    font-weight: 600;
}}

.finding.alert strong {{
    color: var(--coral);
}}

/* ── Stat bar ─────────────────────────────────────────────── */
.stat-bar {{
    display: flex;
    gap: 1px;
    background: var(--border);
    border-radius: 12px;
    overflow: hidden;
    margin: 16px 0 8px;
}}

.stat-item {{
    flex: 1;
    background: var(--surface);
    padding: 18px 16px;
    text-align: center;
}}

.stat-item .num {{
    font-family: var(--font-display);
    font-size: 26px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    display: block;
    letter-spacing: -0.4px;
}}

.stat-item .lbl {{
    font-family: var(--font-body);
    font-size: 11px;
    color: var(--muted);
    display: block;
    margin-top: 6px;
    line-height: 1.35;
}}

/* ── Data table ───────────────────────────────────────────── */
.dataframe {{
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}}

.dataframe thead {{
    background: var(--surface);
}}

.dataframe th {{
    font-family: var(--font-body);
    font-weight: 600;
    color: var(--text);
    font-size: 12px;
}}

.dataframe td {{
    font-family: var(--font-body);
    font-size: 13px;
    color: var(--text);
}}

/* ── Footer ───────────────────────────────────────────────── */
.dafem-footer {{
    border-top: 1px solid var(--border);
    padding: 24px 0 8px;
    margin-top: 48px;
    font-family: var(--font-body);
    font-size: 12px;
    color: var(--muted);
    line-height: 1.6;
}}

.dafem-footer strong {{
    color: var(--text);
    font-weight: 600;
}}

/* ── Plotly ───────────────────────────────────────────────── */
.js-plotly-plot .plotly .modebar {{
    background: transparent !important;
}}

.js-plotly-plot .plotly .modebar-btn path {{
    fill: var(--muted) !important;
}}

/* ── Mobile ───────────────────────────────────────────────── */
@media (max-width: 768px) {{
    .hero {{
        padding: 28px 22px;
    }}
    .hero-value {{
        font-size: 48px;
    }}
    .hero-context {{
        font-size: 14px;
    }}
    .metric-card {{
        margin-bottom: 8px;
    }}
    .metric-value,
    .metric-card.tall .metric-value {{
        font-size: 28px;
    }}
    .section-title {{
        font-size: 22px;
        margin-top: 28px;
    }}
    .stat-bar {{
        flex-direction: column;
        gap: 0;
    }}
    .stat-item {{
        border-bottom: 1px solid var(--border);
        text-align: left;
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 12px;
        padding: 14px 18px;
    }}
    .stat-item .num {{
        font-size: 22px;
    }}
    .stat-item .lbl {{
        margin-top: 0;
        text-align: right;
    }}
    .stat-item:last-child {{
        border-bottom: none;
    }}
}}

@media (prefers-reduced-motion: reduce) {{
    .hero,
    .metric-card,
    .finding {{
        animation: none !important;
    }}
}}
</style>
"""


def inject_css():
    """Inject CSS via st.html so <style> is not stripped into visible text."""
    if hasattr(st, "html"):
        st.html(CSS)
    else:
        # Last resort for Streamlit <1.33 — may still sanitize on some builds
        st.markdown(CSS, unsafe_allow_html=True)


# ══════════════════════════════════ DATA ══════════════════════════════════

@st.cache_data
def load_data():
    d = {}
    base = os.path.dirname(os.path.abspath(__file__))

    d["painel"] = pd.read_csv(os.path.join(base, "painel_feminicidio_uf_2016_2025.csv"))
    d["brasil"] = d["painel"][d["painel"].uf == "Brasil"]
    d["ufs"] = d["painel"][d["painel"].uf != "Brasil"]

    for key, fname in [("desemp", "b1_desemprego_mulheres_uf.csv"),
                       ("informal", "b3_informalidade_mulheres_uf.csv"),
                       ("mpu", "b4_medidas_protetivas_uf.csv"),
                       ("matriz", "matriz_variaveis_uf_2023_25.csv")]:
        path = os.path.join(base, fname)
        d[key] = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()
    return d


DATA = load_data()

# ══════════════════════════════════ HELPERS ════════════════════════════════


def hero(value, label, context):
    return f"""
    <div class="hero">
        <div class="hero-label">{label}</div>
        <div class="hero-value">{value}</div>
        <p class="hero-context">{context}</p>
    </div>
    """


def metric(label, value, delta="", delta_type="neutral", color="violet", size=""):
    dt = {"up": "↑", "down": "↓", "neutral": ""}
    dclass = delta_type if delta_type in ("up", "down", "neutral") else "neutral"
    size_cls = f" {size}" if size in ("tall", "compact") else ""
    delta_html = ""
    if delta:
        delta_html = f'<div class="metric-delta {dclass}">{dt[dclass]} {delta}</div>'
    return f"""
    <div class="metric-card {color}{size_cls}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """


def finding(text, variant=""):
    cls = f"finding {variant}".strip()
    return f'<div class="{cls}">{text}</div>'


def section(title, subtitle=""):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)


def style_plotly(fig, **overrides):
    layout = {**PLOTLY_LAYOUT, **overrides}
    fig.update_layout(**layout)
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.03)",
        zeroline=False,
        showline=False,
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.03)",
        zeroline=False,
        showline=False,
    )
    return fig


def chart(fig, **kwargs):
    """Plotly chart with stretch width; falls back for older Streamlit."""
    try:
        st.plotly_chart(fig, width="stretch", **kwargs)
    except TypeError:
        st.plotly_chart(fig, use_container_width=True, **kwargs)


def table(df, **kwargs):
    try:
        st.dataframe(df, width="stretch", hide_index=True, **kwargs)
    except TypeError:
        st.dataframe(df, use_container_width=True, hide_index=True, **kwargs)


def footer():
    st.markdown("""
    <div class="dafem-footer">
        <strong>DaFem</strong> · Squad de Dados — Fora FB! · Outubro 2026 ·
        Fontes: FBSP 2018–2026 + IBGE/SIDRA · Correlação ≠ causalidade
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════ SIDEBAR ════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class="nav-brand">
        <div class="brand-mark">
            <span class="brand-dot"></span>
            <h1>DaFem</h1>
        </div>
        <p>Observatório de feminicídio<br>Brasil · 2016–2025</p>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Navegação",
        ["Visão Geral", "Por Estado", "Variáveis", "Sobre"],
        label_visibility="collapsed",
    )

    st.markdown("""
    <div class="nav-sources">
        <strong>Fontes</strong><br>
        Anuário FBSP 2018–2026<br>
        IBGE/SIDRA PNAD Contínua<br>
        Squad de Dados — Fora FB!<br>
        <span style="opacity:0.65">Correlação ≠ causalidade</span>
    </div>
    """, unsafe_allow_html=True)

inject_css()

# ══════════════════════════════════ PÁGINA: VISÃO GERAL ═════════════════════

if pagina == "Visão Geral":
    br = DATA["brasil"]
    fem25 = br[br.ano == 2025].prop_pct.iloc[0]
    fem16 = br[br.ano == 2016].prop_pct.iloc[0]

    st.markdown(hero(
        "1.571",
        "Feminicídios registrados em 2025",
        "Em um ano, <em>+4,5%</em> frente a 2024. Em uma década, o reconhecimento "
        "legal mudou o mapa — e o número continua subindo."
    ), unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.15, 1, 1])
    with col1:
        st.markdown(metric(
            "Homicídios de mulheres em 2025", "3.539",
            "−5,1% vs 2024", "down", "green", "tall"
        ), unsafe_allow_html=True)
    with col2:
        st.markdown(metric(
            "Classificados como feminicídio", f"{fem25:.0f}%",
            f"+{fem25 - fem16:.0f}pp desde 2016", "neutral", "violet"
        ), unsafe_allow_html=True)
    with col3:
        st.markdown(metric(
            "MPUs descumpridas em 2025", "132.025",
            "70 mortas com MPU ativa", "neutral", "amber"
        ), unsafe_allow_html=True)

    st.markdown(finding("""
        <strong>A contradição central:</strong> o total de mulheres assassinadas <strong>cai 17%</strong> desde 2016,
        mas o feminicídio <strong>sobe 69%</strong>. Isso acontece porque a parcela de homicídios
        classificados como feminicídio <strong>dobrou</strong> (22% → 44%) — a Lei 13.104/2015 levou anos
        para ser incorporada pelos estados. A alta é em parte reconhecimento, não só violência.
    """, "alert"), unsafe_allow_html=True)

    section(
        "Homicídios caem. Feminicídio sobe.",
        "Série nacional com faixas de governo. O número sobe atravessando três administrações — com desaceleração em cada mandato.",
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=br.ano, y=br.hom_abs, name="Total de homicídios de mulheres",
        mode="lines",
        line=dict(color=MUTED, width=1.5),
        hovertemplate="<b>%{x}</b><br>Total: %{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=br.ano, y=br.fem_abs, name="Feminicídios",
        mode="lines+markers",
        line=dict(color=ACCENT, width=3.5),
        marker=dict(size=6, color=ACCENT, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Feminicídios: %{y:,.0f}<extra></extra>",
    ))
    for x0, x1, nome in [(2015.5, 2018.5, "Temer"), (2018.5, 2022.5, "Bolsonaro"), (2022.5, 2025.5, "Lula")]:
        fig.add_vrect(x0=x0, x1=x1, fillcolor=ACCENT_DEEP, opacity=0.03, line_width=0)
        fig.add_annotation(
            x=(x0 + x1) / 2, y=4800, text=nome, showarrow=False,
            font=dict(size=11, color=MUTED, family=f"{FONT_BODY}, sans-serif"),
        )
    fig.update_layout(height=420, yaxis_title="Vítimas", hovermode="x unified")
    chart(style_plotly(fig))

    section(
        "A classificação dobrou",
        "Percentual de homicídios de mulheres registrados como feminicídio. O salto reflete a adoção gradual da Lei 13.104/2015 pelos estados.",
    )

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=br.ano, y=[0] * len(br), mode="lines",
        line=dict(width=0), showlegend=False, hoverinfo="skip",
    ))
    fig2.add_trace(go.Scatter(
        x=br.ano, y=br.prop_pct, mode="lines",
        name="% feminicídio",
        fill="tonexty",
        fillcolor="rgba(157,112,245,0.15)",
        line=dict(color=ACCENT, width=2.5),
        hovertemplate="<b>%{x}</b><br>%{y:.0f}% classificados<extra></extra>",
    ))
    fig2.update_layout(
        height=300,
        yaxis_title="",
        yaxis_ticksuffix="%",
        showlegend=False,
    )
    chart(style_plotly(fig2))

    section(
        "Raça é estrutura, não conjuntura",
        "Percentual de vítimas por cor/raça nos anos com dado disponível. Mulheres negras são ~56% da população feminina e 60–67% das vítimas, sempre.",
    )

    st.markdown(f"""
    <div class="stat-bar">
        <div class="stat-item"><span class="num" style="color:{ACCENT}">61%</span><span class="lbl">negras (2017–18)</span></div>
        <div class="stat-item"><span class="num" style="color:{ACCENT}">67%</span><span class="lbl">negras (2019)</span></div>
        <div class="stat-item"><span class="num" style="color:{ACCENT}">62%</span><span class="lbl">negras (2020–21)</span></div>
        <div class="stat-item"><span class="num" style="color:{ACCENT}">64%</span><span class="lbl">negras (2023–24)</span></div>
        <div class="stat-item"><span class="num" style="color:{ACCENT}">65%</span><span class="lbl">negras (2025)</span></div>
        <div class="stat-item" style="border-left:1px solid {BORDER}">
            <span class="num" style="color:{MUTED}">56%</span><span class="lbl">da pop. feminina (IBGE)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    section(
        "A proteção que não protege",
        "Cinco avanços legislativos em 17 anos. Mas 1 em cada 4 medidas protetivas é descumprida.",
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(metric(
            "MPUs concedidas (2024)", "555.001", "", "neutral", "violet", "compact"
        ), unsafe_allow_html=True)
    with col_b:
        st.markdown(metric(
            "Descumpridas (2025)", "132.025", "1 em cada 4", "neutral", "amber", "compact"
        ), unsafe_allow_html=True)
    with col_c:
        st.markdown(metric(
            "Mortas com MPU ativa", "70", "em 2025", "neutral", "coral", "tall"
        ), unsafe_allow_html=True)

    st.markdown(finding("""
        <strong>Marco legislativo:</strong> Maria da Penha (2006) → Feminicídio é crime (2015) →
        MPU pela polícia (2019) → Violência psicológica (2021) → Crimes Hediondos (2023).
        A lei avançou 5 vezes. A execução continua falhando.
    """), unsafe_allow_html=True)

# ══════════════════════════════════ PÁGINA: POR ESTADO ═════════════════════

elif pagina == "Por Estado":
    fem = DATA["ufs"]

    section(
        "Padrão Norte e Centro-Oeste",
        "Taxa por 100 mil mulheres. Acre, Rondônia e Mato Grosso lideram. Cada célula é um estado-ano.",
    )

    w = fem.pivot_table(index="uf", columns="ano", values="fem_taxa")
    years = list(w.columns)
    ufs = list(w.index)
    z = w.values
    text = [[f"{v:.1f}" if pd.notna(v) else "" for v in row] for row in z]

    fig3 = go.Figure(data=go.Heatmap(
        z=z,
        x=years,
        y=ufs,
        text=text,
        texttemplate="%{text}",
        textfont=dict(size=10, color=TEXT, family=f"{FONT_BODY}, sans-serif"),
        colorscale=[
            [0, SURFACE],
            [0.5, ACCENT_DEEP],
            [1, ACCENT],
        ],
        hovertemplate="<b>%{y}</b> · %{x}<br>Taxa: %{z:.2f} /100k<extra></extra>",
        colorbar=dict(
            title=dict(text="Taxa /100k", font=dict(size=11, color=MUTED)),
            thickness=12,
            len=0.8,
            tickfont=dict(size=11, color=MUTED),
            bgcolor="rgba(0,0,0,0)",
        ),
    ))
    fig3.update_layout(
        height=620,
        xaxis_title="",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
    )
    chart(style_plotly(fig3, showlegend=False))

    uf_sel = st.selectbox("Escolha um estado:", sorted(fem.uf.unique()))
    sub = fem[fem.uf == uf_sel].sort_values("ano")

    col1, col2 = st.columns(2)
    with col1:
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=sub.ano, y=sub.fem_abs,
            marker_color=[ACCENT if a == 2025 else ACCENT_DEEP for a in sub.ano],
            hovertemplate="<b>%{x}</b><br>%{y} feminicídios<extra></extra>",
        ))
        fig4.update_layout(
            height=320,
            title=dict(
                text=f"Feminicídios — {uf_sel}",
                font=dict(family=f"{FONT_DISPLAY}, sans-serif", size=16, color=TEXT),
            ),
            showlegend=False,
        )
        chart(style_plotly(fig4))
    with col2:
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=sub.ano, y=sub.fem_taxa, mode="lines+markers",
            line=dict(color=ACCENT, width=2.5),
            marker=dict(size=6, color=ACCENT),
            hovertemplate="<b>%{x}</b><br>%{y:.2f} por 100k<extra></extra>",
        ))
        fig5.update_layout(
            height=320,
            title=dict(
                text=f"Taxa por 100k — {uf_sel}",
                font=dict(family=f"{FONT_DISPLAY}, sans-serif", size=16, color=TEXT),
            ),
            showlegend=False,
        )
        chart(style_plotly(fig5))

    section("Ranking 2025", "Maiores e menores taxas por 100 mil mulheres.")

    rank = fem[fem.ano == 2025].sort_values("fem_taxa", ascending=False)
    col_top, col_bottom = st.columns(2)
    with col_top:
        st.markdown('<p class="rank-label">Maiores taxas</p>', unsafe_allow_html=True)
        top10 = rank.head(10)[["uf", "fem_abs", "fem_taxa"]].copy()
        top10.columns = ["Estado", "Casos", "Taxa/100k"]
        table(top10)
    with col_bottom:
        st.markdown('<p class="rank-label">Menores taxas</p>', unsafe_allow_html=True)
        bottom10 = rank.tail(10)[["uf", "fem_abs", "fem_taxa"]].copy()
        bottom10.columns = ["Estado", "Casos", "Taxa/100k"]
        table(bottom10)

    section(
        "Quem puxou o aumento de 2025",
        "Variação absoluta de feminicídios entre 2024 e 2025. SP, Pará e Pernambuco lideram.",
    )

    w_d = fem.pivot_table(index="uf", columns="ano", values="fem_abs")
    w_d["delta"] = w_d[2025] - w_d[2024]
    top_up = w_d.sort_values("delta", ascending=False).head(10).reset_index()
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(
        x=top_up["delta"], y=top_up["uf"], orientation="h",
        marker_color=[CORAL if d > 0 else POSITIVE for d in top_up["delta"]],
        hovertemplate="<b>%{y}</b><br>%{x:+d} casos<extra></extra>",
    ))
    fig6.update_layout(height=400, showlegend=False, yaxis={"categoryorder": "total ascending"})
    chart(style_plotly(fig6))

# ══════════════════════════════════ PÁGINA: VARIÁVEIS ═════════════════════

elif pagina == "Variáveis":
    matriz = DATA["matriz"]

    section(
        "Desemprego NÃO explica o mapa",
        "Testamos 4 variáveis contra a taxa de feminicídio nos 27 estados (Spearman, média 2023–25). O resultado inverte a narrativa.",
    )

    st.markdown(finding("""
        <strong>A descoberta central:</strong> variáveis econômicas NÃO explicam o mapa.
        Desemprego feminino tem correlação <strong>negativa</strong> (ρ=−0,43) — mais desemprego,
        <strong>menos</strong> feminicídio. Já o descumprimento de MPU tem a correlação mais
        forte da matriz (ρ=+0,46): onde a proteção falha, mais mulheres morrem.
    """), unsafe_allow_html=True)

    if not matriz.empty:
        var_map = {
            "desemp": ("Desemprego feminino (%)", "−0,43*", "Negativa: mais desemprego = menos feminicídio"),
            "informal": ("Informalidade (%)", "−0,25", "Não significante (proxy Bolsa Família)"),
            "mpu_conc": ("MPU concedida /100k", "+0,45*", "Positiva: sistema reage, não previne"),
            "descump": ("Descumprimento MPU /100k", "+0,46*", "Positiva: onde mais MPU falha, mais mortes"),
        }

        var_sel = st.selectbox(
            "Variável explicativa:",
            list(var_map.keys()),
            format_func=lambda k: var_map[k][0],
        )

        if var_sel in matriz.columns:
            fig7 = go.Figure()
            fig7.add_trace(go.Scatter(
                x=matriz[var_sel],
                y=matriz["fem_taxa"],
                mode="markers+text",
                text=matriz["uf"],
                textposition="top center",
                textfont=dict(size=10, color=MUTED, family=f"{FONT_BODY}, sans-serif"),
                marker=dict(
                    size=11,
                    color=matriz["fem_taxa"],
                    colorscale=[
                        [0, MUTED],
                        [0.45, "#5a5f6a"],
                        [0.7, ACCENT_DEEP],
                        [1, ACCENT],
                    ],
                    line=dict(width=0),
                    showscale=False,
                ),
                customdata=matriz["uf"],
                hovertemplate="<b>%{customdata}</b><br>x: %{x:.1f}<br>Taxa: %{y:.2f}/100k<extra></extra>",
            ))
            fig7.update_layout(
                height=480,
                xaxis_title=var_map[var_sel][0],
                yaxis_title="Taxa de feminicídio /100k",
                showlegend=False,
            )
            chart(style_plotly(fig7))

        rho_label, rho_val, rho_desc = var_map[var_sel]
        st.markdown(f"""
        <div class="metric-card violet">
            <div class="metric-label">ρ Spearman — {rho_label}</div>
            <div class="metric-value">{rho_val}</div>
            <div class="metric-delta neutral">{rho_desc}</div>
        </div>
        """, unsafe_allow_html=True)

        section("Matriz completa", "Todas as correlações testadas, média 2023–25, n=27 UFs.")
        st.markdown(f"""
        <div class="stat-bar">
            <div class="stat-item">
                <span class="num" style="color:{CORAL}">−0,43*</span>
                <span class="lbl">Desemprego<br>(p=0,017)</span>
            </div>
            <div class="stat-item">
                <span class="num" style="color:{MUTED}">−0,25</span>
                <span class="lbl">Informalidade<br>(p=0,20)</span>
            </div>
            <div class="stat-item">
                <span class="num" style="color:{ACCENT}">+0,45*</span>
                <span class="lbl">MPU concedida<br>(p=0,015)</span>
            </div>
            <div class="stat-item">
                <span class="num" style="color:{ACCENT}">+0,46*</span>
                <span class="lbl">Descumprimento<br>(p=0,010)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(finding("""
            <strong>Inter-correlação reveladora:</strong> estados com mais informalidade concedem
            <strong>menos</strong> MPU (ρ=−0,59). A cadeia é: menos capacidade institucional →
            menos proteção concedida → mais descumprimento → mais mortes.
            O eixo não é "pobreza → violência" — é <strong>capacidade institucional</strong>.
        """), unsafe_allow_html=True)

# ══════════════════════════════════ PÁGINA: SOBRE ══════════════════════════

elif pagina == "Sobre":
    section("DaFem — Dashboard de Análise de Feminicídio")
    st.markdown("""
    <div class="section-sub" style="margin-top:4px">
        Ferramenta de dados abertos para jornalismo e advocacy. Análise completa da série
        histórica de feminicídio no Brasil (2016–2025) com painel estadual, correlações
        socioeconômicas e recorte racial.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(finding("""
        <strong>Equipe:</strong> Squad de Dados — Fora FB!<br>
        <strong>Metodologia:</strong> Correlação de posto (Spearman), n=27 UFs, ecológica.
        Correlação não implica causalidade.<br>
        <strong>Período:</strong> Outubro de 2026
    """), unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title" style="font-size:20px">Fontes</div>
    <div class="section-sub">
        <strong style="color:#E8EAEF">Anuário Brasileiro de Segurança Pública</strong> — edições 2018–2026, do
        Fórum Brasileiro de Segurança Pública (FBSP), com dados das SSPs estaduais.<br><br>
        <strong style="color:#E8EAEF">IBGE/SIDRA</strong> — PNAD Contínua trimestral (tabela 4093), variáveis
        taxa de desocupação e taxa de informalidade, recorte sexo feminino.<br><br>
        <strong style="color:#E8EAEF">Dados de medidas protetivas</strong> — Anuários FBSP 2025 (T31) e 2026 (T27).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dafem-footer">
        <strong>DaFem</strong> v1.0 · Squad de Dados — Fora FB! · Outubro 2026<br>
        Todos os dados são públicos e a análise é reproduzível (scripts Python anexos).<br>
        Este dashboard não coleta dados pessoais e não utiliza cookies de rastreamento.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════ FOOTER GLOBAL ═══════════════════════════

if pagina != "Sobre":
    footer()
