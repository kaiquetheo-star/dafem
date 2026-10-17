# DaFem — Dashboard de Análise de Feminicídio

Análise completa da série histórica de feminicídio no Brasil (2016–2025) com painel estadual, correlações socioeconômicas e recorte racial.

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Como hospedar

1. Push para este repositório
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. New app → selecione este repo → main → `app.py`

## Dados

Todos os dados são públicos:

- **Anuário Brasileiro de Segurança Pública** (FBSP), edições 2018–2026
- **IBGE/SIDRA** — PNAD Contínua (tabela 4093, mulheres)
- **Medidas protetivas** — Anuário FBSP 2025 (T31: MPU concedidas) e Anuário 2026 (T22: vítimas com MPU ativa; T27: descumprimentos)

## Estrutura

```
app.py                              ← aplicação principal
requirements.txt                    ← dependências
.streamlit/config.toml              ← tema
painel_feminicidio_uf_2016_2025.csv ← painel 27 UFs × 10 anos
b1_desemprego_mulheres_uf.csv       ← desemprego feminino por UF
b3_informalidade_mulheres_uf.csv    ← informalidade feminina por UF
b4_medidas_protetivas_uf.csv        ← MPU concedida + descumprimento
matriz_variaveis_uf_2023_25.csv     ← base para correlações
estudo/                             ← relatório, fontes, gráficos e scripts do estudo
```

## Estudo completo

Tudo que sustenta os números está em [`estudo/`](estudo/): relatório final, kit de
posts, 6 gráficos prontos, dados de apoio, os scripts Python que geraram cada
número e o [`estudo/FONTES.md`](estudo/FONTES.md) com a proveniência exata
(edições dos Anuários, tabelas, abas e links oficiais para download).

## Aviso metodológico

Correlação de posto (Spearman) comparando os 27 estados entre si (estudo ecológico).
**Esta análise mostra quais padrões andam juntos — não prova que uma coisa causa a outra.**

---

Squad de Dados — Fora FB! · Outubro 2026
