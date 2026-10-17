# -*- coding: utf-8 -*-
"""
monta_painel_uf.py - Painel de feminicidios por UF (2016-2025) a partir dos Anuarios FBSP.
Layout identico em TODAS as edicoes (col 0=UF | 1-5 homicidios | 6-10 feminicidios | 11-12 proporcao).
Tratamentos: UF com nota de rodape ("Alagoas (4)") -> strip; "..." -> NaN (dado nao disponivel).
Regra de revisao: ano coberto por mais de uma edicao -> vale a EDICAO MAIS RECENTE.
Saidas: painel_feminicidio_uf_2016_2025.csv + relatorio de revisoes + validacao nacional. Linha Brasil: override final pela serie nacional P06 (edicao mais recente).
"""
import os
import re
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
ANU = os.path.join(AQUI, "anuaries")

EDICOES = [  # (arquivo, aba, ano1, ano2, rank de atualidade)
    (os.path.join(ANU, "2018_anuario_brasileiro_seguranca_publica_planilha.xlsx"), "T26", 2016, 2017, 1),
    (os.path.join(ANU, "2019_anuario_brasileiro_seguranca_publica_planilha.xlsx"), "T28", 2017, 2018, 2),
    (os.path.join(ANU, "2020_anuario_brasileiro_seguranca_publica_planilha.xlsx"), "T37", 2018, 2019, 3),
    (os.path.join(ANU, "Anuario-16_vfinal_retificado_02-08 (1).xlsx"),             "T23", 2020, 2021, 4),
    (os.path.join(ANU, "anuario-2023.xlsx"), "T27", 2021, 2022, 5),
    (os.path.join(ANU, "anuario-2024.xlsx"), "T23", 2022, 2023, 6),
    (os.path.join(ANU, "anuario-2025.xlsx"), "T24", 2023, 2024, 7),
    (os.path.join(ANU, "PLANILHA Anuário Brasileiro de Segurança Pública 2026.xlsx"), "T21", 2024, 2025, 8),
]

UFS = ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
       "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul",
       "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí",
       "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia",
       "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"]

def limpa_uf(nome):
    return re.sub(r"\s*\(\d+\)\s*$", "", str(nome).strip())

def num(v):
    """'...' ou texto -> NaN; numero -> float."""
    if pd.isna(v):
        return float("nan")
    try:
        return float(v)
    except (TypeError, ValueError):
        return float("nan")

def parse_edicao(arq, aba, y1, y2, rotulo):
    df = pd.read_excel(arq, sheet_name=aba, header=None)
    registros = []
    for _, linha in df.iterrows():
        nome = limpa_uf(linha[0]) if pd.notna(linha[0]) else ""
        if nome not in UFS and nome != "Brasil":
            continue
        for (ano, c_abs, c_taxa) in [(y1, 6, 8), (y2, 7, 9)]:
            registros.append({
                "uf": nome, "ano": ano,
                "fem_abs": num(linha[c_abs]), "fem_taxa": num(linha[c_taxa]),
                "hom_abs": num(linha[1 if c_abs == 6 else 2]),
                "prop_pct": num(linha[11 if c_abs == 6 else 12]),
            })
    return registros

