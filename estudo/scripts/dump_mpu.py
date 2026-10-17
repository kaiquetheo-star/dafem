# -*- coding: utf-8 -*-
"""Dumpa as tabelas de medidas protetivas por UF para calibrar a extracao do B4."""
import pandas as pd

ALVOS = [
    (r".\feminicidio-analise\anuaries\anuario-2025.xlsx", "T31", "ed2025-T31-MPU distribuidas/concedidas TJ"),
    (r".\feminicidio-analise\anuaries\anuario-2025.xlsx", "T32", "ed2025-T32-Descumprimento MPU"),
    (r".\feminicidio-analise\anuaries\anuario-2025.xlsx", "T52", "ed2025-T52-MPU (2a parte?)"),
    (r".\feminicidio-analise\anuaries\anuario-2026.xlsx", "T27", "ed2026-T27-Descumprimento MPU"),
    (r".\feminicidio-analise\anuaries\anuario-2026.xlsx", "T22", "ed2026-T22-MPU ativa no obito"),
]

for arq, aba, rot in ALVOS:
    try:
        df = pd.read_excel(arq, sheet_name=aba, header=None, nrows=15)
        print(f"\n===== {rot}  shape={df.shape}")
        for i in range(min(15, len(df))):
            vals = []
            for j, v in enumerate(df.iloc[i]):
                if pd.notna(v):
                    vals.append(f"[{j}]{str(v)[:30]}")
            print(f" r{i:2d}: " + " | ".join(vals[:14]))
    except Exception as e:
        print(f"ERRO {rot}: {e}")
