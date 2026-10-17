# -*- coding: utf-8 -*-
"""Dumpa o cabecalho bruto das tabelas-alvo para calibrar o extrator."""
import pandas as pd

ALVOS = [
    (r".\feminicidio-analise\anuaries\anuario-2023.xlsx", "T27", "ed2023"),
    (r".\feminicidio-analise\anuaries\anuario-2024.xlsx", "T23", "ed2024"),
    (r".\feminicidio-analise\anuaries\anuario-2025.xlsx", "T24", "ed2025"),
    (r".\feminicidio-analise\anuario-2026.xlsx", "T21", "ed2026"),
]

for arq, aba, rot in ALVOS:
    df = pd.read_excel(arq, sheet_name=aba, header=None, nrows=13)
    print(f"\n===== {rot} / {aba}  shape={df.shape}")
    for i in range(min(13, len(df))):
        vals = []
        for j, v in enumerate(df.iloc[i]):
            if pd.notna(v):
                vals.append(f"[{j}]{str(v)[:26]}")
        print(f" r{i:2d}: " + " | ".join(vals[:16]))
