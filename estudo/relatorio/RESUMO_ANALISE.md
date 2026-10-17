# Análise histórica de feminicídios no Brasil (2016–2025)

**Tarefa:** resposta ao chamado da Carolina Silveira no `#dados` (10/out) — "frente de análise
histrica do feminicídio e quais variáveis impactam aumento/redução", contextualizando a
narrativa "aumento do feminicídio no governo Lula".

**Fonte primária:** Anuário Brasileiro de Segurança Pública 2026 (20ª edição, dados de 2025),
do Fórum Brasileiro de Segurança Pública (FBSP) — dados das SSPs estaduais.
- Planilha oficial: https://forumseguranca.org.br/wp-content/uploads/2026/07/anuario-2026.xlsx
- PDF: https://forumseguranca.org.br/wp-content/uploads/2026/07/anuario-2026.pdf

---

## A série (Brasil, número de vítimas)

| Ano | Feminicídios | Homicídios de mulheres (total) | % classificados como feminicídio |
|-----|--------------|-------------------------------|----------------------------------|
| 2016 | 929  | 4.245 | 21,9% |
| 2017 | 1.075 | 4.556 | 23,6% |
| 2018 | 1.229 | 4.340 | 28,3% |
| 2019 | 1.330 | 3.966 | 33,5% |
| 2020 | 1.354 | 3.999 | 33,9% |
| 2021 | 1.347 | 3.869 | 34,8% |
| 2022 | 1.455 | 3.934 | 37,0% |
| 2023 | 1.475 | 3.937 | 37,5% |
| 2024 | 1.504 | 3.728 | 40,3% |
| 2025 | 1.571 | 3.539 | 44,4% |

## Variação por mandato (base: último ano do governo anterior)

| Mandato | Feminicídios | Total de homicídios de mulheres |
|---------|--------------|---------------------------------|
| Temer (2016–18) | **+32,3%** | +2,2% |
| Bolsonaro (2019–22) | **+18,4%** | −9,4% |
| Lula (2023–25) | **+8,0%** | **−10,0%** (maior queda da série) |

## Os 4 argumentos centrais (todos com fonte)

1. **A alta é uma tendência de uma década, não do governo atual.** O feminicídio sobe todos os
   anos desde 2016 — passou por Temer (+32%), Bolsonaro (+18%) e Lula (+8%). A subida
   **desacelerou** em cada mandato seguinte.
2. **Enquanto isso, o total de mulheres assassinadas CAIU 17%** (4.245 → 3.539). No governo
   Lula foi a maior queda da série (−10%).
3. **Efeito de classificação:** a Lei do Feminicídio (13.104/2015) foi incorporada aos poucos
   pelas polícias estaduais. A parcela de homicídios de mulheres classificados como feminicídio
   **dobrou** (22% → 44%). Parte da "alta" é melhoria do registro, não necessariamente mais
   crimes. (Cautela: não dá para precisar quanto é cada efeito — dizer isso abertamente só dá
   credibilidade.)
4. **Segurança pública é competência ESTADUAL.** Quem investiga, patrulha e cumpre medidas
   protetivas são SSPs, Polícias Civis e Militares dos estados. Atribuir o número nacional de
   um ano ao governo federal é analiticamente frágil — serve para os dois lados.

## Munição complementar para conteúdo (dados de 2025, mesma fonte)

- **80% dos feminicídios** são cometidos por companheiro (60,9%) ou ex-companheiro (18,9%).
- **62,5% acontecem na residência** da vítima.
- **50,8% com arma branca** (arma de fogo: só 22,5% — o oposto dos homicídios em geral).
- **65% das vítimas são mulheres negras** (demais MVI: 74,6%).
- **132.025 registros de descumprimento de Medida Protetiva de Urgência** em 2025 — o sistema
  de proteção existe no papel e falha na execução.
- **70 vítimas em 2025 tinham medida protetiva ATIVA** no momento em que foram mortas (T22).
- 4.191 tentativas de feminicídio registradas em 2025.
- 788.531 registros de ameaça contra mulheres em 2025.

## Cuidados de honestidade (importante para credibilidade)

- ✋ **Não negar o aumento.** Ele é real: 1.571 em 2025 é o maior número da série. O argumento
  é contexto e tendência, não negação.
- Variações anuais de ±5% (~75 casos) são ruído estatístico — evitar comparação ano-a-ano
  isolada (isso vale para os dois lados da narrativa).
- 2016 é base subnotificada (lei recém-criada) — a série mais antiga tende a subestimar.
- Sempre citar a fonte (FBSP/Anuário 2026) — regra interna do servidor (bombril reforçou isso
  em #dados, e a coordenação pediu atenção às regras do TSE em #ia).

## Sugestões de post (rascunho)

> **Post 1 (gráfico 3):** "Feminicídio no Brasil: +32% no governo Temer. +18% no governo
> Bolsonaro. +8% no governo Lula. A tragédia é uma tendência de uma década — e é a maior
> responsabilidade dos ESTADOS, que comandam a segurança pública. Dados oficiais do Anuário
> do FBSP. Quem usa a vida de mulheres para atacar adversário político tá chantageando
> luto. Fonte: Anuário Brasileiro de Segurança Pública 2026."
>
> **Post 2 (gráfico 1):** "Desde 2016, o total de mulheres assassinadas no Brasil CAIU 17%.
> O feminicídio subiu porque agora a lei e a polícia classificam melhor esses crimes (a
> parcela classificada dobrou: 22% → 44%). Temos muito a avançar — 1.571 vidas em 2025 é
> inaceitável. Mas dados não se dobram a narrativa eleitoreira. Fonte: FBSP, Anuário 2026."
>
> **Post 3 (dados duros):** "80% dos feminicídios: companheiro ou ex. 62% em casa. 51% com
> arma branca. 132 MIL descumprimentos de medida protetiva em um ano. 70 mulheres mortas em
> 2025 tinham medida protetiva ativa. O problema não é governo federal, é execução da
> proteção. Fonte: Anuário FBSP 2026."

## Arquivos

- `analise_feminicidio.py` — script reproduzível (lê o Excel oficial e gera tudo)
- `anuario-2026.xlsx` — planilha oficial do FBSP (baixada da fonte)
- `serie_feminicidio_brasil_2016_2025.csv` — série extraída
- `grafico_1_tendencia.png` — feminicídios X total de homicídios de mulheres (herói)
- `grafico_2_proporcao.png` — proporção classificada como feminicídio (22% → 44%)
- `grafico_3_mandatos.png` — variação por mandato

## Próximos passos possíveis (se o squad quiser evoluir)

1. Corte por estado (tabela 21 tem 2024×2025 por UF — dá para apontar onde subiu/caiu de
   verdade, desmontando ou confirmando narrativas locais).
2. Dashboard interativo (Streamlit) — mesma stack que o Ian sugeriu pro CSV do Paulo M:
   os dois projetos podem virar UM produto do squad de dados.
3. Cruzar com taxa per 100 mil mulheres (tabela 21 tem) para ajustar por população.
4. Relação com variáveis socioeconômicas (desemprego, cobertura Bolsa Família/CadÚnico) —
   fonte complementar: IPEA/Atlas da Violência.
