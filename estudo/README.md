# Estudo completo — Feminicídio no Brasil 2016–2025

Esta pasta contém **tudo que sustenta os números do DaFem**: relatório, gráficos
prontos, dados de apoio e os scripts que geraram cada número. Nada aqui é caixa-preta.

> **Proveniência exata de cada fonte** (edições, tabelas, abas e links de download
> dos Anuários FBSP e do IBGE): veja [FONTES.md](FONTES.md).

```
estudo/
├── FONTES.md                    ← proveniência exata de cada número
├── relatorio/
│   ├── RELATORIO_FINAL.md       ← relatório completo (série, mapa, variáveis, raça)
│   ├── RESUMO_ANALISE.md        ← resumo da série nacional + argumentos centrais
│   ├── B_VARIAVEIS_NOTAS.md     ← caderno metodológico das variáveis/correlações
│   └── KIT_POSTS.md             ← 6 cards prontos para redes
├── dados/
│   ├── serie_feminicidio_brasil_2016_2025.csv   ← série nacional (Anuário 2026, P06)
│   └── b5_correlacao_por_ano.csv                ← Spearman desemprego × feminicídio por ano
├── graficos/                    ← 6 gráficos prontos para redes (PNG)
└── scripts/                     ← extração, painel, correlações e gráficos (Python)
```

Os dados que alimentam o **dashboard** são os 5 CSVs na raiz do repositório
(`painel_feminicidio_uf_2016_2025.csv`, `b1_*`, `b3_*`, `b4_*`, `matriz_*`) —
validados contra as planilhas oficiais (ver FONTES.md).

## Como reproduzir

1. Baixe as planilhas oficiais dos Anuários (links em [FONTES.md](FONTES.md))
   e organize a pasta local assim: planilhas dentro de `anuaries/`,
   scripts e CSVs no mesmo nível.
2. Dependências: `pip install pandas matplotlib openpyxl`
3. Ordem de execução:
   - `analise_feminicidio.py` — série nacional (lê a P06 do Anuário 2026)
   - `monta_painel_uf.py` — painel 27 UFs × 10 anos (regra da edição mais recente)
   - `b1/b3/b4_*.py` + `b5_correlacoes.py` — variáveis e correlações
   - `graficos_c1_c3.py` — gráficos de raça e legislativo

> Os scripts foram escritos para a pasta local de análise e assumem os caminhos
> acima — não rodam de dentro do repositório sem baixar as planilhas primeiro.
> `dump_*.py` / `inspeciona_*.py` imprimem as linhas cruas das tabelas para
> conferência número a número.

## Avisos

- Correlação entre estados não prova causa individual (estudo ecológico, n=27).
- Segurança pública é competência estadual — nada aqui atribui resultado a um
  governo federal específico.
- Dados públicos (FBSP + IBGE/SIDRA), análise própria: Squad de Dados — Fora FB!

---

Squad de Dados — Fora FB! · Outubro 2026
