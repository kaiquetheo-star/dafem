# -*- coding: utf-8 -*-
"""
Análise histórica de feminicídios no Brasil (2016-2025)
Tarefa do squad de dados — servidor Fora FB!
Fonte: Anuário Brasileiro de Segurança Pública 2026 (FBSP)
       https://forumseguranca.org.br/publicacoes/anuario-brasileiro-de-seguranca-publica/

Gera: série em CSV + 3 gráficos prontos para redes sociais (com fonte citada)
      + verificação automática de sobreposição de textos.

Uso:  python analise_feminicidio.py
Requer: pandas, matplotlib, openpyxl  (pip install pandas matplotlib openpyxl)
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

AQUI = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(AQUI, "anuario-2026.xlsx")
FONTE_LINHA1 = ("Fonte: Anuário Brasileiro de Segurança Pública 2026 — Fórum Brasileiro de "
                "Segurança Pública (FBSP), com dados das SSPs estaduais.")
FONTE_LINHA2 = ("Elaboração própria. Feminicídio: homicídio qualificado por condições de "
                "gênero (Lei 13.104/2015).")

ROXO = "#6a1b9a"
ROXO_CLARO = "#b39ddb"
CINZA = "#78909c"
VERMELHO = "#c62828"
VERDE = "#2e7d32"

# ----------------------------------------------------------------------------
# 1) Extração da série histórica (aba P06 do Anuário 2026)
# ----------------------------------------------------------------------------
def extrair_serie():
    painel = pd.read_excel(XLSX, sheet_name="P06", header=None)
    anos, fem, hom = [], [], []
    linha_anos = None
    for i, linha in enumerate(painel.values.tolist()):
        textos = [c for c in linha if pd.notna(c)]
        if linha_anos is None and any(str(c) == "2016" for c in textos if pd.notna(c)):
            linha_anos = i
            anos = [int(c) for c in textos if str(c).replace(".0", "").isdigit()][:10]
        if linha_anos is not None and i > linha_anos:
            rotulo = str(textos[0]) if textos else ""
            valores = [c for c in textos[1:] if isinstance(c, (int, float))]
            if rotulo.startswith("Feminicídios") and len(valores) >= 10:
                fem = [int(v) for v in valores[:10]]
            if rotulo.startswith("Homicídios") and len(valores) >= 10:
                hom = [int(v) for v in valores[:10]]
    serie = pd.DataFrame({
        "ano": anos,
        "feminicidios": fem,
        "homicidios_mulheres_total": hom,
    })
    serie["proporcao_feminicidio_pct"] = (serie.feminicidios /
                                          serie.homicidios_mulheres_total * 100).round(1)
    serie["var_feminicidio_pct"] = serie.feminicidios.pct_change().mul(100).round(1)
    serie["var_homicidios_pct"] = serie.homicidios_mulheres_total.pct_change().mul(100).round(1)
    return serie

# ----------------------------------------------------------------------------
# 2) Estatísticas por período de governo
# ----------------------------------------------------------------------------
def variacao(serie, ano_base, ano_fim):
    f0 = serie.loc[serie.ano == ano_base, "feminicidios"].iloc[0]
    f1 = serie.loc[serie.ano == ano_fim, "feminicidios"].iloc[0]
    h0 = serie.loc[serie.ano == ano_base, "homicidios_mulheres_total"].iloc[0]
    h1 = serie.loc[serie.ano == ano_fim, "homicidios_mulheres_total"].iloc[0]
    return ((f1 - f0) / f0 * 100, (h1 - h0) / h0 * 100)

def stats_governos(serie):
    mandatos = [
        ("Temer (2016–18)", 2016, 2018),
        ("Bolsonaro (2019–22)", 2018, 2022),
        ("Lula (2023–25)", 2022, 2025),
    ]
    out = []
    for rotulo, a0, a1 in mandatos:
        base = a0
        vf, vh = variacao(serie, base, a1)
        out.append({"governo": rotulo, "var_feminicidio_pct": round(vf, 1),
                    "var_homicidios_mulheres_pct": round(vh, 1)})
    return pd.DataFrame(out)

# ----------------------------------------------------------------------------
# 3) Esqueleto de figura com faixas fixas (título / subtítulo / rodapé)
#    — elimina sobreposição por construção.
#    Layout vertical da FIGURA (frações de altura):
#      0.985–0.955  título          (fig.suptitle)
#      0.945–0.845  subtítulo       (fig.text, até 3 linhas)
#      0.975–0.950  (reservado espaçamento)
#      0.955–0.085  EIXOS (gráfico)
#      0.065–0.005  rodapé (2 linhas)
# ----------------------------------------------------------------------------
def nova_figura(titulo, subtitulo, footer_extra=None, legend_abaixo=False):
    fig, ax = plt.subplots(figsize=(11, 8), dpi=150)
    topo_eixos = 0.845 if legend_abaixo else 0.87
    base_eixos = 0.175 if legend_abaixo else 0.115
    fig.subplots_adjust(top=topo_eixos, bottom=base_eixos, left=0.095, right=0.97)
    fig.suptitle(titulo, y=0.968, fontsize=19, fontweight="bold", color="#222222")
    fig.text(0.5, 0.925, subtitulo, ha="center", va="top", fontsize=11.5,
             color="#333333", linespacing=1.35)
    fig.text(0.02, 0.045, FONTE_LINHA1, fontsize=7.8, color="#555555", ha="left", va="top")
    fig.text(0.02, 0.018, FONTE_LINHA2, fontsize=7.8, color="#555555", ha="left", va="top")
    if footer_extra:
        fig.text(0.02, 0.070, footer_extra, fontsize=7.8, color="#555555",
                 ha="left", va="top")
    return fig, ax

def checar_sobreposicao(fig, nome):
    """Auditoria: retorna pares de textos da figura cujos retângulos se intersectam."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    artistas = []
    for art in fig.texts:
        artistas.append(("fig:" + (art.get_text()[:28].replace("\n", " ")), art))
    for art in fig.axes[0].texts:
        artistas.append(("ax:" + (art.get_text()[:28].replace("\n", " ")), art))
    caixas = [(nome_, art.get_window_extent(renderer=renderer)) for nome_, art in artistas]
    problemas = []
    for i in range(len(caixas)):
        for j in range(i + 1, len(caixas)):
            if caixas[i][1].overlaps(caixas[j][1]):
                problemas.append((caixas[i][0], caixas[j][0]))
    if problemas:
        print(f"  [!] {nome}: {len(problemas)} sobreposições de texto detectadas")
        for a, b in problemas[:8]:
            print(f"      '{a}'  <->  '{b}'")
    else:
        print(f"  [ok] {nome}: nenhum texto sobreposto")
    return problemas

