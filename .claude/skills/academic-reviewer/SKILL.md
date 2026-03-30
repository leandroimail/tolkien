---
name: academic-reviewer
description: >
  Revisão acadêmica completa do artigo em 5 dimensões com múltiplas perspectivas.
  Suporta full review, re-review (verificação pós-revisão), quick assessment e
  focused review. Simula painel de revisores com Editor-in-Chief + 3 reviewers + Devil's Advocate.
  Trigger: /academic-reviewer, "revisar artigo", "peer review", "avaliar paper",
  "review paper", "critique paper", "verificar revisão".
allowed-tools: [Read, Write, Edit, Bash, Grep]
metadata:
  version: "1.0"
  depends_on: "academic-writer, academic-citation-manager, academic-bibliography-manager"
---

# Academic Reviewer

Revisão acadêmica multi-perspectiva que simula processo completo de peer review. Consolida lógica de academic-paper-reviewer (painel de 5 revisores), scientific-validation (rigor metodológico) e scientific-manuscript-review (qualidade IMRaD).

## When To Use

- Revisão completa de artigo antes de submissão
- Verificação pós-revisão (re-review) para confirmar que correções foram endereçadas
- Avaliação rápida de qualidade de paper
- Revisão focada em dimensão específica (metodologia, argumentação etc.)

## When Not To Use

- Para redigir o artigo → use `academic-writer`
- Para validar citações/bibliografia → use `academic-citation-manager` + `academic-bibliography-manager`
- Para humanizar texto → use `academic-humanizer`

## Prerequisites

1. **Draft completo** — `draft/*.md` (todas as seções)
2. **`prd.md`** — para contexto de disciplina e objetivos
3. **Gate Citation↔Bibliography** — deve estar ✅ PASS antes de revisão

## Modes

| Mode | Trigger | Output |
|------|---------|--------|
| `full` | "revisão completa" | 5 reports + Editorial Decision + Revision Roadmap |
| `re-review` | "verificar revisão" | Checklist de resposta + decisão |
| `quick` | "avaliação rápida" | Checklist + issues principais (15 min) |
| `focused` | "revisar metodologia" | Report focado em dimensões específicas |

## Method

### Phase 0: Field Analysis & Persona Configuration

1. Ler paper completo
2. Identificar: disciplina, paradigma, tipologia, maturidade
3. Configurar 5 reviewer personas dinamicamente:
   - **EIC**: fit editorial, originalidade, relevância
   - **R1 (Methodology)**: design, validade estatística, reprodutibilidade
   - **R2 (Domain)**: cobertura da literatura, framework teórico, contribuição
   - **R3 (Perspective)**: conexões interdisciplinares, impacto prático
   - **Devil's Advocate**: contra-argumentos, fallacies, viés de confirmação

### Phase 1: Parallel 5-D Review

Cada reviewer avalia independentemente (sem cross-referencing):

#### 5 Dimensões de Avaliação

| # | Dimensão | Peso | Avaliador Principal |
|---|----------|------|-------------------|
| 1 | Rigor científico | 25% | R1 (Methodology) |
| 2 | Coerência argumentativa | 20% | R2 (Domain) + Devil's Advocate |
| 3 | Integridade bibliográfica | 20% | R2 (Domain) |
| 4 | Qualidade da escrita | 20% | EIC + R3 |
| 5 | Conformidade de formato | 15% | EIC |

#### Scoring Scale (0-100)

| Range | Descriptor |
|-------|-----------|
| 90-100 | Exceptional — publication-ready |
| 75-89 | Strong — minor revisions needed |
| 60-74 | Adequate — significant revisions needed |
| 40-59 | Weak — major revisions or restructuring |
| 0-39 | Inadequate — fundamental problems |

### Phase 2: Editorial Synthesis & Decision

O editorial_synthesizer consolida os 5 reports:
1. Identificar consenso (4+ reviewers concordam) vs. divergência
2. Arbitrar questões disputadas
3. Issues CRITICAL do Devil's Advocate bloqueiam Accept

#### Decision Verdicts

| Verdict | Criteria |
|---------|----------|
| **Accept** | Score ≥ 80, 0 CRITICAL issues, no Devil's Advocate blocks |
| **Minor Revision** | Score 65-79, issues endereçáveis em 1 rodada |
| **Major Revision** | Score 50-64, restruturação necessária |
| **Reject** | Score < 50, problemas fundamentais |

### Phase 2.5: Revision Coaching (Socratic)

Se Decision = Minor/Major Revision:
1. Identificar as 3 questões mais importantes
2. Guia Socratic: "Após ler os comentários, o que mais te surpreendeu?"
3. Ajudar a priorizar revisões
4. Gerar Revision Roadmap priorizado

## Re-Review Mode

Para verificação pós-revisão:

```
Input: Revision Roadmap + manuscrito revisado
Process:
  Para cada item no Roadmap:
    Priority 1 (Required): FULLY_ADDRESSED | PARTIALLY | NOT_ADDRESSED | MADE_WORSE
    Priority 2 (Suggested): ≥ 80% devem ter resposta
    Priority 3 (Nice): Verificar mas não bloqueia
Output: Verification Report + New Decision
```

## Self-Review

### Determinístico
- [ ] Cada reviewer cobre perspectiva diferente (sem criticismos duplicados)
- [ ] Decisão editorial baseada nos reports (sem fabricação)
- [ ] Todo weakness tem sugestão concreta de melhoria
- [ ] Devil's Advocate CRITICAL issues refletidos na decisão

### Agêntico
- Consistência interna do relatório
- Equilíbrio entre strengths e weaknesses
- Tom profissional e construtivo

## Output

```markdown
### Review Report
- **Overall Score**: N/100
- **Dimension Scores**: [Rigor: N | Coerência: N | Bibliografia: N | Escrita: N | Formato: N]
- **Verdict**: Accept | Minor Revision | Major Revision | Reject
- **Critical Issues**: N items
- **Revision Roadmap**:
  - Priority 1 (Required): items
  - Priority 2 (Suggested): items
  - Priority 3 (Nice-to-fix): items
```

## References

- `references/review-criteria.md` — framework de critérios por tipo de paper
- `references/scoring-rubrics.md` — rubrics 0-100 com descritores
- `references/devils-advocate.md` — protocolo Devil's Advocate
