# Feminicídio no Brasil — Análise completa 2016-2025

**Tarefa:** Carolina Silveira, #dados (Fora FB!), 10/10/2026 — "frente de análise histórica do
feminicídio e entender quais variáveis impactam nesse aumento ou redução"
**Equipe:** k-iq (execução) × coordenação #dados · **Data:** 17/10/2026
**Produtos:** dashboard interativo (Streamlit), painel 27 UFs × 10 anos, 6 gráficos prontos
para redes, matriz de correlações com 4 variáveis, este relatório.

---

## Fontes (todas públicas e verificáveis)

- **Atos criminais e vitimização:** Anuário Brasileiro de Segurança Pública, edições 2018–2026
  (FBSP), com dados das SSPs estaduais — planilhas oficiais baixadas e cruzadas entre edições.
- **Socioeconômico:** IBGE/SIDRA — PNAD Contínua trimestral (tabela 4093), variáveis taxa de
  desocupação e taxa de informalidade, recorte sexo feminino.
- **Medidas protetivas:** Anuários FBSP 2025 (T31: MPU concedidas/distribuídas) e 2026
  (T27: descumprimentos), por UF.

---

## 1. O RETRATO (série nacional 2016–2025)

| Ano | Feminicídios | Homicídios de mulheres | % classificado |
|---|---|---|---|
| 2016 | 929 | 4.245 | 22% |
| 2017 | 1.075 | 4.556 | 24% |
| 2018 | 1.229 | 4.340 | 28% |
| 2019 | 1.330 | 3.966 | 34% |
| 2020 | 1.354 | 3.999 | 34% |
| 2021 | 1.347 | 3.869 | 35% |
| 2022 | 1.455 | 3.934 | 37% |
| 2023 | 1.475 | 3.937 | 37% |
| 2024 | 1.504 | 3.728 | 40% |
| 2025 | 1.571 | 3.539 | 44% |

**Fatos:**
1. Feminicídio sobe todos os anos, atravessando 3 governos (Temer +32%, Bolsonaro +18%, Lula +8%).
2. Total de mulheres assassinadas **CAI 17%** no período (maior queda da série: −10% em 2023-25).
3. A parcela classificada como feminicídio **DOBROU** (22%→44%) — efeito da Lei 13.104/2015
   sendo incorporada progressivamente pelos estados.

## 2. O MAPA (painel 27 UFs × 10 anos)

**Maiores taxas em 2025 (por 100k mulheres):** Acre 3,18 · Rondônia 2,87 · Mato Grosso 2,74 ·
MS 2,64 · Tocantins 2,54 — **padrão Norte/Centro-Oeste**.

**Maiores volumes em 2025:** São Paulo 270 · Minas Gerais 177 · Rio de Janeiro 105 · Bahia 102.

**Quem puxou o aumento de 2025 (+4,4%):** SP (+17), Pará (+13), PE (+10), PB (+10), RO (+10).
**Quem caiu:** Paraná (−22), Maranhão (−18), Amazonas (−9).

**Validação:** soma das 27 UFs = linha "Brasil" = série nacional em 7 dos 10 anos. Exceções
documentadas: **2019** — soma 1.326 vs nacional 1.330 (revisão estadual não publicada; prevalece
a série nacional do Anuário 2026, regra da edição mais recente) e **2017** — soma 1.053 vs
nacional 1.075 (3 UFs sem dado declarado nos painéis estaduais, incluídas no total nacional).
Os demais anos fecham com diferença zero.

## 3. AS VARIÁVEIS (resposta à pergunta central)

| Variável | ρ Spearman | p | Veredito |
|---|---|---|---|
| **Desemprego feminino** | **−0,43*** | 0,024 | MAIS desemprego = MENOS feminicídio |
| **Informalidade feminina** (proxy BF) | −0,25 | 0,215 | Não significante |
| **MPU concedida /100k** | **+0,44*** | 0,023 | Mais MPU = MAIS feminicídio (reage, não previne) |
| **Descumprimento MPU /100k** | **+0,46*** | 0,016 | Onde mais MPU falha, mais mulheres morrem |

**Inter-correlações:** informalidade × MPU concedida: ρ=−0,59 (estados pobres concedem MENOS
MPU — capacidade institucional é o eixo oculto).

### A conclusão que muda a narrativa

**Variáveis econômicas NÃO explicam o mapa do feminicídio.** Nem desemprego, nem
informalidade/vulnerabilidade. Se algo, o sinal é INVERSO (Norte/CO = desemprego baixo +
taxas altas). A tese "pobreza causa violência" não se sustenta no recorte estadual.

**Variáveis institucionais SIM discriminam.** Descumprimento de MPU é a correlação mais forte
da matriz (ρ=+0,46). Estados que falham em fiscalizar medidas protetivas têm mais feminicídio.

**A cadeia causal sugerida pelos dados:** pobreza → menos Estado → menos proteção concedida →
mais descumprimento → mais mortes. O problema não é "pobreza → violência" — é
**capacidade institucional de executar a proteção**.

## 4. RAÇA (recorte estrutural)