GOVS = [(2016, 2018, "Temer"), (2019, 2022, "Bolsonaro"), (2023, 2025, "Lula")]
CORES_GOV = {"Temer": "#eceff1", "Bolsonaro": "#ffe0b2", "Lula": "#e1f5fe"}

# ----------------------------------------------------------------------------
# 4) Gráficos
# ----------------------------------------------------------------------------
def grafico_1(serie):
    fig, ax = nova_figura(
        "Feminicídios X total de homicídios de mulheres — Brasil, 2016–2025",
        "O total de mulheres assassinadas CAIU 17% desde 2016.\n"
        "A alta do feminicídio é tendência de uma década — atravessa três governos.",
        legend_abaixo=True)
    # cabeçalho vertical garantido: dados até 4.556; eixo vai até 5.250
    ax.set_ylim(700, 5250)
    for a0, a1, nome in GOVS:
        ax.axvspan(a0 - 0.5, a1 + 0.5, color=CORES_GOV[nome], zorder=0)
        ax.text((a0 + a1) / 2, 5060, nome, ha="center", va="top", fontsize=13,
                fontweight="bold", color="#455a64", zorder=5,
                bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=2.5))
    ax.plot(serie.ano, serie.homicidios_mulheres_total, "-o", color=CINZA, lw=3,
            markersize=7, label="Homicídios de mulheres — TOTAL (−17% na década)", zorder=3)
    ax.plot(serie.ano, serie.feminicidios, "-o", color=ROXO, lw=4, markersize=8,
            label="Feminicídios (+69% na década)", zorder=4)
    for _, r in serie.iterrows():
        ax.annotate(f"{r.feminicidios:,}".replace(",", "."), (r.ano, r.feminicidios),
                    textcoords="offset points", xytext=(0, -20), ha="center",
                    fontsize=9.5, color=ROXO, fontweight="bold", zorder=6)
        ax.annotate(f"{r.homicidios_mulheres_total:,}".replace(",", "."),
                    (r.ano, r.homicidios_mulheres_total), textcoords="offset points",
                    xytext=(0, 11), ha="center", fontsize=9, color=CINZA, zorder=6)
    ax.set_xticks(serie.ano)
    ax.tick_params(axis="both", labelsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda v, _: f"{int(v):,}".replace(",", ".")))
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.085), fontsize=11.5,
              framealpha=0.95)
    ax.grid(axis="y", alpha=0.3)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    checar_sobreposicao(fig, "gráfico 1")
    caminho = os.path.join(AQUI, "grafico_1_tendencia.png")
    fig.savefig(caminho)
    plt.close(fig)
    return caminho

