# -*- coding: utf-8 -*-
"""Dumpa cabecalhos das tabelas-alvo antigas para calibrar o parser."""
import pandas as pd

ALVOS = [
    (r".\feminicidio-analise\anuaries\2018_anuario_brasileiro_seguranca_publica_planilha.xlsx", "T26", "ed2018"),
    (r".\feminicidio-analise\anuaries\2019_anuario_brasileiro_seguranca_publica_planilha.xlsx", "T28", "ed2019"),
    (r".\feminicidio-analise\anuaries\2020_anuario_brasileiro_seguranca_publica_planilha.xlsx", "T37", "ed2020"),
    (r".\feminicidio-analise\anuaries\Anuario-16_vfinal_retificado_02-08 (1).xlsx", "T23", "ed16"),
]

for arq, aba, rot in ALVOS:
    df = pd.read_excel(arq, sheet_name=aba, header=None, nrows=14)
    print(f"\n===== {rot} / {aba} shape={df.shape}")
    for i in range(min(14, len(df))):
        vals = []
        for j, v in enumerate(df.iloc[i]):
            if pd.notna(v):
                vals.append(f"[{j}]{str(v)[:24]}")
        print(f" r{i:2d}: " + " | ".join(vals[:16]))
