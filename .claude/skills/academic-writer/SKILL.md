---
name: academic-writer
description: >
  Redação completa de artigos acadêmicos seção por seção, seguindo outline aprovado.
  Consolida boas práticas de escrita científica, registro acadêmico humano, e
  estruturas IMRaD/review/case-study.
  Trigger: /academic-writer, "escrever seção", "redigir artigo", "escrever introdução",
  "write paper", "draft manuscript", "write methodology", "write discussion".
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  version: "1.0"
  depends_on: "academic-prd, academic-plan, academic-researcher"
---

# Academic Writer

Redação de artigos acadêmicos com qualidade publicável, seção por seção. Consolida as melhores práticas de scientific-writing, academic-paper, academic-writing, academic-writing-style e scientific-paper em uma skill unificada.

## When To Use

- Redigir qualquer seção de paper acadêmico (abstract, introduction, methods, results, discussion, conclusion)
- Seguir estrutura IMRaD, revisão sistemática, estudo de caso ou temática
- Produzir prosa acadêmica fluida, sem bullet points no output final
- Ajustar registro acadêmico por disciplina (STEM, ciências sociais, humanities)

## When Not To Use

- Para buscar literatura → use `academic-researcher`
- Para validar citações in-text → use `academic-citation-manager`
- Para revisão do artigo pronto → use `academic-reviewer`
- Para humanizar texto já escrito → use `academic-humanizer`
- Para gerar figuras/diagramas → use `academic-media`

## Prerequisites

1. **`prd.md`** — tipo de paper, disciplina, formato de citação, língua
2. **`draft/outline.md`** — estrutura aprovada com alocação de palavras
3. **`research/literature.md`** — síntese da literatura
4. **`research/references.bib`** — referências disponíveis para citação

## Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| `section` | "escrever introdução" | Redige uma seção específica |
| `full` | "redigir artigo completo" | Todas as seções sequencialmente |
| `continue` | "continuar draft" | Retoma a partir do último ponto |

## Method: Two-Stage Writing Process

### Stage 1: Outline com Key Points (Estrutural)

Para cada seção, criar outline interno com:
- Argumentos principais a apresentar
- Estudos-chave para citar (com anos e achados)
- Dados e estatísticas a incluir
- Fluxo lógico e organização

> Este outline é scaffolding interno — NÃO é o output final.

### Stage 2: Conversão para Prosa Completa

Expandir cada ponto em parágrafos fluidos:
1. Transformar bullets em sentenças com sujeito, verbo, objeto
2. Integrar citações naturalmente (narrativa vs. parentética)
3. Variar estrutura de sentenças — evitar monotonia
4. Conectar parágrafos por lógica de conteúdo, não por "Furthermore/Moreover"

## Writing Quality Standards

### 5 Anti-Patterns a Evitar

| Padrão IA | Como Corrigir |
|-----------|---------------|
| **Hedging Soup** — stacking "potentially/possibly/may" | Uma declaração precisa + uma limitação precisa |
| **Formulaic Transitions** — "Furthermore/Moreover/Additionally" | Deixar a lógica do conteúdo conectar; usar transições reais |
| **Structural Monotony** — mesma extensão em cada parágrafo | Variar extensão ≥ 30%; misturar parágrafos curtos e longos |
| **Abstraction Fog** — "various studies/the literature suggests" | Nomear estudos: "Patel et al. (2022) found..." |
| **Voice Erasure** — "it can be argued/it was found" | Usar voz ativa: "We argue..." quando disciplina permite |

### Self-Audit Per Section

Before presenting any section:
- [ ] Hedging: < 2 hedging words per paragraph
- [ ] Transitions: 0 instances of Furthermore/Moreover/Additionally
- [ ] Structure: No 3 consecutive paragraphs within 10 words of each other
- [ ] Specificity: 0 instances of "various studies" without concrete referent
- [ ] Voice: < 3 instances of "it can be/it was found" per page

## Section-Specific Checkers

| Section | Must Have | Must NOT Have |
|---------|-----------|---------------|
| Introduction | Contexto + gap + objetivo + estrutura do paper | Resultados, interpretações |
| Methods | Design, amostra, variáveis, protocolo reprodutível | Interpretações de resultados |
| Results | Fatos, dados, estatísticas objetivas | Interpretação ou especulação |
| Discussion | Conexão resultados↔questões, comparação com literatura | Dados novos não apresentados em Results |
| Conclusion | Limitações, trabalhos futuros, implicações | Novos dados ou resultados |

## Discipline-Aware Register

| Discipline | Voice | Citation Style | Key Features |
|-----------|-------|---------------|--------------|
| STEM | Active for claims, passive acceptable in Methods | Author-date or numbered | Hypotheses numbered, statistical reporting |
| Social Sciences | Active + first person plural | Author-date (APA) | Theoretical framing, effect sizes |
| Humanities | First person singular | Notes or author-date | Close reading, interpretive argument |
| Interdisciplinary | Active + first person plural | Per target journal | Define terms from each field |

## Citation Integration

- **Narrative**: quando identidade do autor importa — "Foucault (1975) argued..."
- **Parentetical**: quando o achado importa — "rates tripled (Alexander, 2010)"
- **Direct quote**: apenas quando wording é o ponto — definição, frase contestada
- **Synthesis**: para mostrar consenso — "(Lee, 2019; Nakamura, 2020; dos Santos, 2021)"

## Integration with academic-media

Quando detectar necessidade de figura, esquema ou EDA:
```
→ academic-media: {descrição do elemento visual necessário}
```

## Self-Review

### Determinístico
- [ ] ∀ citação usa formato `\cite{key}` ou `(Autor, Ano)` conforme style
- [ ] Contagem de palavras ±10% da alocação no outline
- [ ] Sem bullet points na prosa final (exceto Methods: inclusion criteria)
- [ ] Registro acadêmico mantido (sem linguagem coloquial)

### Agêntico
- Consistência de terminologia entre seções
- Fluxo lógico da argumentação
- Lacunas de evidência (afirmações factuais sem citação)

## References

- `references/imrad-structure.md` — guia detalhado IMRAD
- `references/writing-quality-check.md` — checklist anti-AI markers
- `references/discipline-registers.md` — convenções por campo
