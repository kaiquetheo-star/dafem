# -*- coding: utf-8 -*-
"""
b5_correlacoes.py - Correlacao (Spearman) taxa de feminicidio x desemprego feminino, por UF.
n=27, corte transversal por ano e media 2023-25. Correlacao != causalidade (nota metodologica).
Fontes: FBSP (Anuarios, taxa/100k mulheres) e IBGE/SIDRA t4093 (PNAD Continua, mulheres).
"""
import os
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))

def _betacf(a, b, x):
    """Fracao continua da funcao beta incompleta (Numerical Recipes)."""
    MAXIT, EPS, FPMIN = 300, 3e-16, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < EPS:
            break
    return h


def _betai(a, b, x):
    """Funcao beta incompleta regularizada I_x(a,b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                  + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def _t_p_bicaudal(t, df):
    """p bicaudal de T de Student: I_{df/(df+t^2)}(df/2, 1/2)."""
    return _betai(df / 2.0, 0.5, df / (df + t * t))


def spearman(x, y):
    """Spearman rho via Pearson nos postos; p-valor bicaudal pela distribuicao t (df=n-2)."""
    ok = pd.concat([x, y], axis=1).dropna()
    n = len(ok)
    if n < 8:
        return np.nan, np.nan, n
    rx = ok.iloc[:, 0].rank()
    ry = ok.iloc[:, 1].rank()
    rho = rx.corr(ry)
    t = rho * np.sqrt((n - 2) / max(1e-12, 1 - rho ** 2))
    p = _t_p_bicaudal(abs(t), n - 2)
    return rho, p, n

def main():
    painel = pd.read_csv(os.path.join(AQUI, "painel_feminicidio_uf_2016_2025.csv"))
    desemp = pd.read_csv(os.path.join(AQUI, "b1_desemprego_mulheres_uf.csv"))

    df = painel[painel.uf != "Brasil"].merge(desemp, on=["uf", "ano"], how="inner")
    print(f"Base combinada: {len(df)} UF-ano | UFs: {df.uf.nunique()}")

    # ---- 1) correlacao por ano ----
    print("\n=== SPEARMAN por ano: taxa feminicidio x desemprego mulheres (27 UFs) ===")
    linhas = []
    for ano in sorted(df.ano.unique()):
        sub = df[df.ano == ano]
        rho, p, n = spearman(sub["fem_taxa"], sub["desemp_mulheres_pct"])
        nota = " (dado fraco: pandemia)" if ano in (2020,) else ""
        linhas.append({"ano": ano, "rho": rho, "p_valor": p, "n": n})
        estrela = "*" if p < 0.05 else " "
        print(f"   {ano}: rho={rho:+.3f}{estrela}  p={p:.3f}  n={n}{nota}")
    res = pd.DataFrame(linhas)
    res.to_csv(os.path.join(AQUI, "b5_correlacao_por_ano.csv"), index=False, encoding="utf-8-sig")

    # ---- 2) media 2023-25 (periodo recente estavel) ----
    fem3 = (df[df.ano.isin([2023, 2024, 2025])].groupby("uf", as_index=False)
            .agg(fem_taxa_media=("fem_taxa", "mean"),
                 fem_abs_medio=("fem_abs", "mean")))
    de3 = (df[df.ano.isin([2023, 2024, 2025])].groupby("uf", as_index=False)
           .agg(desemp_medio=("desemp_mulheres_pct", "mean")))
    m3 = fem3.merge(de3, on="uf")
    rho3, p3, n3 = spearman(m3["fem_taxa_media"], m3["desemp_medio"])
    print(f"\n=== MEDIA 2023-25: rho={rho3:+.3f}  p={p3:.3f}  n={n3} ===")

    # hom_totais como contraste (a relacao muda quando o recorte e 'mulheres'?)
    hom3 = (df[df.ano.isin([2023, 2024, 2025])].groupby("uf", as_index=False)
            .agg(hom_taxa_media=("hom_abs", "sum")))
    # hom_abs nao e taxa; usar proporcao feminicidio/homicidios como 2a metrica
    prop3 = (df[df.ano.isin([2023, 2024, 2025])].groupby("uf", as_index=False)
             .agg(prop_media=("prop_pct", "mean")))
    m3b = m3.merge(prop3, on="uf")
    rho_prop, p_prop, _ = spearman(m3b["prop_media"], m3b["desemp_medio"])
    print(f"Contraste - % classificada como feminicidio x desemprego: rho={rho_prop:+.3f}  p={p_prop:.3f}")

    # ---- 3) grafico: scatter 2025 e media 23-25, lado a lado ----
    FONTE1 = ("Fontes: Anuarios Brasileiros de Seguranca Publica (FBSP) e IBGE/SIDRA (PNAD Continua, tab. 4093 - mulheres)."
              " Elaboracao propria.")
    FONTE2 = "Correlacao de posto (Spearman), n=27 UFs. Correlacao NAO implica causalidade."
    fig, axes = plt.subplots(1, 2, figsize=(13, 7.5), dpi=150)
    fig.subplots_adjust(top=0.82, bottom=0.14, left=0.07, right=0.98, wspace=0.25)
    fig.suptitle("Feminicídio X desemprego feminino — quem tem mais, quem tem menos",
                 y=0.965, fontsize=19, fontweight="bold", color="#222222")
    fig.text(0.5, 0.925, "Cada ponto é um estado. À esquerda o retrato de 2025; à direita a média 2023-25.",
             ha="center", va="top", fontsize=11.5, color="#333333")
    fig.text(0.02, 0.048, FONTE1, fontsize=7.8, color="#555555", ha="left", va="top")
    fig.text(0.02, 0.020, FONTE2, fontsize=7.8, color="#555555", ha="left", va="top")

    sub25 = df[df.ano == 2025]
    registros = []  # (annotation, rank de extremidade em fem_taxa) para auto-correcao
    for ax, (xd, yd, rot, rho, p, subs) in zip(axes, [
        (sub25["desemp_mulheres_pct"], sub25["fem_taxa"], "2025", rho_25 := spearman(sub25["fem_taxa"], sub25["desemp_mulheres_pct"])[0], spearman(sub25["fem_taxa"], sub25["desemp_mulheres_pct"])[1], sub25),
        (m3["desemp_medio"], m3["fem_taxa_media"], "média 2023-25", rho3, p3, m3),
    ]):
        ax.scatter(xd, yd, s=60, color="#6a1b9a", alpha=0.75, edgecolor="white")
        # rotula apenas extremos: top/bottom 5 de cada eixo (grafico limpo, zero colisao)
        ord_fem = subs.sort_values("fem_taxa" if "fem_taxa" in subs else "fem_taxa_media", ascending=False)["uf"].tolist()
        ord_des = subs.sort_values("desemp_mulheres_pct" if "desemp_mulheres_pct" in subs else "desemp_medio", ascending=False)["uf"].tolist()
        rotular = set(ord_fem[:5]) | set(ord_fem[-5:]) | set(ord_des[:5]) | set(ord_des[-5:])
        rank_aqui = {uf: i for i, uf in enumerate(ord_fem)}
        for i, (_, r) in enumerate(subs.iterrows()):
            if r["uf"] not in rotular:
                continue
            sigla = {"Acre": "AC", "Alagoas": "AL", "Amapá": "AP", "Amazonas": "AM", "Bahia": "BA",
                     "Ceará": "CE", "Distrito Federal": "DF", "Espírito Santo": "ES", "Goiás": "GO",
                     "Maranhão": "MA", "Mato Grosso": "MT", "Mato Grosso do Sul": "MS",
                     "Minas Gerais": "MG", "Pará": "PA", "Paraíba": "PB", "Paraná": "PR",
                     "Pernambuco": "PE", "Piauí": "PI", "Rio de Janeiro": "RJ",
                     "Rio Grande do Norte": "RN", "Rio Grande do Sul": "RS", "Rondônia": "RO",
                     "Roraima": "RR", "Santa Catarina": "SC", "São Paulo": "SP", "Sergipe": "SE",
                     "Tocantins": "TO"}[r["uf"]]
            desloc = (4, 4) if i % 3 == 0 else ((4, -10) if i % 3 == 1 else (-14, 4))
            ann = ax.annotate(sigla, (r[xd.name if hasattr(xd, 'name') else 0], r[yd.name if hasattr(yd, 'name') else 0]),
                              textcoords="offset points", xytext=desloc, fontsize=9, color="#333333",
                              fontweight="bold")
            registros.append((ann, rank_aqui[r["uf"]]))
        ax.set_title(f"{rot}   ρ = {rho:+.2f}  (p = {p:.2f})", fontsize=13, fontweight="bold",
                     color="#2e7d32" if p < 0.05 else "#555555")
        ax.set_xlabel("Desemprego das mulheres (%)", fontsize=11.5)
        ax.set_ylabel("Taxa de feminicídio /100k mulheres", fontsize=11.5)
        ax.grid(alpha=0.3)
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)

    # auditoria de sobreposicao com auto-correcao: colidiu -> remove rotulo do estado menos extremo
    for _ in range(3):
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        itens = [(a, a.get_window_extent(renderer=r), rk) for a, rk in registros if a.get_text()]
        colisoes = [(itens[i], itens[j]) for i in range(len(itens)) for j in range(i + 1, len(itens))
                    if itens[i][1].overlaps(itens[j][1])]
        if not colisoes:
            break
        for (a1, _, r1), (a2, _, r2) in colisoes:
            perdedor = a1 if r1 > r2 else a2  # rank maior = menos extremo
            perdedor.set_text("")
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    arts = [(("fig:" + a.get_text()[:20].replace("\n", " ")), a) for a in fig.texts]
    for axx in axes:
        arts += [(("ax:" + a.get_text()[:20]), a) for a in axx.texts]
    boxes = [(n, a.get_window_extent(renderer=r)) for n, a in arts]
    probs = [(boxes[i][0], boxes[j][0]) for i in range(len(boxes))
             for j in range(i + 1, len(boxes)) if boxes[i][1].overlaps(boxes[j][1])]
    print(f"\nAuditoria grafico (pos auto-correcao): {len(probs)} sobreposicoes"
          + (f" -> {probs[:4]}" if probs else " [ok]"))

    caminho = os.path.join(AQUI, "b5_scatter_desemprego.png")
    fig.savefig(caminho)
    plt.close(fig)
    print("Gerado:", caminho)

if __name__ == "__main__":
    main()
