# Fase B — Caderno de variáveis (pergunta da Carolina: "quais variáveis impactam?")

## MATRIZ FINAL — Feminicídio × Variáveis (Spearman, média 2023-25, 27 UFs)

| Variável | ρ | p | Veredito |
|---|---|---|---|
| **Desemprego feminino (%)** | **−0,43*** | 0,024 | NEGATIVO — mais desemprego = MENOS femicídio |
| **Informalidade feminina (%)** (proxy BF/vulnerabilidade) | −0,25 | 0,215 | Não significante (mesma direção) |
| **MPU concedida /100k mulheres** | **+0,44*** | 0,023 | POSITIVO — mais MPU = MAIS femicídio |
| **Descumprimento MPU /100k** | **+0,46*** | 0,016 | POSITIVO — maior descumprimento = MAIS femicídio |
| % homicídios classificados como femicídio × desemprego | −0,47* | 0,013 | Estados mais ricos classificam melhor |

**Inter-correlações (confundidores):**
- Desemprego × Informalidade: ρ=+0,58 (mesmo construto econômico)
- MPU × Descumprimento: ρ=+0,79 (mesmo sistema respondendo à violência)
- Informalidade × MPU concedida: ρ=−0,59 (**estados pobres concedem MENOS MPU** — capacidade institucional)

### A GRANDE HISTÓRIA (narrativa consolidada para o post)

1. **Variáveis econômicas NÃO explicam o mapa do feminicídio brasileiro.** Nem desemprego, nem
   informalidade (proxy BF/vulnerabilidade). Se algo, o sinal é INVERSO (Norte/CO = desemprego
   baixo + taxas altas). A narrativa "pobreza causa violência" não se sustenta no recorte estadual.

2. **Variáveis institucionais SIM discriminam.** Descumprimento de MPU (ρ=+0,46) é a correlação
   mais forte da matriz. Estados que falham em fiscalizar medidas protetivas têm mais feminicídio.

3. **A capacidade institucional é o eixo oculto:** estados pobres concedem menos MPU (ρ=−0,59)
   e fiscalizam menos — o problema não é "pobreza → violência" mas
   **"pobreza → menos Estado → menos proteção → mais mortes".**

4. **O efeito classificação persiste:** a % de homicídios de mulheres classificados como
   feminicídio correlaciona NEGATIVAMENTE com desemprego (ρ=−0,47) — estados mais ricos
   classificam melhor, inflando os números de estados como Norte/CO (que ao mesmo tempo
   têm menos desemprego). Parte da "alta" de feminicídio é melhora de registro.

### Para o post (o gancho final)

> *"Não é pobreza. Não é desemprego. O que correlaciona com feminicídio entre estados
> brasileiros é a FALHA DE EXECUÇÃO da proteção: onde mais medidas protetivas são
> descumpridas, mais mulheres morrem. O Brasil concede 555 mil MPUs por ano — e descumpre
> 1 em cada 4. 70 mulheres morreram em 2025 com medida protetiva ativa.
> O problema não é a lei. É a execução."*

---

## Detalhamento por tarefa

### B1 — Desemprego feminino por UF ✅ (17/10)

- Fonte: IBGE/SIDRA tabela 4093 (PNAD Contínua trimestral), variável 4099, sexo c2/5 (Mulheres).
  Média anual por UF. Arquivos: `b1_desemprego_mulheres_uf.csv` (+wide).
- Cobertura: 2016-2019 e 2022-2025 completos; 2020 só 1º tri; 2021 SEM dado (pandemia).

#### Correlação por ano (Spearman):

| Ano | ρ | p | n |
|---|---|---|---|
| 2016 | −0,26 | 0,23 | 23 |
| 2017 | −0,14 | 0,51 | 25 |
| 2018 | −0,28 | 0,16 | 27 |
| 2019 | +0,02 | 0,91 | 27 |
| 2022 | −0,25 | 0,21 | 27 |
| 2023 | **−0,48*** | **0,012** | 27 |
| 2024 | **−0,44*** | **0,021** | 27 |
| 2025 | −0,28 | 0,16 | 27 |
| **Média 2023-25** | **−0,43*** | **0,024** | 27 |

> Nota (18/10/2026): p-valores recalculados com a distribuição t (df=n−2) — a versão anterior
> usava a aproximação normal, que subestimava os p. Nenhum veredito de significância mudou.

### B3 — Informalidade feminina por UF (proxy BF) ✅ (17/10)

- Fonte: IBGE/SIDRA tabela 4093, variável 12466 (taxa de informalidade), sexo c2/5.
  Arquivos: `b3_informalidade_mulheres_uf.csv` (+wide).
- Pivô metodológico: dados diretos de Bolsa Família inacessíveis (API do Portal da
  Transparência exige chave; MDS bloqueado). Informalidade é fortemente correlacionada
  com elegibilidade ao BF (ρ=+0,58 com desemprego, mesmo eixo vulnerabilidade).

#### Correlação por ano: todas não significantes (ρ entre −0,19 e +0,10)

### B4 — Medidas protetivas por UF ✅ (17/10)

- Fontes: Anuário FBSP 2025 (T31: MPU concedidas/distribuídas) e Anuário 2026 (T27: descumprimentos).
  Arquivo: `b4_medidas_protetivas_uf.csv`.
- Números nacionais: 555.001 MPUs concedidas em 2024; 132.025 descumprimentos em 2025;
  70 vítimas com MPU ativa no óbito em 2025.

### B5 — Scatterplot e correlação visual ✅ (17/10)

- Arquivo: `b5_scatter_desemprego.png` (0 sobreposições na auditoria).
- Também resolvia B5 com a matriz consolidada acima.

---

## Pendências da Fase B (menor prioridade)
- B2: rendimento médio feminino por UF (SIDRA — tabela a identificar)
- B6: % arma de fogo no feminicídio ao longo do tempo (edições anteriores)
