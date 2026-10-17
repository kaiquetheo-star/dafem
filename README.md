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
- **Medidas protetivas** — Anuários FBSP 2025 (T31) e 2026 (T27)

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
```

## Aviso metodológico

Correlação de posto (Spearman), n=27 UFs, estudo ecológico.
**Correlação não implica causalidade.**

---

Squad de Dados — Fora FB! · Outubro 2026
