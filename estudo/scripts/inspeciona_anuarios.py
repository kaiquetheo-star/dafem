# -*- coding: utf-8 -*-
"""Inspeciona abas dos anuarios: acha tabelas de feminicidio por UF e quantos anos cada uma traz."""
import pandas as pd
import glob
import os

ARQS = sorted(glob.glob(r".\feminicidio-analise\anuaries\anuario-*.xlsx"))
ARQS.append(r".\feminicidio-analise\anuario-2026.xlsx")

for f in ARQS:
    nome = os.path.basename(f)
    try:
        xl = pd.ExcelFile(f)
        print(f"=== {nome} ({len(xl.sheet_names)} abas)")
        for s in xl.sheet_names:
            df = xl.parse(s, header=None, nrows=4)
            titulo = " / ".join(str(c) for linha in df.values.tolist() for c in linha if pd.notna(c))[:120]
            marca = "  <<<< FEMINICIDIO/UF" if ("eminic" in titulo) else ""
            print(f"   {s:8s} {titulo}{marca}")
    except Exception as e:
        print(f"ERRO {nome}: {e}")