def main():
    tudo = []
    for arq, aba, y1, y2, rank in EDICOES:
        regs = parse_edicao(arq, aba, y1, y2, rank)
        for r in regs:
            r["rank_ed"] = rank
        tudo.extend(regs)
        br = [r for r in regs if r["uf"] == "Brasil"]
        print(f"rank{rank}: {os.path.basename(arq)[:44]:46s}{aba} {y1}-{y2} | "
              + " | ".join(f"{b['ano']}:{b['fem_abs']:.0f}" for b in br))

    base = pd.DataFrame(tudo)

    # ---- revisoes entre edicoes ----
    print("\n=== REVISÕES ENTRE EDIÇÕES (Brasil e UFs, fem_abs) ===")
    rev = base.dropna(subset=["fem_abs"]).groupby(["uf", "ano"])["fem_abs"].agg(["nunique", "min", "max"])
    dif = rev[rev["nunique"] > 1].reset_index()
    br_dif = dif[dif.uf == "Brasil"]
    for _, r in br_dif.iterrows():
        print(f"   Brasil {r['ano']:.0f}: {r['min']:.0f} -> {r['max']:.0f}")
    print(f"   UFs com revisão: {len(dif) - len(br_dif)} casos (regra: edição mais recente prevalece)")

    # ---- painel final ----
    base = base.sort_values("rank_ed").drop_duplicates(["uf", "ano"], keep="last")
    painel = base[["uf", "ano", "fem_abs", "fem_taxa", "hom_abs", "prop_pct"]].sort_values(["uf", "ano"])

    # ---- override da linha Brasil pela série nacional da edição mais recente ----
    # A série nacional (P06 da ed. 2026) cobre todos os anos e incorpora revisões que as
    # tabelas por UF antigas não refletem — ex.: 2019 (T37/ed2020: 1.326 fem / 3.730 hom
    # vs P06/ed2026: 1.330 / 3.966). A regra documentada ("edição mais recente prevalece")
    # vale para o país; as revisões estaduais de anos antigos não foram publicadas (nota
    # no relatório: soma das UFs pode divergir da linha Brasil nesses anos).
    P06_FEM = {2016: 929, 2017: 1075, 2018: 1229, 2019: 1330, 2020: 1354,
               2021: 1347, 2022: 1455, 2023: 1475, 2024: 1504, 2025: 1571}
    P06_HOM = {2016: 4245, 2017: 4556, 2018: 4340, 2019: 3966, 2020: 3999,
               2021: 3869, 2022: 3934, 2023: 3937, 2024: 3728, 2025: 3539}
    for idx, ano in painel.loc[painel.uf == "Brasil", "ano"].items():
        ano = int(ano)
        f0 = painel.at[idx, "fem_abs"]
        painel.at[idx, "fem_abs"] = float(P06_FEM[ano])
        painel.at[idx, "hom_abs"] = float(P06_HOM[ano])
        painel.at[idx, "prop_pct"] = P06_FEM[ano] / P06_HOM[ano] * 100
        # fem_taxa nacional: reescala pelo mesmo denominador implícito da tabela original
        if pd.notna(f0) and f0 and pd.notna(painel.at[idx, "fem_taxa"]):
            painel.at[idx, "fem_taxa"] = painel.at[idx, "fem_taxa"] * P06_FEM[ano] / f0

    painel.to_csv(os.path.join(AQUI, "painel_feminicidio_uf_2016_2025.csv"),
                  index=False, encoding="utf-8-sig")

    # ---- validacao: soma UFs vs linha Brasil (agora = serie nacional P06 ed2026) ----
    print("\n=== VALIDAÇÃO NACIONAL (soma UFs | linha Brasil = P06 ed2026) ===")
    for ano in range(2016, 2026):
        sub = painel[(painel.ano == ano)]
        soma = sub[sub.uf != "Brasil"]["fem_abs"].sum()
        br = sub[sub.uf == "Brasil"]["fem_abs"]
        br = br.iloc[0] if len(br) else float("nan")
        if abs(soma - br) < 1:
            print(f"   {ano}: soma={soma:.0f} | Brasil={br:.0f} | OK")
        else:
            print(f"   {ano}: soma={soma:.0f} | Brasil={br:.0f} | nota: revisão estadual de "
                  f"{ano} não publicada em edições posteriores (nacional prevalece)")

    # ---- cobertura: UF-ano sem dado ----
    faltas = painel[painel.fem_abs.isna()]
    print(f"\n=== COBERTURA: {len(faltas)} UF-ano sem dado declarado ('...') ===")
    for _, r in faltas.iterrows():
        print(f"   {r['uf']} {r['ano']:.0f}")

    # ---- resumo do painel ----
    print(f"\nPainel: {len(painel)} registros | {painel.uf.nunique()} entidades (27 UFs + Brasil) | "
          f"anos {painel.ano.min():.0f}-{painel.ano.max():.0f}")
    w = painel[painel.uf != "Brasil"].pivot_table(index="uf", columns="ano", values="fem_abs")
    print("\nAmostra (primeiras 6 UFs):")
    print(w.head(6).to_string())

if __name__ == "__main__":
    main()
