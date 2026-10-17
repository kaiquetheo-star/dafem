# -*- coding: utf-8 -*-
"""
b4_medidas_protetivas.py - Medidas protetivas (MPU) por UF e correlacao com feminicidio.
Extrai: MPU concedidas (T31 ed2025), descumprimentos (T27 ed2026), vítimas com MPU ativa (T22 ed2026).
Correlaciona com taxa de feminicídio do painel (Spearman, n=27).
Tese testada: "proteção no papel" — mais MPU concedida reduz feminicídio? Descumprimento aumenta?
"""
import os
import re
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
ANU = os.path.join(AQUI, "anuaries")

UFS = ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
       "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul",
       "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí",
       "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia",
       "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"]

def limpa_uf(s):
    return re.sub(r"\s*\(\d+\)\s*$", "", str(s).strip())

def num(v):
    if pd.isna(v):
        return np.nan
    try:
        return float(v)
    except (TypeError, ValueError):
        return np.nan

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
    # ---- extrai MPU concedidas 2024 (T31 ed2025) ----
    df31 = pd.read_excel(os.path.join(ANU, "anuario-2025.xlsx"), sheet_name="T31", header=None)
    mpu = {}
    for _, l in df31.iterrows():
        uf = limpa_uf(l[0]) if pd.notna(l[0]) else ""
        if uf not in UFS:
            continue
        mpu[uf] = {
            "mpu_dist_24": num(l[2]),        # distribuídas 2024
            "mpu_dist_taxa_24": num(l[4]),   # taxa distribuídas 2024
            "mpu_conc_24": num(l[7]),        # concedidas 2024
            "mpu_conc_taxa_24": num(l[9]),   # taxa concedidas 2024
            "mpu_pct_conc_24": num(l[12]),   # % concedidas 2024
        }
    df_mpu = pd.DataFrame(mpu).T.reset_index().rename(columns={"index": "uf"})

    # ---- extrai descumprimento 2025 (T27 ed2026) ----
    df27 = pd.read_excel(os.path.join(ANU, "anuario-2026.xlsx"), sheet_name="T27", header=None)
    desc = {}
    for _, l in df27.iterrows():
        uf = limpa_uf(l[0]) if pd.notna(l[0]) else ""
        if uf not in UFS:
            continue
        desc[uf] = {
            "desc_abs_25": num(l[2]),        # descumprimento 2025
            "desc_taxa_25": num(l[4]),       # taxa descumprimento 2025
        }
    df_desc = pd.DataFrame(desc).T.reset_index().rename(columns={"index": "uf"})

    # ---- junta com painel de feminicidio ----
    painel = pd.read_csv(os.path.join(AQUI, "painel_feminicidio_uf_2016_2025.csv"))
    fem = painel[painel.uf != "Brasil"][["uf", "ano", "fem_abs", "fem_taxa"]]

    base = (fem[(fem.ano.isin([2024, 2025]))]
            .pivot_table(index="uf", columns="ano", values="fem_taxa")
            .reset_index())
    base.columns = ["uf", "fem_taxa_24", "fem_taxa_25"]
    base = base.merge(df_mpu, on="uf", how="inner").merge(df_desc, on="uf", how="inner")

    # métrica derivada: descumprimentos por 100 MPUs concedidas ("taxa de falha da proteção")
    base["falha_por100mpu_25"] = (base["desc_abs_25"] / base["mpu_conc_24"].replace(0, np.nan) * 100).round(1)

    base.to_csv(os.path.join(AQUI, "b4_medidas_protetivas_uf.csv"), index=False, encoding="utf-8-sig")

    # ---- correlacoes ----
    print("=" * 76)
    print("B4: CORRELAÇÕES MPU X FEMINICÍDIO (Spearman, 27 UFs)")
    print("=" * 76)
    pares = [
        ("fem_taxa_24", "mpu_conc_taxa_24", "Feminicídio 2024 X MPU concedida (taxa) 2024"),
        ("fem_taxa_25", "desc_taxa_25", "Feminicídio 2025 X Descumprimento MPU (taxa) 2025"),
        ("fem_taxa_25", "falha_por100mpu_25", "Feminicídio 2025 X Falha por 100 MPUs concedidas"),
        ("fem_taxa_24", "mpu_pct_conc_24", "Feminicídio 2024 X % MPUs concedidas"),
    ]
    for xcol, ycol, rotulo in pares:
        rho, p, n = spearman(base[xcol], base[ycol])
        estrela = " ***" if p < 0.01 else (" *" if p < 0.05 else "")
        print(f"   {rotulo}")
        print(f"      rho={rho:+.3f}{estrela}  p={p:.4f}  n={n}")

    # ---- ranking: estados com maior taxa de falha ----
    print("\n=== TOP/BOTTOM: Descumprimentos por 100 MPUs concedidas (proxy de falha de proteção) ===")
    ordem = base.sort_values("falha_por100mpu_25", ascending=False)
    print("MAIORES FALHAS:")
    for _, r in ordem.head(6).iterrows():
        print(f"   {r['uf']:24s} {r['falha_por100mpu_25']:>6.1f} descumprimentos/100 MPU | "
              f"fem_taxa_25={r['fem_taxa_25']:.2f}")
    print("MENORES FALHAS:")
    for _, r in ordem.tail(4).iterrows():
        print(f"   {r['uf']:24s} {r['falha_por100mpu_25']:>6.1f} descumprimentos/100 MPU | "
              f"fem_taxa_25={r['fem_taxa_25']:.2f}")

    # ---- resumo nacional ----
    print("\n=== NÚMEROS NACIONAIS ===")
    print(f"   MPUs distribuídas 2024: {base['mpu_dist_24'].sum():,.0f}")
    print(f"   MPUs concedidas 2024: {base['mpu_conc_24'].sum():,.0f}")
    print(f"   Descumprimentos 2025: {base['desc_abs_25'].sum():,.0f}")
    print(f"   Vítimas com MPU ativa no óbito 2025: 70 (Brasil)")

    print(f"\nSalvo: b4_medidas_protetivas_uf.csv ({len(base)} UFs)")

if __name__ == "__main__":
    main()
