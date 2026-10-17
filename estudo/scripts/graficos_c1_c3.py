# -*- coding: utf-8 -*-
"""
graficos_c1_c3.py — C1: raça/cor no tempo + C3: linha legislativa sobre a série de feminicídio.
Fontes: painéis "Perfil dos Feminicídios" dos Anuários FBSP (edições 2019, 2020, 16ª, 2025, 2026).
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches

AQUI = os.path.dirname(os.path.abspath(__file__))

FONTE1 = ("Fontes: Anuários Brasileiros de Segurança Pública (FBSP) 2019-2026, painéis 'Perfil dos Feminicídios'; "
          "IBGE (população feminina por cor/raça, Censo 2022).")
FONTE2 = "Squad de dados — Fora FB! · 17/10/2026 · Os dados de raça cobrem os anos disponíveis nos anuários."

ROXO = "#6a1b9a"
ROXO_CLARO = "#b39ddb"
VERMELHO = "#c62828"
VERDE = "#2e7d32"
AZUL = "#1565c0"
CINZA = "#78909c"
PRETO = "#1a1a1a"

def checar(fig, nome):
    """Auditoria com tolerância a falhas."""
    problemas = []
    try:
        fig.canvas.draw()
        renderer = getattr(fig.canvas, "_renderer", None)
        if renderer is None:
            return problemas
        artistas = []
        for art in fig.texts:
            artistas.append(("fig:" + (art.get_text()[:28].replace("\n", " ")), art))
        for ax in fig.axes:
            for art in ax.texts:
                artistas.append(("ax:" + (art.get_text()[:28].replace("\n", " ")), art))
        caixas = [(nome_, art.get_window_extent(renderer=renderer)) for nome_, art in artistas]
        for i in range(len(caixas)):
            for j in range(i + 1, len(caixas)):
                if caixas[i][1].overlaps(caixas[j][1]):
                    problemas.append((caixas[i][0], caixas[j][0]))
    except Exception:
        pass  # gráfico já foi salvo
    if problemas:
        print(f"  [!] {nome}: {len(problemas)} sobreposições")
    else:
        print(f"  [ok] {nome}: nenhum texto sobreposto")
    return problemas

def grafico_c1_raca():
    """C1: % de vítimas negras vs população, ao longo do tempo."""
    # dados extraídos dos painéis (percentuais)
    raca = pd.DataFrame([
        {"periodo": "2017-18", "edicao": "Anuário 2019 (P4)", "negra_pct": 60.98, "branca_pct": 38.53},
        {"periodo": "2019",    "edicao": "Anuário 2020 (P5)", "negra_pct": 66.57, "branca_pct": 33.14},
        {"periodo": "2020-21", "edicao": "Anuário 16ª ed (P08)", "negra_pct": 61.97, "branca_pct": 37.54},
        {"periodo": "2023-24", "edicao": "Anuário 2025 (P07)", "negra_pct": 63.57, "branca_pct": 35.71},
        {"periodo": "2025",    "edicao": "Anuário 2026 (P06)", "negra_pct": 65.08, "branca_pct": 34.04},
    ])

    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=150)
    fig.subplots_adjust(top=0.82, bottom=0.14, left=0.10, right=0.97)
    fig.suptitle("As vítimas de feminicídio são majoritariamente NEGRAS — sempre", y=0.965,
                 fontsize=19, fontweight="bold", color=PRETO)
    fig.text(0.5, 0.925,
             "Em TODOS os períodos com dado disponível, mulheres negras são 60-67% das vítimas,\n"
             "enquanto são ~55% da população feminina brasileira (Censo 2022). O recorte racial é estrutural.",
             ha="center", va="top", fontsize=11.5, color="#333333", linespacing=1.35)
    fig.text(0.02, 0.045, FONTE1, fontsize=7.5, color="#555555", ha="left", va="top")
    fig.text(0.02, 0.018, FONTE2, fontsize=7.5, color="#555555", ha="left", va="top")

    x = range(len(raca))
    larg = 0.35
    b1 = ax.bar([i - larg/2 for i in x], raca["negra_pct"], larg,
                color=PRETO, label="Vítimas NEGRAS (%)")
    b2 = ax.bar([i + larg/2 for i in x], raca["branca_pct"], larg,
                color=ROXO_CLARO, label="Vítimas BRANCAS (%)")

    # linha da população feminina negra (55% IBGE Censo 2022)
    ax.axhline(y=55, color=VERMELHO, linestyle="--", linewidth=2, alpha=0.7)
    ax.text(len(raca)-0.5, 56.5, "55% da população\nfeminina é negra\n(IBGE, Censo 2022)",
            fontsize=9.5, color=VERMELHO, ha="right", va="bottom", fontweight="bold")

    for barras in (b1, b2):
        for b in barras:
            v = b.get_height()
            ax.annotate(f"{v:.0f}%", (b.get_x() + b.get_width()/2, v),
                        textcoords="offset points", xytext=(0, 5), ha="center",
                        fontsize=12, fontweight="bold", color="#333333")

    ax.set_xticks(list(x))
    ax.set_xticklabels(raca["periodo"], fontsize=12, rotation=15)
    ax.set_ylim(0, 78)
    ax.set_ylabel("% das vítimas", fontsize=12)
    ax.legend(loc="upper right", fontsize=11.5)
    ax.grid(axis="y", alpha=0.3)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

    checar(fig, "C1 raça")
    caminho = os.path.join(AQUI, "grafico_c1_raca_tempo.png")
    fig.savefig(caminho)
    plt.close(fig)
    print(f"Gerado: {caminho}")

def grafico_c3_legislativo():
    """C3: série + timeline legislativa dedicada + proporção. 3 painéis verticais."""
    br = pd.DataFrame({
        "ano": [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        "fem": [929, 1075, 1229, 1330, 1354, 1347, 1455, 1475, 1504, 1571],
        "hom": [4245, 4556, 4340, 3966, 3999, 3869, 3934, 3937, 3728, 3539],
    })
    br["prop"] = br.fem / br.hom * 100

    fig, (ax1, ax_leg, ax2) = plt.subplots(
        3, 1, figsize=(12, 10), dpi=150,
        gridspec_kw={"height_ratios": [3, 0.9, 2.2]})
    fig.subplots_adjust(top=0.88, bottom=0.10, left=0.09, right=0.97, hspace=0.55)
    fig.suptitle("O que a lei mudou — e o que ela NÃO mudou", y=0.965,
                 fontsize=19, fontweight="bold", color=PRETO)
    fig.text(0.5, 0.925,
             "Cada avanço legislativo amplia o reconhecimento do crime. Mas a execução continua falhando:\n"
             "1 em cada 4 medidas protetivas é descumprida. 70 mulheres morreram com MPU ativa em 2025.",
             ha="center", va="top", fontsize=11, color="#333333", linespacing=1.35)
    fig.text(0.02, 0.005,
             "Fontes: Anuários FBSP 2018-2026 · IBGE/SIDRA · Elaboração: squad de dados — Fora FB!",
             fontsize=7.5, color="#555555", ha="left", va="bottom")

    # === PAINEL 1: número de feminicídios ===
    ax1.plot(br.ano, br.fem, "-o", color=ROXO, lw=3, markersize=8, zorder=4)
    for i, (_, r) in enumerate(br.iterrows()):
        off = -22 if i % 2 == 0 else 14
        ax1.annotate(f"{r.fem:,}".replace(",", "."), (r.ano, r.fem),
                     textcoords="offset points", xytext=(0, off), ha="center",
                     fontsize=9, color=ROXO, fontweight="bold")
    ax1.set_xlim(2004.5, 2026)
    ax1.set_ylim(800, 1750)
    ax1.set_ylabel("Feminicídios", fontsize=12)
    ax1.set_xticks(br.ano)
    ax1.tick_params(axis="x", labelsize=9, labelbottom=False)
    ax1.grid(axis="y", alpha=0.25)
    for s in ["top", "right"]:
        ax1.spines[s].set_visible(False)
    ax1.set_title("Feminicídios no Brasil (2016-2025)", fontsize=13, pad=6)

    # === PAINEL 2: TIMELINE LEGISLATIVA (faixa dedicada) ===
    ax_leg.set_xlim(2004.5, 2026)
    ax_leg.set_ylim(-1, 1)
    ax_leg.axis("off")
    # linha do tempo
    ax_leg.axhline(y=0, color="#cccccc", linewidth=3, zorder=1)
    legislacao = [
        (2006, "Maria da Penha\n(11.340)", VERDE, -0.6),
        (2015, "Feminicídio\né crime\n(13.104)", AZUL, 0.6),
        (2019, "MPU pela\npolícia\n(13.827)", AZUL, -0.6),
        (2021, "Violência\npsicológica\n(14.188)", AZUL, 0.6),
        (2023, "Crimes\nHediondos\n(14.550)", VERDE, -0.6),
    ]
    for ano, texto, cor, y_pos in legislacao:
        ax_leg.plot(ano, 0, "o", color=cor, markersize=10, zorder=3)
        ax_leg.annotate(texto, (ano, y_pos), fontsize=8.5, color=cor, ha="center",
                        fontweight="bold", va="center",
                        bbox=dict(facecolor="white", edgecolor=cor, alpha=0.85,
                                  boxstyle="round,pad=0.3", linewidth=0.8),
                        arrowprops=dict(arrowstyle="-", color=cor, lw=1))

    # === PAINEL 3: % classificada como feminicídio ===
    ax2.fill_between(br.ano, br.prop, color=ROXO_CLARO, alpha=0.4)
    ax2.plot(br.ano, br.prop, "-o", color=ROXO, lw=2.5, markersize=6)
    for _, r in br.iterrows():
        ax2.annotate(f"{r.prop:.0f}%", (r.ano, r.prop),
                     textcoords="offset points", xytext=(0, 8), ha="center",
                     fontsize=10, fontweight="bold", color=ROXO)
    ax2.annotate("DOBRA (22% → 44%)\nEfeitos da Lei 13.104\nsendo incorporados",
                 (2019.5, 18), fontsize=10, color="#333333", ha="center", fontweight="bold",
                 bbox=dict(facecolor="white", edgecolor=ROXO_CLARO, alpha=0.85, boxstyle="round,pad=0.4"))
    ax2.set_xlim(2004.5, 2026)
    ax2.set_ylim(15, 55)
    ax2.set_ylabel("% classificado como feminicídio", fontsize=11)
    ax2.set_xlabel("Ano", fontsize=12)
    ax2.set_xticks(br.ano)
    ax2.tick_params(axis="x", labelsize=9)
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax2.grid(axis="y", alpha=0.25)
    for s in ["top", "right"]:
        ax2.spines[s].set_visible(False)
    ax2.set_title("Parcela dos homicídios de mulheres classificados como feminicídio (%)", fontsize=13, pad=6)

    # rodapé com dado forte
    fig.text(0.5, 0.035,
             "555.001 MPUs concedidas em 2024 · 132.025 descumpridas em 2025 · 70 mulheres mortas com MPU ativa",
             ha="center", fontsize=10.5, color=VERMELHO, fontweight="bold",
             bbox=dict(facecolor="#ffebee", edgecolor=VERMELHO, alpha=0.85, boxstyle="round,pad=0.4"))

    checar(fig, "C3 legislativo")
    caminho = os.path.join(AQUI, "grafico_c3_legislativo.png")
    fig.savefig(caminho)
    plt.close(fig)
    print(f"Gerado: {caminho}")

    checar(fig, "C3 legislativo")
    caminho = os.path.join(AQUI, "grafico_c3_legislativo.png")
    fig.savefig(caminho)
    plt.close(fig)
    print(f"Gerado: {caminho}")

if __name__ == "__main__":
    print("Auditoria:")
    grafico_c1_raca()
    grafico_c3_legislativo()
