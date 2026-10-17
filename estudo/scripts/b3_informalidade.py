# -*- coding: utf-8 -*-
"""
b3_informalidade.py - Informalidade feminina por UF (proxy de vulnerabilidade economica/BF) 
+ correlacao com feminicidio + matriz resumida das variaveis B1+B3+B4.
Fonte: IBGE/SIDRA t4093 v12466 c2/5 (PNAD Continua, mulheres).
"""
import os
import json
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEM = r"C:\Users\Kaique\.local\share\opencode\tool-output\tool_149f37b090011qz7RFPTBKO3Db"

def spearman(x, y):
    ok = pd.concat([x, y], axis=1).dropna()
    n = len(ok)
    if n < 8:
        return np.nan, np.nan, n
    rho = ok.iloc[:, 0].rank().corr(ok.iloc[:, 1].rank())
    t = rho * np.sqrt((n - 2) / max(1e-12, 1 - rho ** 2))
    from math import erf, sqrt
    p = 2 * (1 - 0.5 * (1 + erf(abs(t) / sqrt(2))))
    return rho, p, n

def main():
    # ---- parse informalidade ----
    with open(ORIGEM, "r", encoding="utf-8") as f:
        dados = json.load(f)
    linhas = [d for d in dados[1:] if str(d.get("D1N")) != "Unidade da Federação"]
    inf = pd.DataFrame([{
        "uf": d["D1N"],
        "tri": str(d["D2C"]),
        "informal": pd.to_numeric(d["V"], errors="coerce"),
    } for d in linhas])
    inf["ano"] = inf["tri"].str[:4].astype(int)
    inf = inf[(inf.ano >= 2016) & (inf.ano <= 2025)]

    # media anual
    inf_anual = (inf.dropna(subset=["informal"])
                 .groupby(["uf", "ano"], as_index=False)["informal"].mean()
                 .rename(columns={"informal": "informal_fem_pct"}))
    inf_anual.to_csv(os.path.join(AQUI, "b3_informalidade_mulheres_uf.csv"),
                     index=False, encoding="utf-8-sig")
    w = inf_anual.pivot(index="uf", columns="ano", values="informal_fem_pct")
    w.to_csv(os.path.join(AQUI, "b3_informalidade_mulheres_uf_wide.csv"), encoding="utf-8-sig")
    print("=== INFORMALIDADE FEMENINA (% da ocupação), amostra ===")
    print(w.round(1).head(6).to_string())

    # ---- carrega painel + B1 + B4 ----
    painel = pd.read_csv(os.path.join(AQUI, "painel_feminicidio_uf_2016_2025.csv"))
    fem = painel[painel.uf != "Brasil"]
    desemp = pd.read_csv(os.path.join(AQUI, "b1_desemprego_mulheres_uf.csv"))
    mpu = pd.read_csv(os.path.join(AQUI, "b4_medidas_protetivas_uf.csv"))

    # ---- correlacao informalidade x feminicidio por ano ----
    print("\n=== B3: SPEARMAN por ano: taxa feminicídio x informalidade feminina ===")
    merged = fem.merge(inf_anual, on=["uf", "ano"], how="inner")
    for ano in sorted(merged.ano.unique()):
        sub = merged[merged.ano == ano]
        rho, p, n = spearman(sub["fem_taxa"], sub["informal_fem_pct"])
        estrela = "*" if p < 0.05 else " "
        print(f"   {ano}: rho={rho:+.3f}{estrela}  p={p:.3f}  n={n}")

    # ---- MEDIA 2023-25: informalidade ----
    fem3 = (fem[fem.ano.isin([2023, 2024, 2025])].groupby("uf", as_index=False)
            .agg(fem_taxa=("fem_taxa", "mean")))
    inf3 = (inf_anual[inf_anual.ano.isin([2023, 2024, 2025])].groupby("uf", as_index=False)
            .agg(informal=("informal_fem_pct", "mean")))
    base = fem3.merge(inf3, on="uf")
    rho_i, p_i, n_i = spearman(base["fem_taxa"], base["informal"])
    print(f"\nMEDIA 2023-25: informalidade x feminicidio: rho={rho_i:+.3f}  p={p_i:.3f}  n={n_i}")

    # ---- MATRIZ RESUMIDA: todas as variaveis B1+B3+B4 juntas (media 23-25) ----
    print("\n" + "=" * 76)
    print("MATRIZ RESUMIDA — FEMINICÍDIO X VARIÁVEIS (Spearman, média 2023-25, 27 UFs)")
    print("=" * 76)

    desemp3 = (desemp[desemp.ano.isin([2023, 2024, 2025])].groupby("uf", as_index=False)
               .agg(desemp=("desemp_mulheres_pct", "mean")))
    mpu_base = mpu[["uf", "mpu_conc_taxa_24", "desc_taxa_25"]].copy()
    mpu_base.columns = ["uf", "mpu_conc", "descump"]

    matriz_base = (base.merge(desemp3, on="uf", how="inner")
                        .merge(mpu_base, on="uf", how="inner"))

    pares = [
        ("fem_taxa", "informal", "Informalidade feminina (%) [proxy BF/vulnerabilidade]"),
        ("fem_taxa", "desemp",   "Desemprego feminino (%) [B1]"),
        ("fem_taxa", "mpu_conc", "MPU concedida por 100k mulheres [B4]"),
        ("fem_taxa", "descump",  "Descumprimento MPU por 100k [B4]"),
    ]
    for xcol, ycol, rotulo in pares:
        rho, p, n = spearman(matriz_base[xcol], matriz_base[ycol])
        estrela = " ***" if p < 0.01 else (" *" if p < 0.05 else "")
        print(f"   {rotulo}")
        print(f"      rho={rho:+.3f}{estrela}  p={p:.4f}  n={n}")

    # inter-correlacao entre variaveis (confundidores?)
    print("\nINTER-CORRELAÇÕES (as variáveis explicativas se correlacionam entre si?)")
    for (x, y, rx, ry) in [("desemp", "informal", "Desemprego", "Informalidade"),
                           ("mpu_conc", "descump", "MPU concedida", "Descumprimento"),
                           ("informal", "mpu_conc", "Informalidade", "MPU concedida")]:
        rho, p, _ = spearman(matriz_base[x], matriz_base[y])
        print(f"   {rx} x {ry}: rho={rho:+.3f}  p={p:.3f}")

    matriz_base.to_csv(os.path.join(AQUI, "matriz_variaveis_uf_2023_25.csv"),
                       index=False, encoding="utf-8-sig")
    print(f"\nBase da matriz salva: matriz_variaveis_uf_2023_25.csv ({len(matriz_base)} UFs)")

if __name__ == "__main__":
    main()
