---
name: academic-writer
description: >
  Full writing of academic articles section by section, following an approved outline.
  Consolidates best practices for scientific writing, human academic register, and
  IMRaD/review/case-study structures with strict scope discipline and causal motivation.
  Trigger: /academic-writer, "write section", "write article", "write introduction",
  "write paper", "draft manuscript", "write methodology", "write discussion".
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  version: "2.0"
  role: "producer"
  depends_on: "academic-prd, academic-plan, academic-researcher"
---

# Academic Writer v2

Redação de artigos acadêmicos com qualidade publicável, seção por seção, orientada por evidências e guiada pela estrutura IMRaD ou temática. Transforma outlines e notas de pesquisa em prosa fluida e madura, combatendo o truncamento, o despejo de dados sem narrativa e a deriva temática.

---

## 1. Regras de Ouro (IRON RULES)

1. **NUNCA ESCREVER NO VÁCUO:** Só redigir se houver `draft/outline.md` aprovado e insumos empíricos/bibliográficos carregados (`research/literature.md`, `research/references.bib`, notas ou tabelas). Faltando insumos, emita `[MATERIAL GAP: descrição do dado faltante]` — nunca preencha com alucinação da memória paramétrica.
2. **NUNCA INVENTAR DADO OU CITAÇÃO:** Toda alegação factual exige âncora direta em tabela, figura ou chave existente no `.bib`.
3. **FICHA DE ESCOPO OBRIGATÓRIA (`Scope Card`):** Antes de gerar a prosa de qualquer seção, preencha o bloco `<!-- SCOPE_CARD ... -->` no topo do arquivo com o **Nível de Análise estrito** (ex.: *Team of Agents*, não *Entire Firm*) e os limites fora de escopo.
4. **PERGUNTAS ANTES DA PROSA & OS 6 GATILHOS:** Antes de redigir, responda mentalmente às perguntas STORM e cumpra rigorosamente o dever de justificar o "porquê" caso o texto atinja algum dos **6 Gatilhos de Motivação** (`references/questions-before-prose.md`).
5. **ARQUITETURA DE PARÁGRAFO CEI:** Parágrafos substantivos de resultados e discussão devem seguir a tríade **Claim $\rightarrow$ Evidence $\rightarrow$ Interpretation**. Nunca encerre parágrafos apenas com números sem explicar o que significam para a tese.
6. **DEVER DE GLOSA INTERDISCIPLINAR:** Para artigos na área de Gestão / Engenharia de Produção, termos técnicos de computação (*latência, tokens, context window, temperature*) devem receber definição funcional no primeiro uso.
7. **HIERARQUIA DE ESTILO & ANTI-VÍCIOS:** Normas da Disciplina > Convenções do Periódico > Guia do Autor (`resources/style-guide.md`). Se `resources/anti-style-guide.md` existir, respeite todas as proibições (especialmente erradicar o "tom de mestrado" e *hedging* excessivo).
8. **TAGS DE INTERVENÇÃO HUMANA:** Em trechos puramente reflexivos onde a decisão ou posicionamento do autor humano não estiver claro nas notas, marque `[HUMAN VOICE REQUIRED: descreva a questão a ser decidida pelo pesquisador]`.

---

## 2. Pré-Requisitos

1. **`{root}/paper-{slug}/prd.md`** — tipo de artigo, disciplina, periódico alvo, idioma e formato de citação.
2. **`draft/outline.md`** — estrutura aprovada com meta de contagem de palavras por seção.
3. **`research/literature.md`** e **`research/references.bib`** — base bibliográfica curada.
4. **`resources/`** (opcional) — `style-guide.md`, `anti-style-guide.md`, `human-decisions.md` ou dados brutos.

---

## 3. Modos de Execução

| Modo | Trigger | Comportamento |
|---|---|---|
| `section` | "write introduction", "escreva a metodologia" | Redige uma seção específica mantendo coerência com o outline. |
| `full` | "draft full article", "redija o artigo completo" | Executa sequencialmente todas as seções planejadas. |
| `continue` | "continue draft", "retome a escrita" | Retoma a redação a partir da última seção interrompida. |

---

## 4. Método de Redação em 3 Passos

### Passo 1: Ficha de Escopo e Ancoragem
Insira no topo de `draft/{section}.md`:
```markdown
<!-- SCOPE_CARD
Section: {nome_da_secao}.md
Level_of_Analysis: Team of Agents [STRICT] (NOT Entire Organization)
Primary_Question: {Pergunta respondida por esta seção}
Out_of_Scope: {Tópicos proibidos de expandir}
Theoretical_Anchor: {Teoria ou construto base}
-->
```

### Passo 2: Conversão de Pontos em Prosa Fluida (CEI)
- Expanda argumentos garantindo que cada dado empírico venha acompanhado da sentença interpretativa.
- Desdobre construtos novos via: *Definição Operacional $\rightarrow$ Mecanismo Causal $\rightarrow$ Impacto no Sistema*.
- Aplique *burstiness* consciente (frases curtas intercaladas com sentenças analíticas).

### Passo 3: Auto-Audit Mínimo (Sanity Check do Writer)
Antes de salvar a seção:
- [ ] 0 marcadores `[MATERIAL GAP]` não resolvidos sem autorização.
- [ ] Toda citação segue o formato `\cite{chave}` ou `(Autor, Ano)` correspondente a entrada no `.bib`.
- [ ] 0 listas de compras em tópicos (bullet points) no texto final (salvo critérios de inclusão na Metodologia).
- [ ] Tamanho do texto dentro de $\pm 10\%$ da alocação prevista no outline.
- [ ] O nível de análise respeitou a `Scope Card`.

---

## 5. Referências da Skill

- `references/questions-before-prose.md` — Perguntas de ancoragem e os 6 Gatilhos de Motivação.
- `references/writing-quality-check.md` — Arquitetura CEI, desempacotamento de conceitos e anti-patterns de IA.
- `references/style-guide-usage.md` — Precedência de estilo e integração com style-guide e anti-style-guide.
- `references/discipline-registers.md` — Convenções de registro para Gestão, Engenharia de Produção e STEM.
- `references/imrad-structure.md` — Diretrizes e restrições específicas para cada seção do IMRaD.
