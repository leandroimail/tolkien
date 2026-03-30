---
name: academic-humanizer
description: >
  Ajuste de registro, humanização e naturalização da escrita acadêmica.
  Remove marcadores típicos de texto AI mantendo rigor acadêmico.
  Suporta múltiplas línguas (EN, PT-BR, FI) com convenções disciplinares.
  Trigger: /academic-humanizer, "humanizar", "ajustar registro",
  "naturalizar escrita", "humanize text", "remove AI feel".
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  version: "1.0"
  depends_on: "academic-writer"
---

# Academic Humanizer

Humanização e naturalização da escrita acadêmica. Remove artificialidade de texto gerado por IA mantendo registro acadêmico, terminologia técnica e integridade factual. Consolida as melhores práticas de humanize, humanize-academic-writing e finnish-humanizer.

## When To Use

- Texto acadêmico soa "perfeito demais", mecânico ou repetitivo
- Parágrafos parecem template com estrutura uniforme
- Transições são todas "Furthermore/Moreover/Additionally"
- Linguagem é excessivamente abstrata sem exemplos concretos
- Após draft do `academic-writer` e antes de revisão final
- Quando autor quer ajustar o registro acadêmico por disciplina

## When Not To Use

- Para redigir o artigo do zero → use `academic-writer`
- Para revisão acadêmica/peer review → use `academic-reviewer`
- Para usar API externa de humanização → consulte HumanizerAI API diretamente

## Prerequisites

1. **Draft completo ou seção** — `draft/*.md`
2. Informação sobre disciplina e língua-alvo (do `prd.md`)

## Method

### Step 1: Analyze — Detect AI Patterns

Identificar padrões problemáticos no texto:

#### 5 Categorias Principais

| # | Padrão | Detecção |
|---|--------|----------|
| 1 | **Rhythm Uniformity** | Todas as sentenças com ~mesma extensão (15-20 palavras) |
| 2 | **Formulaic Transitions** | Moreover/Furthermore/Additionally no início de sentenças |
| 3 | **Abstract Scaffolding** | "various aspects", "in terms of", "multiple factors" |
| 4 | **Generic Academic Tone** | Sem engajamento crítico com fontes, sem voz do autor |
| 5 | **Voice Erasure** | "it can be argued...", "it is important to note..." |

#### Métricas Quantitativas

- **Sentence Length Variance**: deve ser > 30%
- **Type-Token Ratio (TTR)**: diversidade vocabular
- **Transition Word Density**: < 5% das sentenças
- **Passive Voice %**: apropriado para disciplina
- **Consecutive Similarity**: sentenças adjacentes não devem ser estruturalmente idênticas

### Step 2: Rewrite with Targeted Strategies

#### Strategy 1: Vary Sentence Rhythm (Burstiness)
- Mix: short (5-10 words) + medium (15-20) + long (25-35)
- Antes: "This study examines X. The research focuses on Y. The analysis considers Z."
- Depois: "This study examines X's impact on Y, considering factors from identity formation to civic engagement."

#### Strategy 2: Eliminate Abstract Scaffolding
- Replace "various aspects" → conceitos nomeados específicos
- Replace "in terms of" → relação direta
- Replace "it is important to note" → DELETE (comece com o conteúdo)

#### Strategy 3: Natural Transitions
- Remove: Furthermore, Moreover, Additionally, It is important to note
- Use: fluxo lógico direto, "This pattern echoes...", "Building on..."
- Regra: se deletar a transição não muda o significado, delete

#### Strategy 4: Ground in Specificity
- Replace "research has shown" → "Patel et al. (2022) surveyed 814 nurses"
- Replace "various studies" → "Four longitudinal cohort studies (totaling 23,000 participants)"
- Replace "the field" → domínio concreto nomeado

#### Strategy 5: Restore Author Voice
- Replace "it can be argued" → "We argue"
- Replace "it was found" → "We found" / "The analysis reveals"
- Usar primeira pessoa quando disciplina permite

### Step 3: Present with Rationale

Para cada parágrafo modificado:
```
**Original:** [texto original]
**Revised:** [texto humanizado]
**Rationale:** Removed 3x "Moreover" transitions, varied sentence length (8, 24, 15 words),
     replaced "various studies" with specific citation (Smith 2022).
```

## Language-Specific Considerations

### English
- Prefer common over complex: "use" not "utilize"
- Field-specific terminology is fine — don't over-simplify
- Active voice default, passive in Methods when appropriate

### Portuguese (BR)
- Preservar registro formal acadêmico brasileiro
- Remover "Além disso/Ademais/Outrossim" em excesso
- Manter termos técnicos em inglês quando é norma da área
- ABNT: registro em terceira pessoa é padrão

### Finnish (FI)
- Suoruus (directness): dizer e seguir em frente
- Partikkelit: -han/-hän, -pa/-pä, kyllä, vaan — mantêm texto natural
- Não exagerar enthusiasmo — "Ihan hyvä" é elogio

## Guardrails

- **NÃO alterar significado** — apenas forma, nunca conteúdo factual
- **NÃO adicionar informações** — não inventar citações ou dados
- **NÃO simplificar demais** — naturalizar ≠ infantilizar
- **Preservar citações** — toda referência fica intacta
- **Respeitar registro** — texto formal permanece formal
- **NÃO casualizar** — academic writing deve permanecer academic

## Self-Review

### Determinístico
- [ ] 0 informações factuais novas introduzidas (apenas ajustes de forma)
- [ ] Todas as citações preservadas intactas
- [ ] Sentence length variance > 30%
- [ ] < 2 hedging words per paragraph
- [ ] 0 instances of Furthermore/Moreover/Additionally

### Agêntico
- Verificar que tom acadêmico foi preservado por disciplina
- Confirmar que terminologia técnica não foi alterada
- Verificar que o texto soa natural para a língua-alvo

## References

- `references/ai-patterns.md` — lista completa de 26 padrões AI detectáveis
- `references/language-specific.md` — convenções por língua
