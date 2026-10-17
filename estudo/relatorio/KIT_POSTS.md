# Kit de posts — Feminicídio no Brasil 2016-2025
# 6 cards prontos, cada um com gancho + número forte + fonte + gráfico correspondente

---

## CARD 1 — O CONTRANO (hero card) 🏆
**Gráfico:** `grafico_1_perfil_turnover.png` (juízes × CJ) + `b5_scatter_desemprego.png`

> **Não é pobreza. Não é desemprego.**
>
> Testamos 4 variáveis contra a taxa de feminicídio nos 27 estados (média 2023-25):
>
> ❌ Desemprego feminino: ρ = −0,43 → MAIS desemprego = MENOS feminicídio (o INVERSO!)
> ❌ Informalidade/Bolsa Família: ρ = −0,25 → não significante
> ✅ Descumprimento de MPU: ρ = +0,46 → onde mais medida protetiva falha, mais mulheres morrem
> ✅ MPU concedida: ρ = +0,44 → o sistema REAGE, não previne
>
> A correlação mais forte não é econômica — é institucional.
> Estados pobres concedem MENOS MPU (ρ = −0,59). A cadeia é:
> menos Estado → menos proteção → mais descumprimento → mais mortes.
>
> Fonte: Anuário FBSP 2018-2026 · IBGE/SIDRA PNAD Contínua · Análise Spearman, n=27 UFs.

---

## CARD 2 — A DOBRA DA CLASSIFICAÇÃO 📊
**Gráfico:** `grafico_2_proporcao.png` ou painel inferior do `grafico_c3_legislativo.png`

> **O total de mulheres assassinadas CAIU 17% desde 2016.**
>
> Então por que o feminicídio "subiu" +69%?
>
> Porque a parcela de homicídios de mulheres CLASSIFICADOS como feminicídio
> dobrou: de 22% para 44%.
>
> A Lei do Feminicídio (13.104/2015) levou anos para ser incorporada pelos
> estados. Bahia, por exemplo, registrou 18 feminicídios em 2016 — e 74 em 2017.
> O estado não ficou mais violento; a polícia passou a CLASSIFICAR melhor.
>
> Temos muito a avançar (1.571 vidas em 2025 é inaceitável). Mas dado
> não se dobra a narrativa eleitoreira.
>
> Fonte: Anuário Brasileiro de Segurança Pública (FBSP), edições 2018-2026.

---

## CARD 3 — A EXECUÇÃO QUE MATA 🔴
**Gráfico:** rodapé do `grafico_c3_legislativo.png` (número do descumprimento)

> **O Brasil concedeu 555.001 medidas protetivas de urgência em 2024.**
>
> Em 2025: 132.025 foram descumpridas (1 em cada 4).
> **70 mulheres morreram com medida protetiva ATIVA.**
>
> Desde 2006, a Lei Maria da Penha existe. Desde 2015, o feminicídio é crime.
> Em 2023, entrou nos Crimes Hediondos.
>
> **Cinco avanços legislativos em 17 anos. E ainda falhamos em executar.**
>
> O problema não é a lei. É a execução.
>
> Fonte: Anuário FBSP 2025 (T31) e 2026 (T22, T27).

---

## CARD 4 — O MAPA DA DESIGUALDADE 🗺️
**Gráfico:** heatmap do dashboard (ou `grafico_1_tendencia.png` adaptado)

> **Onde as mulheres mais morrem no Brasil?**
>
> Maiores TAXAS por 100 mil mulheres (2025):
> 🥇 Acre: 3,18
> 🥈 Rondônia: 2,87
> 🥉 Mato Grosso: 2,74
> 4º MS: 2,64 · 5º Tocantins: 2,54
>
> **Padrão claro: Norte e Centro-Oeste.**
>
> Maiores VOLUMES (número absoluto):
> 1º São Paulo: 270 · 2º Minas Gerais: 177 · 3º Rio de Janeiro: 105 · 4º Bahia: 102
>
> Quem puxou o aumento de 2025 (+4,4%):
> SP (+17), Pará (+13), Pernambuco (+10), Paraíba (+10), Rondônia (+10)
>
> Fonte: Anuário FBSP 2026, painel de 27 UFs × 10 anos.

---

## CARD 5 — RAÇA É ESTRUTURA ✊
**Gráfico:** `grafico_c1_raca_tempo.png`

> **Mulheres negras são 55% da população feminina brasileira.**
>
> E são **60 a 67% das vítimas de feminicídio** — em TODOS os anos com dado
> disponível, desde 2017.
>
> Isso não é conjuntura. Não é governo. É ESTRUTURA.
>
> 2017-18: 61% negras
> 2019: 67% negras
> 2020-21: 62% negras
> 2023-24: 64% negras
> 2025: 65% negras
>
> Fonte: Anuários FBSP 2019-2026, painéis "Perfil dos Feminicídios".

---

## CARD 6 — TRAVESSANDO GOVERNOS 🇧🇷
**Gráfico:** `grafico_1_tendencia.png` (com faixas de governo)

> **Feminicídio sobe desde 2016 — atravessando 3 governos:**
>
> Temer (2016-18): **+32%**
> Bolsonaro (2019-22): **+18%**
> Lula (2023-25): **+8%** — e a maior QUEDA do total de homicídios de mulheres (−10%)
>
> Mas o total de mulheres assassinadas caiu 17% na década.
> E a parcela classificada como feminicídio dobrou.
>
> A tragédia é uma tendência de uma década — não de um governo.
> E segurança pública é competência ESTADUAL.
>
> Fonte: Anuário FBSP 2018-2026 · Elaboração própria.

---

## INSTRUÇÕES DE USO

1. **Card 1** é o hero — usar sozinho no primeiro post (mais forte)
2. **Cards 2-6** podem sair em sequência (1 por dia) alimentando a thread
3. **Sempre citar a fonte** (Anuário FBSP + IBGE) — regra do servidor
4. **Gráficos correspondentes** estão na pasta `feminicidio-analise/`
5. **Dashboard** (`streamlit run dashboard_feminicidio.py`) pode ser compartilhado
   como link se hospedado (Streamlit Cloud, HuggingFace Spaces)
6. **Cuidado:** correlação não prova causa — esta análise compara estados entre si e mostra
   quais padrões andam juntos (n=27, estudo ecológico). Este caveat
   PROTEGE o grupo de refutação.
