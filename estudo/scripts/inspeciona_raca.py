# -*- coding: utf-8 -*-
"""Inspeciona painéis de todos os anuários procurando dados de RAÇA em feminicídios."""
import pandas as pd
import glob
import os

ARQUIVOS = [
    (r".\feminicidio-analise\anuaries\2018_anuario_brasileiro_seguranca_publica_planilha.xlsx", "ed2018"),
    (r".\feminicidio-analise\anuaries\2019_anuario_brasileiro_seguranca_publica_planilha.xlsx", "ed2019"),
    (r".\feminicidio-analise\anuaries\2020_anuario_brasileiro_seguranca_publica_planilha.xlsx", "ed2020"),
    (r".\feminicidio-analise\anuaries\Anuario-16_vfinal_retificado_02-08 (1).xlsx", "ed16"),
    (r".\feminicidio-analise\anuaries\anuario-2023.xlsx", "ed2023"),
    (r".\feminicidio-analise\anuaries\anuario-2024.xlsx", "ed2024"),
    (r".\feminicidio-analise\anuaries\anuario-2025.xlsx", "ed2025"),
    (r".\feminicidio-analise\anuario-2026.xlsx", "ed2026"),
]

for arq, rot in ARQUIVOS:
    if not os.path.exists(arq):
        print(f"--- {rot}: ARQUIVO NAO ENCONTRADO")
        continue
    try:
        xl = pd.ExcelFile(arq)
        achados = []
        for s in xl.sheet_names:
            df = xl.parse(s, header=None, nrows=5)
            titulo = " ".join(str(c) for linha in df.values.tolist() for c in linha if pd.notna(c)).lower()
            if ("raça" in titulo or "raca" in titulo or "cor" in titulo.lower() or "negra" in titulo
                    or "perfil" in titulo and "feminicídio" in titulo):
                # le mais linhas do painel pra ver se tem serie temporal
                df_full = xl.parse(s, header=None, nrows=25)
                tem_serie = any("2016" in str(v) or "2017" in str(v) or "2018" in str(v)
                                or "2019" in str(v) or "2020" in str(v) or "2021" in str(v)
                                or "2022" in str(v) or "2023" in str(v)
                                for linha in df_full.values.tolist() for v in linha if pd.notna(v))
                titulo_curto = titulo[:120]
                achados.append((s, titulo_curto, tem_serie))
        if achados:
            print(f"\n--- {rot} ({len(achados)} achados):")
            for s, t, serie in achados:
                marca_serie = " <<< TEM SÉRIE TEMPORAL" if serie else ""
                print(f"   {s:8s} {t}{marca_serie}")
        else:
            print(f"\n--- {rot}: nenhum painel de raça/perfil encontrado")
    except Exception as e:
        print(f"\n--- {rot}: ERRO {e}")