def grafico_2(serie):
    fig, ax = nova_figura(
        "Parcela dos homicídios de mulheres classificada como feminicídio — 2016–2025",
        "DOBROU: de 22% para 44%. Parte da alta reflete melhoria na classificação dos "
        "crimes,\ndepois que a Lei do Feminicídio (13.104/2015) passou a ser incorporada "
        "progressivamente pelas polícias estaduais.")
    ax.set_ylim(0, 56)
    ax.fill_between(serie.ano, serie.proporcao_feminicidio_pct, color=ROXO_CLARO, alpha=0.5)
    ax.plot(serie.ano, serie.proporcao_feminicidio_pct, "-o", color=ROXO, lw=4, markersize=9)
    for _, r in serie.iterrows():
        ax.annotate(f"{r.proporcao_feminicidio_pct:.0f}%", (r.ano, r.proporcao_feminicidio_pct),
                    textcoords="offset points", xytext=(0, 12), ha="center",
                    fontsize=12, fontweight="bold", color=ROXO)
    ax.set_xticks(serie.ano)
    ax.tick_params(axis="both", labelsize=11)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.grid(axis="y", alpha=0.3)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    checar_sobreposicao(fig, "gráfico 2")
    caminho = os.path.join(AQUI, "grafico_2_proporcao.png")
    fig.savefig(caminho)
    plt.close(fig)
    return caminho

def grafico_3(stats):
    fig, ax = nova_figura(
        "Variação por mandato: feminicídios X total de homicídios de mulheres",
        "A subida dos feminicídios atravessa os três governos — e foi maior nos mandatos "
        "anteriores.\nNo governo Lula, o total de mulheres assassinadas teve a maior queda "
        "da série (−10%).")
    x = range(len(stats))
    larg = 0.38
    b1 = ax.bar([i - larg / 2 for i in x], stats.var_feminicidio_pct, larg,
                color=ROXO, label="Variação dos FEMINICÍDIOS no mandato")
    b2 = ax.bar([i + larg / 2 for i in x], stats.var_homicidios_mulheres_pct, larg,
                color=CINZA, label="Variação do TOTAL de homicídios de mulheres")
    for barras in (b1, b2):
        for b in barras:
            v = b.get_height()
            ax.annotate(f"{v:+.1f}%".replace(".", ","), (b.get_x() + b.get_width() / 2, v),
                        textcoords="offset points", xytext=(0, 7 if v >= 0 else -17),
                        ha="center", fontsize=12, fontweight="bold",
                        color=VERMELHO if v > 0 else VERDE)
    ax.axhline(0, color="#333333", lw=1)
    ax.set_ylim(-16, 40)
    ax.set_xticks(list(x))
    ax.set_xticklabels(stats.governo, fontsize=13)
    ax.tick_params(axis="y", labelsize=11)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.grid(axis="y", alpha=0.3)
    ax.legend(fontsize=11, loc="upper right", framealpha=0.95)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    checar_sobreposicao(fig, "gráfico 3")
    caminho = os.path.join(AQUI, "grafico_3_mandatos.png")
    fig.savefig(caminho)
    plt.close(fig)
    return caminho

# ----------------------------------------------------------------------------
def main():
    serie = extrair_serie()
    csv_path = os.path.join(AQUI, "serie_feminicidio_brasil_2016_2025.csv")
    serie.to_csv(csv_path, index=False, encoding="utf-8-sig")

    stats = stats_governos(serie)

    print("=" * 64)
    print("SÉRIE BRASIL 2016–2025 (fonte: Anuário FBSP 2026)")
    print(serie.to_string(index=False))
    print("-" * 64)
    print("Variação por mandato:")
    print(stats.to_string(index=False))
    print("-" * 64)
    print(f"2016→2025  feminicídios: {serie.feminicidios.iloc[-1] - serie.feminicidios.iloc[0]:+d} "
          f"({(serie.feminicidios.iloc[-1]/serie.feminicidios.iloc[0]-1)*100:+.1f}%)")
    print(f"2016→2025  homicídios de mulheres: "
          f"{serie.homicidios_mulheres_total.iloc[-1] - serie.homicidios_mulheres_total.iloc[0]:+d} "
          f"({(serie.homicidios_mulheres_total.iloc[-1]/serie.homicidios_mulheres_total.iloc[0]-1)*100:+.1f}%)")
    print("2025: 70 vítimas tinham medida protetiva ativa quando foram mortas (T22)")
    print("=" * 64)
    print("Auditoria visual (sobreposição de textos):")

    g1 = grafico_1(serie)
    g2 = grafico_2(serie)
    g3 = grafico_3(stats)
    print("Gráficos gerados:")
    for g in (g1, g2, g3):
        print(" -", g)
    print("CSV:", csv_path)

if __name__ == "__main__":
    main()
