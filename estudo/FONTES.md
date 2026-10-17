# Fontes e proveniência dos dados

Tudo abaixo é público e verificável. Este documento registra **exatamente** quais
arquivos, edições, tabelas e abas foram usados em cada número do estudo.

---

## 1. Anuário Brasileiro de Segurança Pública (FBSP)

Download oficial das edições (planilhas e PDFs):
https://forumseguranca.org.br/publicacoes/anuario-brasileiro-de-seguranca-publica/

Layout das tabelas por UF é idêntico em todas as edições:
coluna 0 = UF · colunas 1–5 = homicídios de mulheres · 6–10 = feminicídios · 11–12 = proporção.

### Série histórica e painel por UF (2016–2025)

Cada ano usa a tabela por UF da edição mais recente que o cobre ("edição mais
recente prevalece"):

| Edição | Arquivo oficial | Tabela | Anos cobertos |
|---|---|---|---|
| Anuário 2018 | `2018_anuario_brasileiro_seguranca_publica_planilha.xlsx` | T26 | 2016–2017 |
| Anuário 2019 | `2019_anuario_brasileiro_seguranca_publica_planilha.xlsx` | T28 | 2017–2018 |
| Anuário 2020 | `2020_anuario_brasileiro_seguranca_publica_planilha.xlsx` | T37 | 2018–2019 |
| Anuário 2022 (16ª) | `Anuario-16_vfinal_retificado.xlsx` | T23 | 2020–2021 |
| Anuário 2023 | `anuario-2023.xlsx` | T27 | 2021–2022 |
| Anuário 2024 | `anuario-2024.xlsx` | T23 | 2022–2023 |
| Anuário 2025 | `anuario-2025.xlsx` | T24 | 2023–2024 |
| Anuário 2026 | `anuario-2026.xlsx` | T21 | 2024–2025 |

**Linha "Brasil"** = série nacional do painel P06 do **Anuário 2026** (cobertura
2016–2025, já com as revisões retroativas do FBSP — ex.: 2019 revisado para
1.330 feminicídios / 3.966 homicídios de mulheres).

### Perfil racial das vítimas

| Período | Edição / aba | % vítimas negras |
|---|---|---|
| 2017–18 | Anuário 2019, painel P4 | 60,98% |
| 2019 | Anuário 2020, painel P5 | 66,57% |
| 2020–21 | Anuário 2022 (16ª), painel P08 (coluna "Feminicídio") | 61,97% |
| 2023–24 | Anuário 2025, painel P07 | 63,57% |
| 2025 | Anuário 2026, painel P06 (bloco raça/cor) | 65,08% |

### Medidas protetivas de urgência (MPU)

| Dado | Edição / tabela | Valor nacional |
|---|---|---|
| MPU concedidas (2024) | Anuário 2025, T31 | 555.001 |
| Descumprimentos (2025) | Anuário 2026, T27 | 132.025 |
| Vítimas com MPU ativa no óbito (2025) | Anuário 2026, T22 | 70 |

---

## 2. IBGE

- **PNAD Contínua trimestral** (SIDRA tabela 4093): taxa de desocupação
  (variável 4099) e taxa de informalidade (variável 12466), recorte sexo
  feminino. Média anual por UF.
  https://sidra.ibge.gov.br/tabela/4093
  Cobertura: 2016–2019 e 2022–2025 completos; 2020 só 1º tri; **2021 sem
  dado** (supressão na pandemia).
- **Censo 2022**: população feminina por cor/raça — mulheres negras são
  ~55% da população feminina (SIDRA tabela 9606).
  https://sidra.ibge.gov.br/tabela/9606

---

## 3. Regras metodológicas aplicadas

1. **Edição mais recente prevalece** — os Anuários revisam números de anos
   anteriores; sempre usamos a edição mais nova que cobre o dado.
2. **Linha "Brasil" = série nacional P06 (ed. 2026)**, não a soma das UFs —
   as revisões estaduais de anos antigos não foram publicadas (2019: soma das
   UFs dá 1.326 vs 1.330 nacional; 2017: 1.053 vs 1.075, 3 UFs sem dado).
3. **"..." (dado não declarado) = NaN** — não vira zero. 7 UF-anos afetados
   (2016–2017).
4. Correlações: **Spearman** (posto), p-valor bicaudal pela distribuição
   t (df = n−2), n = 27 UFs, média 2023–25.

---

## 4. Scripts de calibração

`scripts/dump_*.py` e `scripts/inspeciona_*.py` imprimem as linhas cruas das
tabelas/abas acima — servem para conferir qualquer número direto na planilha
original sem abrir o Excel.
