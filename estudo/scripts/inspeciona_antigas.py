# -*- coding: utf-8 -*-
"""Inspeciona as planilhas antigas (2018/2019/2020/16a ed): abas com feminicidio/UF."""
import pandas as pd
import os

AQUI = r".\feminicidio-analise\anuaries"
ARQS = [
    "2018_anuario_brasileiro_seguranca_publica_planilha.xlsx",
    "2019_anuario_brasileiro_seguranca_publica_planilha.xlsx",
    "2020_anuario_brasileiro_seguranca_publica_planilha.xlsx",
    "Anuario-16_vfinal_retificado_02-08 (1).xlsx",
]

for arq in ARQS:
    caminho = os.path.join(AQUI, arq)
    try:
        xl = pd.ExcelFile(caminho)
        print(f"\n===== {arq} ({len(xl.sheet_names)} abas)")
        for s in xl.sheet_names:
            df = xl.parse(s, header=None, nrows=4)
            titulo = " / ".join(str(c) for linha in df.values.tolist() for c in linha if pd.notna(c))[:130]
            if "eminic" in titulo.lower() or "omicídios de mulheres" in titulo:
                print(f"   {s:12s} {titulo}   <<<< ALVO")
    except Exception as e:
        print(f"ERRO {arq}: {e}")
