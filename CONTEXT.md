# DaFem — Contexto completo para iteração de frontend

> Este arquivo é o brief completo para o AI do Cursor entender o projeto,
> o que está ruim no design atual, e exatamente pra onde ir.

## O que é este projeto

**DaFem** (Dashboard de Análise de Feminicídio) é uma ferramenta de jornalismo
de dados e advocacy política. Mostra a série histórica de feminicídio no Brasil
(2016-2025) com painel estadual, correlações socioeconômicas e recorte racial.

**Não é um dashboard corporativo.** É uma ferramenta de movimento social.
Deve parecer um observatório de dados com peso emocional — não um SaaS admin panel.

**Stack:** Python + Streamlit + Plotly + pandas.
**Dados:** 5 CSVs no mesmo diretório (carregados com `os.path.join(os.path.dirname(__file__), ...)`).

## O que está RUIM no design atual (seja honesto)

1. **Parece "Streamlit com CSS colado"** — não um produto desenhado. Os overrides CSS funcionam mas sentem-se artificiais. Elementos Streamlit padrão (radio buttons, selectbox) convivem com HTML customizado sem coesão.

2. **Sem hierarquia visual clara.** Todas as seções têm o mesmo peso. Não há um "hero moment" que grab a atenção. O usuário abre a página e vê 4 cards iguais + um texto. Nada salta.

3. **Charts Plotly genéricos.** Apesar das cores customizadas, os gráficos ainda parecem default do Plotly: mesmos tooltips, mesma densidade de grid, mesmo hover box cinza. Não têm personalidade editorial.

4. **Tipografia Inter é segura mas sem identidade.** É uma fonte de UI, não de editorial/data journalism. Números são tabulares mas não são IMPACTANTES. Falta hierarquia tipográfica de verdade.

5. **Monocromia roxa.** Tudo é violeta. Não há calor, não há urgência, não há variedade. Dados sobre morte de mulheres precisam de mais nuance emocional que um acento só.

6. **O heatmap é feio.** `px.imshow` com a escala customizada ainda parece um mapa de calor genérico. Não conta uma história visual.

7. **Sem micro-interações.** Zero animações, zero transições, zero feedback visual ao interagir. Parece estático e morto.

8. **Sidebar genérica.** O `st.radio` do Streamlit no sidebar não parece navegação de app. Parece um formulário.

9. **Spacing inconsistente.** Alguns lugares têm 32px de margem, outros 8px. Não há um grid/rhythm vertical claro.

10. **Mobile é ruim.** 4 colunas de métricas em uma tela de celular viram 1 coluna com scroll infinito.

## Onde IR — direção de design

### Referências mentais

- **The Pudding** (pudding.cool) — visual essays com dados, tipografia editorial, scroll narrativo
- **Our World in Data** — clareza de dados, mas com design próprio (não genérico)
- **Financial Times** — sério, autoritativo, mas com cor e personalidade
- **Reuters Graphics** — data journalism com impacto visual

### Paleta — usar 3 zonas emocionais, não 1

```
NEUTRAL (fundo, texto, estrutura):
  bg: #0D0F12 (quase-preto, levemente azulado)
  surface: #16181D
  border: #26292F
  text: #E8EAEF
  muted: #71767F

VIOLET (identidade, causa, navegação):
  primary: #9D70F5
  deep: #6B3FD4
  soft: rgba(157, 112, 245, 0.08)  → backgrounds de callout

ALERT (números de morte, urgência):
  coral: #FF6B6B (mortes, números críticos)
  amber: #FFB347 (avisos, descumprimento)
```

### Tipografia — editorial, não UI

- **Display/números:** `"Space Grotesk"` ou `"DM Serif Display"` — com personalidade, não Inter
- **Body/UI:** `"Inter"` ou `"DM Sans"` — para legibilidade em dados
- **Números grandes:** tamanho 48-64px, weight 700-800, `font-variant-numeric: tabular-nums`
- **Títulos de seção:** 24-32px, weight 700, cor `text` (não muted)
- **Labels:** 11-12px, cor `muted`, **sem ALL-CAPS** (é cheap)

### Layout — storytelling, não admin panel

```
┌─────────────────────────────────────────────┐
│  HERO: número grande + contexto em 1 frase  │
│  (ocupa 100% da largura, fundo com gradiente│
│   violeta muito sutil)                      │
├──────────┬──────────┬──────────┬───────────┤
│  metric  │  metric  │  metric  │  metric   │
│  (cards com ALTURA diferente por hierarchy) │
├──────────┴──────────┴──────────┴───────────┤
│                                            │
│  ACHADO CENTRAL (callout, full width)      │
│  "A contradição: homicídios caem 17%,      │
│   feminicídio sobe 69%. Classificação      │
│   dobrou."                                 │
│                                            │
├────────────────────┬───────────────────────┤
│                    │                       │
│  CHART: série      │  CHART: proporção     │
│  (com faixas de    │  (área com anotações) │
│   governo sutis)   │                       │
│                    │                       │
├────────────────────┴───────────────────────┤
│  RACA: stat bar horizontal (6 colunas)     │
├─────────────────────────────────────────────┤
│  MPU: 3 cards em linha + callout legislativo│
└─────────────────────────────────────────────┘
```

