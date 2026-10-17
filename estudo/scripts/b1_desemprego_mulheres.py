# -*- coding: utf-8 -*-
"""
b1_desemprego_mulheres.py - Taxa de desocupacao feminina (14+) por UF, media anual 2016-2025.
Fonte: IBGE/SIDRA tabela 4093 (PNAD Continua trimestral), variavel 4099, sexo c2/5 (Mulheres).
Saida: b1_desemprego_mulheres_uf.csv (long) + b1_desemprego_mulheres_uf_wide.csv (UF x ano).
Nota de qualidade: 2020 so tem o 1o tri (IBGE suprimiu a serie durante a pandemia); 2021 sem dado.
"""
import json
import os
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEM = r"C:\Users\Kaique\.local\share\opencode\tool-output\tool_149e34cc0001EoC8oBTRBVdsP0"

def main():
    with open(ORIGEM, "r", encoding="utf-8") as f:
        dados = json.load(f)

    linhas = [d for d in dados[1:] if str(d.get("D1N")) != "Unidade da Federação"]
    df = pd.DataFrame([{
        "uf": d["D1N"],
        "tri": str(d["D2C"]),
        "valor": pd.to_numeric(d["V"], errors="coerce"),
    } for d in linhas])
    df["ano"] = df["tri"].str[:4].astype(int)

    df = df[(df.ano >= 2016) & (df.ano <= 2025)]

    # cobertura por ano (a pandemia derrubou 2020/2021)
    print("=== COBERTURA (trimestres com dado por UF/ano) ===")
    cov = df.dropna(subset=["valor"]).groupby("ano")["tri"].nunique()
    print(cov.to_string())

    anual = (df.dropna(subset=["valor"])
               .groupby(["uf", "ano"], as_index=False)["valor"].mean()
               .rename(columns={"valor": "desemp_mulheres_pct"}))
    anual.to_csv(os.path.join(AQUI, "b1_desemprego_mulheres_uf.csv"),
                 index=False, encoding="utf-8-sig")

    w = anual.pivot(index="uf", columns="ano", values="desemp_mulheres_pct")
    w.to_csv(os.path.join(AQUI, "b1_desemprego_mulheres_uf_wide.csv"), encoding="utf-8-sig")

    print("\n=== MEDIA ANUAL DA TAXA DE DESOCUPACAO DAS MULHERES (%), amostra ===")
    print(w.round(1).head(8).to_string())
    print(f"\nSalvo: b1_desemprego_mulheres_uf.csv ({len(anual)} registros) e versao wide.")

if __name__ == "__main__":
    main()
