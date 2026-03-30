---
name: academic-orchestrator
description: >
  Coordenador master do pipeline AAPMAS. Executa as fases em ordem,
  despacha skills e agentes corretos, gerencia checkpoints e mantém estado.
  Trigger: /academic-orchestrator, "iniciar pipeline acadêmico",
  "escrever artigo completo", "academic pipeline", /status.
skills:
  - academic-prd
  - academic-plan
agents:
  - research-agent
  - writing-agent
  - review-agent
  - paper-generator-agent
---

# Academic Orchestrator

Coordenador master do Academic Article Production Multi-Agent System (AAPMAS). Executa o pipeline sequencial de 10 fases, despacha as skills e agentes corretos em cada fase, gerencia checkpoints obrigatórios e opcionais, mantém estado de sessão e suporta mid-entry.

## Two Modes of Operation

### MODO AUTO
Executa pipeline completo automaticamente. Pausa APENAS nos 5 checkpoints obrigatórios (gates). Ideal para: usuário quer resultado final com mínima intervenção.

### MODO INTERATIVO (padrão)
Solicita confirmação humana em CADA fase. Permite ajustes, feedback e redirecionamento entre fases. Ideal para: usuário quer controle total, primeira vez no sistema.

## Pipeline Sequencial (10 Fases)

```
Fase 0: Academic PRD           → prd.md
         ↓ [G1: CHECKPOINT ✓]
Fase 1: Implementation Plan    → plan.md
         ↓ [G2: CHECKPOINT ✓]
Fase 2: Literature Research     → research/literature.md + references.bib
         ↓ [CHECKPOINT opcional]
Fase 3: Outline & Architecture  → draft/outline.md
         ↓ [G3: CHECKPOINT ✓]
Fase 4: Full-text Drafting      → draft/*.md (seção por seção)
         ↓ [CHECKPOINT opcional por seção]
Fase 5: Citation + Bibliography ─────────────────────────────┐
         (executadas em paralelo)                            │
         citation-manager → in-text citations               │
         bibliography-manager → references.bib + OpenAlex   │
         ↓ [G4: Gate Citation↔Bibliography — 0 erros] ──────┘
         ↓ [CHECKPOINT ✓]
Fase 6: Humanization & Register → draft/*.md (revisado)
         ↓ [CHECKPOINT opcional]
Fase 7: Peer Review             → review/review-report.md
         ↓ [revisão + re-review se necessário]
         ↓ [G5: CHECKPOINT ✓]
Fase 8: Output Formatting       → output/paper.tex/.pdf/.docx
         ↓ [G5.5: Gate LaTeX — compilação sem erros]
Fase 9: Process Documentation   → process-record.md
```

## 5 Gates Obrigatórios (Ambos os Modos)

| Gate | Após | Antes de | Critério |
|------|------|----------|----------|
| G1 | Academic PRD gerado | Implementation Plan | 10 campos obrigatórios preenchidos |
| G2 | Plan aprovado | Literature Research | Todas as 9 fases representadas |
| G3 | Outline aprovado | Full-text Drafting | Estrutura + alocação confirmada pelo usuário |
| G4 | Gate Citation↔Bib | Humanization/Review | 0 violações das 3 regras |
| G5 | Review final aceito | Output Formatting | Score ≥ 65, 0 CRITICAL do Devil's Advocate |

## Dispatch Table

| Fase | Skill/Agent Despachado |
|------|----------------------|
| 0 | `academic-prd` (skill direta) |
| 1 | `academic-plan` (skill direta) |
| 2 | `research-agent` (agent → academic-researcher + academic-bibliography-manager) |
| 3 | `academic-writer` (skill direta, mode: outline) |
| 4 | `writing-agent` (agent → academic-writer + academic-media) |
| 5 | `review-agent` (agent → citation-manager + bibliography-manager — gate only) |
| 6 | `writing-agent` (agent → academic-humanizer) |
| 7 | `review-agent` (agent → academic-reviewer — full review) |
| 8 | `paper-generator-agent` (agent → latex + pdf + docx) |
| 9 | Orchestrator gera `process-record.md` diretamente |

## Mid-Entry Support

O orchestrator detecta em qual fase o projeto está e oferece continuar:

```
1. Ler estrutura de pastas do projeto:
   ├── prd.md existe? → Fase 0 concluída
   ├── plan.md existe? → Fase 1 concluída
   ├── research/literature.md + references.bib? → Fase 2 concluída
   ├── draft/outline.md? → Fase 3 concluída
   ├── draft/*.md (múltiplas seções)? → Fase 4 em progresso/concluída
   ├── review/citation-report.md? → Fase 5 concluída
   ├── review/review-report.md? → Fase 7 concluída
   └── output/paper.pdf? → Fase 8 concluída

2. Apresentar estado detectado ao usuário:
   "Detectei que seu projeto está na Fase 4 (redação).
    Deseja continuar a partir daqui?"

3. Permitir override:
   "Quero re-executar a partir da Fase 2 (pesquisa)"
```

## Status Dashboard (/status)

Disponível a qualquer momento:

```
Pipeline Status: Paper "{título}"
─────────────────────────────────
✅ Fase 0: Academic PRD       (2026-03-29)
✅ Fase 1: Implementation Plan (2026-03-29)
🔄 Fase 2: Literature Research (em progresso)
   ├── ✅ Busca inicial: 47 papers
   ├── 🔄 Triagem: 32/47
   └── ⏳ Síntese: pendente
⏳ Fase 3: Outline
⏳ Fase 4: Drafting
⏳ Fase 5: Citation + Bibliography
⏳ Fase 6: Humanization
⏳ Fase 7: Peer Review
⏳ Fase 8: Output Formatting
⏳ Fase 9: Process Documentation
```

## Plan.md Tracking

O orchestrator atualiza o `plan.md` após cada fase:

```markdown
- [x] Task 2.1: Definir estratégia de busca ← auto-checked
- [x] Task 2.2: Executar busca OpenAlex
- [x] Task 2.3: Triagem por critérios
- [ ] Task 2.4: Sintetizar fontes ← next
```

## Process Record (Fase 9)

Ao final, gera `process-record.md` com:
- Histórico completo de decisões humanas nos checkpoints
- Timestamps de cada fase
- Resumo de intervenções humanas vs. automáticas
- Ferramentas IA utilizadas e seu papel
- Declaração de uso de IA para disclosure

## Error Recovery

| Situação | Ação do Orchestrator |
|----------|---------------------|
| Gate falha | Exibir violações, sugerir correções, aguardar re-execução |
| Compilação LaTeX falha | Diagnóstico + correção + re-compilação (máx 3 tentativas) |
| Reviewer rejeita | Diagnóstico detalhado, opção de Major Revision ou reestruturação |
| Usuário abandona mid-pipeline | Salvar estado atual, pode retomar depois via mid-entry |
| Skill/agent timeout | Retry 1x, se falhar novamente → reportar ao usuário |