### Charts Plotly — específico

- **Remover** gridlines completamente (ou usar `gridcolor: rgba(255,255,255,0.03)`)
- **Hover:** template customizado, não o box padrão. Usar `hovertemplate` com HTML simples
- **Série nacional:** linha roxa grossa (3.5px) com marcadores pequenos, linha cinza fina (1.5px) para total. Faixas de governo como retângulos MUITO sutis (opacity 0.03)
- **Proporção:** área com gradiente violeta (fill com `rgba(157,112,245,0.15)` → transparente)
- **Heatmap:** usar `go.Heatmap` diretamente (não px.imshow), com `colorscale=[[0,'#16181D'],[0.5,'#6B3FD4'],[1,'#9D70F5']]`, texto branco nas células escuras
- **Scatter:** bolhas com cor mapeada à taxa (low=cinza, high=violeta), tamanho fixo (não size=), com labels de estado SEMPRE visíveis (não só no hover)

### CSS — o que fazer

**NÃO usar `@import` do Google Fonts** (demora no Streamlit Cloud). Usar `st.markdown` com um `<link>` ou apenas fontes do sistema com fallback bom.

**Customizar a sidebar** com CSS que esconde o Streamlit default e injeta uma nav custom:
```css
section[data-testid="stSidebar"] .radio-container { display: none; }
/* injetar nav com st.markdown dentro do sidebar */
```

**Animar entrada** de metric-cards com CSS keyframes:
```css
@keyframes slideUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
.metric-card { animation: slideUp 0.4s ease-out; animation-fill-mode: both; }
.metric-card:nth-child(2) { animation-delay: 0.05s; }
.metric-card:nth-child(3) { animation-delay: 0.1s; }
.metric-card:nth-child(4) { animation-delay: 0.15s; }
```

### Streamlit — limitações que você PRECISA saber

1. **Não dá pra fazer layout multi-column livre** — só `st.columns()` que cria colunas iguais (ou com ratio). Não há CSS grid nativo.
2. **HTML customizado** só via `st.markdown(html, unsafe_allow_html=True)` — sem JavaScript customizado
3. **Plotly** é a única biblioteca de charts nativa — não dá pra usar D3 ou Chart.js diretamente
4. **`st.metric`** é limitado — para cards bons, usar HTML puro via `st.markdown`
5. **Sidebar** só aceita widgets Streamlit + `st.markdown` — não aceita HTML com onclick
6. **Cache** — usar `@st.cache_data` para não recarregar dados em cada rerun
7. **Deploy no Streamlit Cloud** — não suporta arquivos estáticos customizados, apenas os CSVs Python
8. **`use_container_width`** está deprecado — usar `width='stretch'` em versões novas

### Mobile

```css
@media (max-width: 768px) {
    .metric-card { margin-bottom: 8px; }
    .metric-value { font-size: 28px; }
    .stat-bar { flex-direction: column; }
    .stat-item { border-bottom: 1px solid var(--border); }
}
```

## Schema dos dados

```python
# painel_feminicidio_uf_2016_2025.csv
# uf, ano, fem_abs (número), fem_taxa (per 100k), hom_abs, prop_pct

# matriz_variaveis_uf_2023_25.csv
# uf, fem_taxa, informal, desemp, mpu_conc, descump

# b4_medidas_protetivas_uf.csv
# uf, fem_taxa_24, fem_taxa_25, mpu_dist_24, mpu_conc_24, mpu_conc_taxa_24, desc_abs_25, desc_taxa_25, ...

# b1_desemprego_mulheres_uf.csv / b3_informalidade_mulheres_uf.csv
# uf, ano, desemp_mulheres_pct / informal_fem_pct
```

## Achados-chave (para copy dos títulos de seção)

1. "Homicídios de mulheres caem 17%. Feminicídio sobe 69%." → classificação dobrou (22%→44%)
2. "Desemprego NÃO explica o mapa" → correlação NEGATIVA (ρ=−0,43)
3. "Onde mais MPU falha, mais mulheres morrem" → descumprimento ρ=+0,46
4. "Raça é estrutura" → negras são 56% da pop. e 60-67% das vítimas, sempre
5. "A proteção que não protege" → 555k MPUs concedidas, 132k descumpridas, 70 mortas com MPU ativa
6. "Padrão Norte/CO" → Acre 3.18, Rondônia 2.87, MT 2.74 (maiores taxas/100k)

## Prioridades de melhoria (nesta ordem)

1. **Hero section** — o primeiro viewport precisa ter IMPACTO. Um número grande (1.571) com contexto. Não 4 cards iguais.
2. **Charts** — remover 100% do feel "default Plotly". Cores, spacing, hover, annotations.
3. **Sidebar** — custom CSS para parecer nav de app, não radio button do Streamlit.
4. **Tipografia** — trocar Inter por algo com personalidade. Números maiores.
5. **Mobile** — garantir que não quebra.
