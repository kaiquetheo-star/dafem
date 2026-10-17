# -*- coding: utf-8 -*-
"""Dumpa os painéis de PERFIL dos feminicídios (raça/cor) de cada edição."""
import pandas as pd

ALVOS = [
    (r".\feminicidio-analise\anuaries\2019_anuario_brasileiro_seguranca_publica_planilha.xlsx", "P4", "ed2019-P4 Perfil Fem 2017-2018"),
    (r".\feminicidio-analise\anuaries\2020_anuario_brasileiro_seguranca_publica_planilha.xlsx", "P5", "ed2020-P5 Perfil Fem 2019"),
    (r".\feminicidio-analise\anuaries\Anuario-16_vfinal_retificado_02-08 (1).xlsx", "P08", "ed16-P08 Perfil Fem/MVI 2020-2021"),
    (r".\feminicidio-analise\anuaries\anuario-2025.xlsx", "P07", "ed2025-P07 Viol. mulheres (raça)"),
]

for arq, aba, rot in ALVOS:
    try:
        df = pd.read_excel(arq, sheet_name=aba, header=None, nrows=40)
        print(f"\n===== {rot}  shape={df.shape}")
        for i in range(min(40, len(df))):
            vals = []
            for j, v in enumerate(df.iloc[i]):
                if pd.notna(v):
                    vals.append(f"[{j}]{str(v)[:35]}")
            if vals:
                print(f" r{i:2d}: " + " | ".join(vals[:10]))
    except Exception as e:
        print(f"ERRO {rot}: {e}")