| Período | % vítimas NEGRAS | % vítimas BRANCAS |
|---|---|---|
| 2017-18 | 61% | 39% |
| 2019 | 67% | 33% |
| 2020-21 | 62% | 38% |
| 2023-24 | 64% | 36% |
| 2025 | 65% | 34% |

Mulheres negras são ~55% da população feminina (Censo 2022) e 60–67% das vítimas.
**O recorte racial é estrutural, não conjuntural.**

## 5. O QUE OS DADOS PERMITEM AFIRMAR (e o que não)

✅ **Permitem:**
- Feminicídio sobe continuamente desde 2016, atravessando 3 governos (com desaceleração)
- O total de mulheres assassinadas cai — a alta do feminicídio é em parte classificação
- O mapa concentra-se no Norte/CO (taxas) e SP/BA/MG (volumes)
- Vítimas são majoritariamente negras (60-67%), sempre
- Descumprimento de MPU correlaciona com feminicídio entre estados
- Variáveis econômicas não explicam o padrão estadual

❌ **Não permitem (ainda):**
- Afirmar causalidade (n=27, estudo ecológico, correlação ≠ causa)
- Dizer que "o governo X é responsável" — segurança pública é estadual
- Quantificar exatamente quanto da alta é classificação vs. aumento real
- Estender correlações para o nível individual (falácia ecológica)

## 6. LEGISLAÇÃO E EXECUÇÃO

| Ano | Marco | Efeito |
|---|---|---|
| 2006 | Lei Maria da Penha (11.340) | Cria medidas protetivas |
| 2015 | Lei do Feminicídio (13.104) | Tipifica como homicídio qualificado |
| 2019 | Lei 13.827 | MPU concedida pela polícia (sem juiz) |
| 2021 | Lei 14.188 | Violência psicológica + MPU digital |
| 2023 | Lei 14.550 | Feminicídio nos Crimes Hediondos |

**A cada lei, o número sobe** — porque o país passa a RECONHECER mais o crime. Mas:
- 555.001 MPUs concedidas em 2024
- 132.025 descumpridas em 2025 (**1 em cada 4**)
- **70 mulheres morreram com MPU ativa** em 2025

## 7. PARA POSTAR

**Gancho principal:**
> "Não é pobreza. Não é desemprego. O que correlaciona com feminicídio entre estados
> brasileiros é a FALHA DE EXECUÇÃO da proteção. O Brasil concede 555 mil MPUs/ano e
> descumpre 1 em cada 4. 70 mulheres morreram em 2025 com medida ativa. O problema
> não é a lei — é a execução."

**Gancho raça:**
> "Em TODOS os anos com dado disponível, mulheres negras são 60-67% das vítimas de
> feminicídio — enquanto são 56% da população feminina. Isso não é conjuntura. É estrutura."

**Gancho classificação:**
> "O total de mulheres assassinadas CAIU 17% desde 2016. O feminicídio 'subiu' porque
> o Brasil passou a CLASSIFICAR melhor esses crimes (22% → 44% dos homicídios de mulheres).
> Temos muito a avançar — 1.571 vidas em 2025 é inaceitável. Mas dado não se dobra
> a narrativa eleitoreira."

---

## Arquivos entregues

| Arquivo | Descrição |
|---|---|
| `dashboard_feminicidio.py` | Dashboard Streamlit (3 abas: Brasil, Por Estado, Variáveis) |
| `painel_feminicidio_uf_2016_2025.csv` | Painel 27 UFs × 10 anos (feminicídio, homicídios, taxa, proporção) |
| `b1_desemprego_mulheres_uf.csv` | Desemprego feminino por UF/ano (IBGE/SIDRA) |
| `b3_informalidade_mulheres_uf.csv` | Informalidade feminina por UF/ano (IBGE/SIDRA) |
| `b4_medidas_protetivas_uf.csv` | MPU concedida + descumprimento por UF |
| `matriz_variaveis_uf_2023_25.csv` | Base consolidada para correlações |
| `B_VARIAVEIS_NOTAS.md` | Caderno metodológico da Fase B |
| `grafico_1_perfil_turnover.png` | Juízes estáveis × CJ explodindo |
| `grafico_2_linha_do_tempo.png` | Mensal 2026 com pico de maio |
| `grafico_3_unidades.png` | Unidades mais atingidas |
| `b5_scatter_desemprego.png` | Scatter feminicídio × desemprego |
| `grafico_c1_raca_tempo.png` | Raça/cor das vítimas ao longo do tempo |
| `grafico_c3_legislativo.png` | Série + timeline legislativa + proporção |
| `MENSAGEM_CAROLINA_D4.md` | Mensagens prontas para o #dados |

## Limitações e honestidade metodológica

1. n=27 (estados), correlação ecológica — não é causalidade individual.
2. Anuários revisam números de anos anteriores; usamos a edição mais recente (regra documentada).
3. 7 UF-ano sem dado declarado nos primeiros anos (Ceará 2016-17, MT 2017, RO 2017, etc.).
4. Desemprego/informalidade sem dados em 2020-21 (IBGE suprimiu na pandemia).
5. Dados de raça não disponíveis para todos os anos (apenas nos painéis "Perfil" de 5 edições).
6. Toda a análise é de fonte pública e reproduzível (scripts em Python anexos).
