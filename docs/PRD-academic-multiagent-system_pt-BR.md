# PRD Técnico: Sistema Multi-Agente para Produção de Artigos Científicos (tolkien)

**Versão:** 1.0
**Data:** 2026-03-29
**Status:** Rascunho para revisão

---

## 1. Resumo Executivo

O **Academic Article Production Multi-Agent System (tolkien)** é um harness de múltiplos agentes para suporte à produção de artigos acadêmicos e científicos, executável no **Claude Code** e no **OpenCode**. O sistema segue a abordagem **Spec-Driven Development (SDD)** adaptada ao contexto acadêmico: o processo inicia com a criação de um *Academic PRD* (documento de requisitos do artigo), que gera um plano de implementação com tasks, e então executa o pipeline de escrita de forma sequencial com checkpoints de confirmação humana.

O sistema é composto por **skills atômicas** (capacidades especializadas) e **agentes** (configurações que orquestram as skills). As skills são os blocos de construção; os agentes determinam quais skills usar e em que ordem.

---

## 2. Problema

A produção de artigos científicos é um processo complexo e multidisciplinar que envolve pesquisa bibliográfica, estruturação de argumentação, redação, gerenciamento de referências, revisão por pares e formatação de saída. Atualmente:

- Não existe um fluxo estruturado e rastreável para esse processo com suporte de IA
- Skills e agentes existentes são fragmentados, sobrepostos e sem orquestração
- Não há validações determinísticas garantindo integridade entre citações e bibliografia
- Não há checkpoints de confirmação humana entre etapas críticas
- O estado do artigo em progresso não é persistido de forma estruturada

---

## 3. Objetivos

### 3.1 Objetivos Primários

- Implementar um pipeline sequencial completo para produção de artigos científicos
- Criar skills consolidadas, sem sobreposição, com responsabilidades claras
- Garantir validações determinísticas em cada etapa (compilação LaTeX, citações, bibliografia)
- Implementar self-review e agentic review em cada skill
- Manter estado do artigo em arquivos Markdown por projeto
- Compatibilidade cross-IDE: Claude Code (`.claude/skills/`) e OpenCode (`.agents/skills/`)

### 3.2 Fora do Escopo

- Interface gráfica ou web
- Submissão automática para periódicos ou conferências
- Gestão de múltiplos artigos simultâneos em um único projeto
- Integração com sistemas de gestão de referências externos (Zotero, Mendeley)

---

## 4. Abordagem: Spec-Driven Development Acadêmico

O sistema adapta o padrão SDD ao contexto acadêmico:

```
┌─────────────────────────────────────────────────────────────┐
│  SDD ACADÊMICO                                              │
│                                                              │
│  [Academic PRD]  →  [Implementation Plan]  →  [Execution]  │
│     prd.md              plan.md + tasks         pipeline    │
│                                                              │
│  Equivalente a:                                             │
│  spec.md          →  implementation steps  →  code/write   │
└─────────────────────────────────────────────────────────────┘
```

**Academic PRD** funciona como documento de requisitos do artigo — define *o quê* será escrito, para quem, com quais restrições.

**Implementation Plan** traduz o PRD em tasks sequenciais com fases, entregáveis e critérios de conclusão.

**Execution** executa o pipeline fase por fase, com checkpoints humanos obrigatórios.

---

## 5. Arquitetura do Sistema

### 5.1 Camadas

```
┌──────────────────────────────────────────────────────────────┐
│  CAMADA 3: AGENTES                                           │
│  academic-orchestrator (auto + interativo)                   │
│  research-agent | writing-agent | review-agent               │
│  paper-generator-agent                                       │
├──────────────────────────────────────────────────────────────┤
│  CAMADA 2: SKILLS DO PIPELINE                                │
│  academic-prd | academic-plan | academic-researcher          │
│  academic-writer | academic-citation-manager                 │
│  academic-bibliography-manager | academic-reviewer           │
│  academic-humanizer | academic-media                         │
├──────────────────────────────────────────────────────────────┤
│  CAMADA 1: SKILLS DE FERRAMENTAS (já implementadas)          │
│  latex | latex-template-converter | pdf | docx | xlsx        │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 Pipeline Sequencial

```
Fase 0: Academic PRD          → prd.md
         ↓ [CHECKPOINT ✓]
Fase 1: Implementation Plan   → plan.md
         ↓ [CHECKPOINT ✓]
Fase 2: Literature Research   → research/literature.md + references.bib
         ↓ [CHECKPOINT ✓]
Fase 3: Outline & Architecture → draft/outline.md
         ↓ [CHECKPOINT ✓]
Fase 4: Full-text Drafting    → draft/*.md (seção por seção)
         ↓ [CHECKPOINT ✓]
Fase 5: Citation + Bibliography ────────────────────────────┐
         (executadas em paralelo)                           │
         citation-manager → in-text citations              │
         bibliography-manager → references.bib + OpenAlex  │
         ↓ [GATE: validação cruzada citation↔bibliography] ┘
         ↓ [CHECKPOINT ✓]
Fase 6: Humanization & Register → draft/*.md (revisado)
         ↓ [CHECKPOINT ✓]
Fase 7: Peer Review            → review/review-report.md
         ↓ [revisão + re-review se necessário]
         ↓ [CHECKPOINT ✓]
Fase 8: Output Formatting      → output/paper.tex/.pdf/.docx
         ↓ [CHECKPOINT ✓]
Fase 9: Process Documentation  → process-record.md
```

### 5.3 Estrutura de Estado (Markdown)

Cada artigo terá uma pasta de projeto com a seguinte estrutura:

```
paper-{slug}/
├── prd.md                    ← Academic PRD (requisitos do artigo)
├── plan.md                   ← Plano de implementação + tasks
├── research/
│   ├── literature.md         ← fontes encontradas, triagem, síntese
│   ├── search-strategy.md    ← estratégia de busca, critérios inclusão/exclusão
│   └── references.bib        ← BibTeX (fonte da verdade para referências)
├── draft/
│   ├── outline.md            ← estrutura aprovada, alocação de palavras
│   ├── introduction.md
│   ├── methodology.md
│   ├── results.md
│   ├── discussion.md
│   ├── conclusion.md
│   └── abstract.md
├── review/
│   ├── review-report.md      ← revisão 5 dimensões
│   └── revision-log.md       ← histórico de revisões
├── output/
│   ├── paper.tex
│   ├── paper.pdf
│   └── paper.docx
└── process-record.md         ← documentação do processo humano-IA
```

---

## 6. Especificação das Skills

### 6.1 Inventário Completo

| # | Skill | Status | Absorve (legadas) | Camada |
|---|---|---|---|---|
| 1 | `academic-prd` | **CRIAR** | — | Meta |
| 2 | `academic-plan` | **CRIAR** | — | Meta |
| 3 | `academic-researcher` | **CONSOLIDAR** | academic-researcher, academic-deep-research, openalex-paper-search | Pipeline |
| 4 | `academic-writer` | **CONSOLIDAR** | academic-writing, academic-writing-style, scientific-writing, academic-paper, scientific-paper | Pipeline |
| 5 | `academic-citation-manager` | **CONSOLIDAR** | citation-anchoring, citation-audit, citation-validator, citation-management | Pipeline |
| 6 | `academic-bibliography-manager` | **CONSOLIDAR** | citation-bibliography-generator, openalex-database | Pipeline |
| 7 | `academic-reviewer` | **CONSOLIDAR** | academic-paper-reviewer, scientific-validation, scientific-manuscript-review | Pipeline |
| 8 | `academic-humanizer` | **CONSOLIDAR** | humanize, humanize-academic-writing, finnish-humanizer | Pipeline |
| 9 | `academic-media` | **CONSOLIDAR** | scientific-eda, scientific-paper-figure-generator, scientific-schematics | Suporte |
| 10 | `latex` | ✅ PRONTA | latex-build, latex-document, latex-paper-en, latex-pdf-compiler, latex-tables, latex-formatting | Ferramenta |
| 11 | `latex-template-converter` | ✅ PRONTA | latex-conference-template-organizer | Ferramenta |
| 12 | `pdf` | ✅ PRONTA | — | Ferramenta |
| 13 | `docx` | ✅ PRONTA | — | Ferramenta |
| 14 | `xlsx` | ✅ PRONTA | — | Ferramenta |
| — | `scientific-email-polishing` | MANTER (utilitária) | — | Utilitária |

### 6.2 Skill: `academic-prd`

**Propósito:** Conduzir entrevista de configuração com o usuário e gerar o `prd.md` do artigo.

**Inspiração:** SDD `spec.md` — define *o quê* antes de *como*.

**Trigger:** `/academic-prd`, "criar PRD acadêmico", "configurar artigo", "iniciar pipeline"

**Inputs obrigatórios (via entrevista):**
1. Tipo de paper (research article, review, case study, systematic review, meta-analysis)
2. Disciplina / campo (e.g., medicina, engenharia, psicologia)
3. Questões de pesquisa e objetivos principais
4. Formato de citação (APA, MLA, Chicago, IEEE, Vancouver, ABNT)
5. Formato de saída (LaTeX, DOCX, PDF, Markdown)
6. Template de conferência/publicação (se aplicável)
7. Documentos de apoio (guidelines, templates, papers de referência)
8. Estratégia de busca (palavras-chave, bases, critérios inclusão/exclusão)
9. Estrutura do paper (IMRaD, temática, outra)
10. Língua(s) (artigo principal + abstract bilíngue se necessário)

**Outputs:**
- `prd.md` — documento de requisitos do artigo com todas as decisões tomadas
- Sumário de decisões imprimido no terminal para confirmação

**Técnica:** Usa BDD para formalizar requisitos:
```gherkin
Given um tipo de paper e disciplina definidos,
When o usuário fornece os detalhes necessários,
Then o sistema gera um outline estruturado que adere às convenções do campo.
```

**Validações determinísticas:**
- Verificar que todos os 10 campos obrigatórios foram preenchidos
- Verificar coerência: ex. formato IEEE requer LaTeX; ABNT permite DOCX
- Alertar se template de conferência for especificado sem arquivo de template

**Self-review:** O agente relê o `prd.md` gerado e verifica completude antes de entregar.

**Checkpoint:** Obrigatório — usuário deve confirmar o `prd.md` antes de avançar.

---

### 6.3 Skill: `academic-plan`

**Propósito:** Ler o `prd.md` e gerar `plan.md` com fases, tasks, entregáveis e critérios de conclusão.

**Trigger:** `/academic-plan`, "gerar plano", "criar tasks do artigo"

**Inputs:** `prd.md` (obrigatório)

**Outputs:**
- `plan.md` — plano completo com fases numeradas, tasks por fase, entregáveis, critérios de aceite
- Tasks formatadas como checklist Markdown: `- [ ] Task`

**Estrutura do `plan.md`:**
```markdown
# Implementation Plan: {título do artigo}
## Fase 2: Literature Research
### Tasks
- [ ] Definir estratégia de busca
- [ ] Executar busca no OpenAlex com keywords: {keywords do PRD}
- [ ] Triagem por critérios: {critérios do PRD}
- [ ] Sintetizar N fontes primárias
### Entregável: research/literature.md + research/references.bib
### Critério de conclusão: N fontes triadas, .bib validado
```

**Validações determinísticas:**
- Verificar que todas as 9 fases do pipeline estão representadas no plano
- Verificar que entregáveis do plano correspondem à estrutura de pastas esperada

**Self-review:** Agente verifica cobertura do PRD no plano antes de entregar.

**Checkpoint:** Obrigatório — usuário confirma plano antes de executar.

---

### 6.4 Skill: `academic-researcher`

**Propósito:** Busca de literatura sistemática, triagem de fontes e síntese bibliográfica.

**Fontes absorvidas:** academic-researcher, academic-deep-research, openalex-paper-search

**Integração OpenAlex (como dependência interna):**
- Busca por keywords, DOI, autor, instituição
- API sem key: `curl "https://api.openalex.org/works?search={query}&mailto={email}"`
- Filtragem por ano, tipo, acesso aberto, fator de impacto (FWCI)
- Exportação de metadados para BibTeX

**Trigger:** `/academic-researcher`, "pesquisar literatura", "encontrar papers sobre"

**Modos:**
- `socratic` — diálogo para refinar questão de pesquisa antes de buscar
- `full` — busca sistemática completa com triagem e síntese
- `quick` — busca rápida para N papers mais relevantes

**Inputs:** `prd.md`, keywords, critérios de inclusão/exclusão

**Outputs:**
- `research/literature.md` — fontes encontradas + triagem + síntese
- `research/search-strategy.md` — estratégia documentada
- `research/references.bib` — BibTeX raw (a ser validado pelo bibliography-manager)

**Validações determinísticas:**
- Verificar que cada entrada exportada tem campos obrigatórios: `author`, `title`, `year`, `journal/booktitle`
- Verificar que não há entradas duplicadas (por DOI)
- Contar N fontes encontradas vs. N mínimo definido no PRD

**Self-review:** Agente avalia cobertura temática da literatura vs. questões de pesquisa do PRD.

**Agentic review:** Agente gera relatório de gaps: "Questão X do PRD não tem fontes suficientes — sugerir busca adicional?"

**Checkpoint:** Opcional (interativo) ou automático (auto).

---

### 6.5 Skill: `academic-writer`

**Propósito:** Redação completa do artigo, seção por seção, seguindo o outline aprovado.

**Fontes absorvidas:** academic-writing, academic-writing-style, scientific-writing, academic-paper, scientific-paper

> **Nota de consolidação:** `scientific-paper` e `academic-paper` serão analisados para remover duplicidades. Práticas antagonistas (ex. diferentes abordagens de introdução) serão resolvidas em favor das melhores práticas do campo. A skill consolidada deve cobrir tanto research articles quanto reviews.

**Trigger:** `/academic-writer`, "escrever seção", "redigir artigo", "escrever introdução"

**Modos:**
- `section` — redige uma seção específica
- `full` — redige o artigo completo seção por seção com checkpoints entre seções
- `continue` — continua rascunho existente a partir de `draft/outline.md`

**Inputs:** `prd.md`, `draft/outline.md`, `research/literature.md`, `research/references.bib`

**Outputs:** `draft/*.md` — uma seção por arquivo

**Estruturas suportadas:**
- IMRaD (Introduction, Methods, Results, Discussion)
- Revisão sistemática (Introduction, Methods, Results, Discussion, Conclusion)
- Temática (seções livres definidas no PRD)
- Estudo de caso

**Checkers por seção:**
- Introdução: tem contexto + gap + objetivo + estrutura do paper
- Métodos: tem design, amostra/dataset, variáveis, protocolo reprodutível
- Resultados: não contém interpretação (apenas fatos e dados)
- Discussão: conecta resultados às questões de pesquisa
- Conclusão: não introduz novos dados, tem limitações e trabalhos futuros

**Self-review:** Após cada seção, agente verifica:
1. Seção atende ao outline aprovado?
2. Todas as citações são referenciadas como `[KEY]` ou `\cite{key}`?
3. Registro acadêmico mantido (sem linguagem coloquial)?
4. Contagem de palavras vs. alocação no outline?

**Agentic review:** Após draft completo, agente faz revisão transversal:
- Consistência de terminologia entre seções
- Fluxo lógico de argumentação
- Lacunas de evidência (afirmações sem citação)

**Integração com academic-media:** Quando detectar necessidade de figura/esquema/EDA, emite chamada explícita: `→ academic-media: {descrição do elemento visual necessário}`

**Checkpoint:** Obrigatório após outline; opcional após cada seção (modo interativo).

---

### 6.6 Skill: `academic-citation-manager`

**Propósito:** Gestão e validação de citações in-text — formato, completude e consistência.

**Fontes absorvidas:** citation-anchoring, citation-audit, citation-validator, citation-management

**Trigger:** `/academic-citation-manager`, "verificar citações", "formatar referências in-text"

**Responsabilidades:**
- Rastrear todas as ocorrências de `\cite{key}` / `(Autor, Ano)` no draft
- Validar formato de citação conforme estilo do PRD (APA, IEEE, ABNT etc.)
- Identificar citações órfãs (no texto mas sem entrada no `.bib`)
- Identificar citações fantasma (no `.bib` mas não citadas no texto)

**Gate de Validação Cruzada (com bibliography-manager):**
```
VERIFICAR: ∀ citação no draft → existe entrada correspondente em references.bib
VERIFICAR: ∀ entrada em references.bib → é citada pelo menos uma vez no draft
RESULTADO: ✅ Consistente | ❌ N inconsistências encontradas
```

**Outputs:**
- Relatório de validação: `review/citation-report.md`
- Draft com citações corrigidas

**Validações determinísticas:**
- Contagem de citações únicas vs. entradas no `.bib`
- Verificação de formato por estilo (ex. APA: `(Autor, Ano)`, IEEE: `[N]`)
- Detecção de duplicatas: mesma obra citada com chaves diferentes

**Self-review:** Agente re-executa o gate após correções para confirmar 0 inconsistências.

**Checkpoint:** Gate de validação cruzada é checkpoint obrigatório antes de revisão.

---

### 6.7 Skill: `academic-bibliography-manager`

**Propósito:** Gestão e validação do `references.bib` — completude, formato e enriquecimento via OpenAlex.

**Fontes absorvidas:** citation-bibliography-generator, openalex-database

**Integração OpenAlex (como dependência interna):**
- Resolver DOI → metadados completos → BibTeX
- Verificar existência e retração de artigos via `is_retracted`
- Enriquecer entradas incompletas com dados do OpenAlex

**Trigger:** `/academic-bibliography-manager`, "validar bibliografia", "gerar BibTeX", "resolver DOI"

**Responsabilidades:**
- Validar completude de cada entrada BibTeX (campos obrigatórios por tipo)
- Enriquecer entradas incompletas via OpenAlex
- Detectar e remover duplicatas
- Formatar saída conforme estilo do PRD

**Campos obrigatórios por tipo BibTeX:**
```
@article:      author, title, journal, year, volume, pages
@inproceedings: author, title, booktitle, year
@book:         author/editor, title, publisher, year
@misc:         author, title, year, url, note (acesso)
```

**Outputs:**
- `research/references.bib` — validado e enriquecido
- Relatório de validação: `review/bibliography-report.md`

**Validações determinísticas:**
```bash
# Verificar campos obrigatórios em cada entrada
python scripts/validate_bib.py research/references.bib

# Verificar duplicatas por DOI
python scripts/check_bib_duplicates.py research/references.bib
```

**Self-review:** Agente relê o `.bib` inteiro e verifica que 0 entradas têm campos obrigatórios faltando.

**Checkpoint:** Executado antes do gate de validação cruzada com citation-manager.

---

### 6.8 Skill: `academic-reviewer`

**Propósito:** Revisão acadêmica completa do artigo em 5 dimensões.

**Fontes absorvidas:** academic-paper-reviewer, scientific-validation, scientific-manuscript-review

**Trigger:** `/academic-reviewer`, "revisar artigo", "peer review", "avaliar paper"

**Dimensões de Revisão (5-D):**
1. **Rigor científico** — metodologia, reprodutibilidade, validade estatística
2. **Coerência argumentativa** — fluxo lógico, claim-evidence chains
3. **Integridade bibliográfica** — cobertura da literatura, citações adequadas
4. **Qualidade da escrita** — clareza, coesão, registro acadêmico
5. **Conformidade de formato** — aderência ao template/estilo do PRD

**Modos:**
- `full` — revisão completa em todas as 5 dimensões
- `focused` — revisão focada em dimensões específicas (pós-revisão)
- `quick` — checklist rápido antes de submissão

**Outputs:**
- `review/review-report.md` — relatório detalhado com pontuação por dimensão e sugestões
- `review/revision-log.md` — histórico de revisões

**Self-review:** Agente verifica consistência interna do relatório antes de entregar.

**Agentic review:** Segunda passagem após revisões do usuário — verifica se os pontos levantados foram endereçados.

**Checkpoint:** Obrigatório após revisão completa; obrigatório após re-revisão pós-correção.

---

### 6.9 Skill: `academic-humanizer`

**Propósito:** Ajuste de registro, humanização e naturalização da escrita acadêmica.

**Fontes absorvidas:** humanize, humanize-academic-writing, finnish-humanizer

**Trigger:** `/academic-humanizer`, "humanizar", "ajustar registro", "naturalizar escrita"

**Responsabilidades:**
- Manter registro acadêmico mas remover artificialidade de texto gerado por IA
- Adaptar tom conforme disciplina e tipo de paper
- Preservar terminologia técnica
- Garantir consistência de voz ao longo do documento

**Self-review:** Agente verifica que não foram introduzidas informações factuais novas (apenas ajustes de forma).

**Checkpoint:** Opcional — executado antes da revisão final ou após revisão do reviewer.

---

### 6.10 Skill: `academic-media`

**Propósito:** Criação de figuras, esquemas, diagramas e análises exploratórias de dados para artigos acadêmicos. Pode ser invocada pelo writer ou usada de forma avulsa.

**Fontes absorvidas:** scientific-eda, scientific-paper-figure-generator, scientific-schematics

**Trigger:** `/academic-media`, "criar figura", "gerar esquema", "análise exploratória", "EDA"

**Modos:**
- `figure` — gera figuras de resultados (gráficos, plots)
- `schematic` — gera diagramas conceituais e workflows
- `eda` — executa análise exploratória de dados e gera visualizações

**Outputs:** Arquivos de imagem em `output/figures/` + código de geração em `output/figures/scripts/`

**Validações determinísticas:**
- Verificar que as figuras geradas têm caption, label e referência no texto (`\ref{fig:X}`)
- Verificar resolução mínima para publicação (300 DPI)

**Self-review:** Agente verifica aderência da figura ao estilo visual do template especificado no PRD.

**Integração:** Pode ser chamada diretamente (`/academic-media figure "descrição"`) ou via writer.

---

## 7. Especificação dos Agentes

### 7.1 Agente: `academic-orchestrator`

**Propósito:** Coordenador master do pipeline — executa as fases em ordem, despacha as skills corretas, gerencia checkpoints e mantém estado de sessão.

**Referência:** Baseado em `academic-pipeline v2.7` (`.agents_old/skills/academic-pipeline/skill.md`)

**Trigger:** `/academic-orchestrator`, "iniciar pipeline acadêmico", "escrever artigo completo"

**Dois Modos de Operação:**

```
MODO AUTO
─────────
Executa pipeline completo automaticamente.
Pausa APENAS nos checkpoints obrigatórios (5 gates).
Ideal para: usuário quer resultado final com mínima intervenção.

MODO INTERATIVO (padrão)
────────────────────────
Solicita confirmação humana em CADA fase.
Permite ajustes, feedback e redirecionamento entre fases.
Ideal para: usuário quer controle total, primeira vez no sistema.
```

**Checkpoints Obrigatórios (ambos os modos):**

| Gate | Após | Antes de |
|---|---|---|
| G1 | Academic PRD gerado | Implementation Plan |
| G2 | Implementation Plan aprovado | Literature Research |
| G3 | Outline aprovado | Full-text Drafting |
| G4 | Gate Citation↔Bibliography (0 erros) | Humanization/Review |
| G5 | Review final aceito | Output Formatting |

**Checkpoints Opcionais (modo interativo):**
- Após literatura revisada
- Após cada seção redigida
- Após humanização
- Antes de exportar formato final

**Capacidades do Orchestrator:**
- Detectar em qual fase o projeto está (mid-entry)
- Ler `plan.md` para rastrear progresso
- Atualizar checklist de tasks no `plan.md` após cada fase
- Gerar `process-record.md` ao final com histórico da sessão
- Modo de entrada no meio do pipeline: "já tenho o draft, quero revisão"

**Status Dashboard** (disponível a qualquer momento com `/status`):
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
...
```

**Skills utilizadas:**
- Todas as pipeline skills (Camada 2)
- Tools skills conforme necessidade (Camada 1)

---

### 7.2 Agente: `research-agent`

**Propósito:** Agente especializado na fase de pesquisa — pode ser usado de forma independente do orchestrator.

**Skills utilizadas:** `academic-researcher` + `academic-bibliography-manager`

**Trigger:** Invocado pelo orchestrator na Fase 2, ou diretamente pelo usuário.

**Responsabilidade:** Produzir `literature.md` + `references.bib` validados prontos para o writer.

---

### 7.3 Agente: `writing-agent`

**Propósito:** Agente especializado na fase de redação — coordena writer + media.

**Skills utilizadas:** `academic-writer` + `academic-media` (quando necessário) + `academic-humanizer`

**Trigger:** Invocado pelo orchestrator nas Fases 4-6, ou diretamente pelo usuário.

---

### 7.4 Agente: `review-agent`

**Propósito:** Agente especializado na fase de revisão — executa ciclo completo de revisão.

**Skills utilizadas:** `academic-citation-manager` + `academic-bibliography-manager` + `academic-reviewer`

**Ciclo:**
1. Gate Citation↔Bibliography (determinístico)
2. Revisão 5-D
3. Aguarda correções
4. Re-review focado

**Trigger:** Invocado pelo orchestrator nas Fases 5-7, ou diretamente pelo usuário com paper existente.

---

### 7.5 Agente: `paper-generator-agent`

**Propósito:** Agente especializado na geração do paper final em formato publicável — converte o draft revisado em LaTeX compilado, gerando o PDF acadêmico definitivo.

**Skills utilizadas:** `latex` + `latex-template-converter` + `pdf`

**Trigger:** `/paper-generator`, "gerar paper final", "compilar LaTeX", "gerar PDF do artigo", "exportar paper". Invocado pelo orchestrator na Fase 8 (Output Formatting).

**Pipeline Interno:**

```
1. Consolidação do draft
   ├── Ler draft/*.md (todas as seções aprovadas)
   ├── Montar ordem: abstract → introduction → methodology
   │   → results → discussion → conclusion
   └── Verificar que todas as seções obrigatórias existem

2. Seleção e configuração do template LaTeX
   ├── Ler prd.md → identificar template de conferência/publicação
   ├── Se template especificado: invocar latex-template-converter
   │   para organizar e configurar o template
   └── Se sem template: usar estrutura LaTeX padrão acadêmica

3. Geração do paper.tex
   ├── Converter conteúdo Markdown → LaTeX
   │   ├── Seções → \section{}, \subsection{}
   │   ├── Figuras → \includegraphics{} + \caption{} + \label{}
   │   ├── Tabelas → ambiente tabular/booktabs
   │   ├── Equações → ambientes equation/align
   │   └── Citações [KEY] → \cite{key}
   ├── Inserir references.bib via \bibliography{}
   ├── Configurar \bibliographystyle{} conforme estilo do PRD
   └── Escrever output/paper.tex

4. Compilação LaTeX → PDF
   ├── Executar pdflatex (2 passes para referências cruzadas)
   ├── Executar bibtex / biber para bibliografia
   ├── Executar pdflatex (2 passes finais)
   └── Verificar: compilação sem erros → output/paper.pdf

5. Validação do PDF gerado
   ├── Verificar que paper.pdf existe e não está corrompido
   ├── Verificar contagem de páginas (≥ 1)
   ├── Verificar que todas as seções aparecem no PDF
   └── Verificar que referências bibliográficas foram resolvidas

6. Geração opcional de DOCX
   └── Se prd.md especifica DOCX como saída adicional:
       invocar skill docx para gerar output/paper.docx
```

**Inputs:**
- `prd.md` — requisitos (template, estilo de citação, formato de saída, língua)
- `draft/*.md` — todas as seções do artigo revisadas e aprovadas
- `research/references.bib` — bibliografia validada pelo review-agent
- `output/figures/` — imagens e figuras geradas pelo academic-media
- Template LaTeX (se especificado no PRD)

**Outputs:**
- `output/paper.tex` — fonte LaTeX completa e compilável
- `output/paper.pdf` — PDF final gerado por pdflatex/xelatex
- `output/paper.docx` — versão Word (opcional, se especificado no PRD)
- `output/compilation-log.txt` — log completo da compilação para diagnóstico

**Validações Determinísticas (Gate LaTeX):**
```bash
# Compilação deve terminar com exit code 0
pdflatex -interaction=nonstopmode output/paper.tex
echo "Exit code: $?"   # deve ser 0

# PDF deve existir e ter tamanho > 0
test -s output/paper.pdf && echo "PDF OK" || echo "PDF AUSENTE"

# Verificar ausência de erros críticos no log
grep -c "! " output/compilation-log.txt  # deve ser 0

# Verificar warnings de referências não resolvidas
grep "Citation .* undefined" output/compilation-log.txt  # deve ser vazio
grep "Reference .* undefined" output/compilation-log.txt # deve ser vazio
```

**Gate LaTeX (bloqueante):**
```
VERIFICAR: compilação pdflatex termina com exit code 0
VERIFICAR: output/paper.pdf gerado com tamanho > 0
VERIFICAR: 0 erros críticos no log (linhas iniciando com "! ")
VERIFICAR: 0 citações não resolvidas no log
RESULTADO: ✅ Paper gerado | ❌ Compilação falhou — exibir erros e aguardar correção
```

**Tratamento de Erros de Compilação:**

| Erro | Causa Comum | Ação do Agente |
|---|---|---|
| `! Undefined control sequence` | Comando LaTeX inválido no draft | Identificar linha, sugerir correção |
| `Citation X undefined` | Chave não existe no .bib | Invocar academic-bibliography-manager para resolver |
| `File X.sty not found` | Pacote LaTeX não instalado | Listar pacotes faltantes, instruir instalação |
| `Overfull \hbox` | Linha longa demais | Corrigir automaticamente (quebra de linha, hifenização) |
| `Missing $ inserted` | Fórmula fora de ambiente math | Identificar e corrigir delimitadores |

**Self-review:**
1. Agente verifica que o PDF gerado contém todas as seções previstas no outline
2. Agente verifica contagem de páginas vs. limite do PRD (se especificado)
3. Agente verifica que metadados do PDF (título, autor) estão corretos
4. Agente verifica que todas as figuras apareceram corretamente (sem placeholders "??" no PDF)

**Checkpoint:** Gate LaTeX é checkpoint obrigatório (G5.5) — pipeline não avança para Process Documentation se compilação falhar.

---

## 8. Requisitos de Integração

### 8.1 OpenAlex

OpenAlex vive como **dependência interna** de duas skills — não é uma skill autônoma:

| Skill | Uso do OpenAlex | Tipo de uso |
|---|---|---|
| `academic-researcher` | Busca de literatura por keywords, filtros, citações | Busca |
| `academic-bibliography-manager` | Resolução DOI → metadados → BibTeX, verificação retração | Enriquecimento |

**Configuração base (ambas as skills):**
```bash
# Polite pool: 10 req/s com email
BASE_URL="https://api.openalex.org"
MAILTO="user@institution.edu"  # configurável no PRD

# Exemplo: resolver DOI
curl -s "${BASE_URL}/works/https://doi.org/10.1038/nature12345?mailto=${MAILTO}"
```

### 8.2 Gate Citation ↔ Bibliography

Regra de negócio cross-cutting executada pelo `review-agent` antes de avançar para revisão:

```
REGRA 1: ∀ key em \cite{key} no draft → ∃ entrada @{type}{key,...} em references.bib
REGRA 2: ∀ key em references.bib → ∃ pelo menos 1 \cite{key} no draft
REGRA 3: ∀ entry em references.bib → campos obrigatórios por tipo preenchidos

RESULTADO ESPERADO: 0 violações de REGRA 1, REGRA 2, REGRA 3
BLOQUEANTE: Sim — pipeline não avança se resultado ≠ 0 violações
```

### 8.3 Validações Determinísticas por Fase

| Fase | Validação | Bloqueante |
|---|---|---|
| PRD | 10 campos obrigatórios preenchidos | Sim |
| Plano | Todas as 9 fases representadas | Sim |
| Pesquisa | N mínimo de fontes, .bib sem duplicatas | Sim |
| Redação | Checkers por seção (ver §6.5) | Parcial |
| Citação | Gate Citation↔Bibliography | Sim |
| LaTeX | Compilação sem erros (`pdflatex`) | Sim |
| PDF | Verificação visual de formatação | Não (apenas alerta) |

---

## 9. Padrão de Criação de Skills

### 9.1 Referência Normativa: `creating-skills`

**Toda criação, consolidação ou modificação de skill no tolkien deve obrigatoriamente seguir os conceitos, princípios e especificações definidos na skill `creating-skills`** (`.claude/skills/creating-skills/` e `.agents/skills/creating-skills/`).

Esta skill é a **referência normativa** para qualquer trabalho de implementação de skills neste projeto. Não é opcional.

### 9.2 Princípios Obrigatórios (extraídos de `creating-skills`)

**1. Conciseness — Contexto é recurso compartilhado**
- Incluir apenas o que o agente não sabe por padrão
- Questionar cada linha: "Claude precisa disso? Ele já sabe?"
- Focar no que é único ao domínio acadêmico e ao workflow específico

**2. Progressive Disclosure (3 níveis de carregamento)**

| Nível | Quando carrega | Custo | Conteúdo |
|---|---|---|---|
| L1: Metadata | Sempre (startup) | ~100 tokens | YAML `name` + `description` |
| L2: Instructions | Quando a skill dispara | < 5.000 tokens | Corpo do `skill.md` |
| L3: Resources | Sob demanda | Ilimitado | `scripts/`, `references/`, `assets/` |

Regras:
- `skill.md` deve ter **menos de 500 linhas**
- Conteúdo detalhado vai para `references/`
- Referências devem ser **um nível de profundidade** — sem cadeias aninhadas

**3. Graus de Liberdade Adequados**
- Alta liberdade (orientação em texto): múltiplas abordagens válidas
- Média liberdade (pseudocódigo/templates): existe um padrão preferido
- Baixa liberdade (código exato): uma única forma correta

**4. Estrutura de Diretório por Skill**

```
{skill-name}/
├── skill.md          ← instrução principal (< 500 linhas)
├── references/       ← documentação detalhada sob demanda
│   └── *.md
├── scripts/          ← scripts executáveis (checkers, validadores)
│   └── *.py / *.sh
└── assets/           ← templates, exemplos, artefatos estáticos
    └── *
```

**5. Frontmatter Obrigatório**

```yaml
---
name: {skill-name}
description: >
  {descrição precisa de quando usar — palavras-chave de trigger}
  {incluir exemplos de frases que disparam a skill}
allowed-tools: [Read, Write, Edit, Bash, ...]
metadata:
  version: "1.0"
  depends_on: "{skills dependentes, separadas por vírgula}"
---
```

**6. Seções Obrigatórias no `skill.md`**
- `## When To Use` — triggers explícitos
- `## When Not To Use` — exclusões claras para evitar ativação incorreta
- `## Prerequisites` — o que coletar antes de executar
- Protocolo de self-review (determinístico + agêntico)

**7. Regras para Consolidação de Skills Legadas**
- Analisar cada skill a ser absorvida antes de consolidar
- Remover duplicidades — se duas skills ensinam a mesma coisa, manter apenas a melhor versão
- Remover antagonismos — se duas skills têm abordagens contraditórias, decidir qual prevalece e documentar o motivo
- Manter as melhores práticas determinísticas de cada skill absorvida
- Não copiar conteúdo que Claude já sabe (sobrecarga de contexto)

**8. Validação Antes de Deploy**
Toda nova skill deve ser validada contra os critérios de `creating-skills` antes de ser considerada pronta:
- Frontmatter completo e correto
- Triggers bem definidos (sem ambiguidade)
- `skill.md` dentro do limite de 500 linhas
- Scripts em `scripts/` se houver lógica determinística
- Testada em Claude Code E OpenCode

### 9.3 Aplicação ao tolkien

Para cada skill listada no Roadmap (§14), o processo de implementação é:

```
1. Ler todas as skills legadas a absorver (ver §15)
2. Identificar: duplicidades, antagonismos, melhores práticas
3. Decidir: o que manter, o que descartar, o que unificar
4. Implementar seguindo creating-skills (estrutura, frontmatter, limites)
5. Colocar validações determinísticas em scripts/
6. Colocar conteúdo extenso em references/
7. Validar contra creating-skills antes de finalizar
8. Sincronizar .claude/skills/ ↔ .agents/skills/ via multi-ide-artifacts
```

---

## 11. Compatibilidade Cross-IDE

### 9.1 Estrutura de Arquivos

```
.claude/skills/          ← Claude Code
.agents/skills/          ← OpenCode

Ambos devem conter as mesmas skills com mesmo conteúdo.
Usar multi-ide-artifacts para sincronização e conversão.
```

### 9.2 Formato de Skill

Todas as skills devem seguir o padrão definido em `creating-skills`:

```markdown
---
name: {skill-name}
description: {trigger description — quando usar, palavras-chave}
allowed-tools: [Read, Write, Edit, Bash, ...]
metadata:
  version: "1.0"
  depends_on: "{skills dependentes}"
---

# {Skill Name}
...
```

### 9.3 Compatibilidade de Comandos

Todos os scripts Bash dentro das skills devem ser compatíveis com:
- macOS (zsh/bash) — `brew`-based dependencies
- Linux (bash) — `apt`/`pip`-based dependencies

Padrão de detecção:
```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
else
  # Linux
fi
```

---

## 12. Protocolo de Self-Review

Cada skill deve implementar self-review em dois níveis:

### Nível 1: Self-review Determinístico
- Checkers automatizados (scripts, contagens, validações de formato)
- Resultado binário: ✅ / ❌
- Exemplos: compilação LaTeX, contagem de campos BibTeX, gate citation↔bib

### Nível 2: Self-review Agêntico
- O agente relê seu próprio output e avalia qualidade
- Resultado: relatório de qualidade com sugestões de melhoria
- Exemplos: cobertura temática da literatura, coerência argumentativa do draft

**Template de self-review agêntico:**
```
### Self-Review: {nome da fase}
- Completude: {N/N critérios atendidos}
- Qualidade: {avaliação qualitativa}
- Pontos de atenção: {lista de itens para verificação humana}
- Recomendação: ✅ Prosseguir | ⚠️ Revisar antes de prosseguir
```

---

## 13. Critérios de Aceite (BDD)

```gherkin
Feature: Pipeline Completo

  Scenario: Criação de artigo do zero
    Given um usuário inicia /academic-orchestrator
    When completa a entrevista de configuração
    Then prd.md é gerado com 10 campos obrigatórios preenchidos
    And o usuário deve confirmar o prd.md antes de avançar

  Scenario: Validação Citation↔Bibliography
    Given um draft completo com citações
    And um references.bib com entradas
    When o review-agent executa o gate de validação
    Then toda \cite{key} do draft deve ter entrada correspondente no .bib
    And toda entrada no .bib deve ser citada no draft
    And o pipeline NÃO avança se houver violações

  Scenario: Compilação LaTeX
    Given output/paper.tex gerado
    When a skill latex executa pdflatex
    Then deve compilar sem erros
    And deve gerar output/paper.pdf legível
    And o pipeline NÃO avança se houver erros de compilação

  Scenario: Compatibilidade Cross-IDE
    Given uma skill criada em .claude/skills/
    When multi-ide-artifacts sincroniza
    Then a mesma skill deve existir em .agents/skills/
    And ambas as versões devem ter o mesmo comportamento

  Scenario: Mid-entry no pipeline
    Given um paper já com draft em draft/*.md
    When usuário inicia /academic-orchestrator
    Then o orchestrator detecta a fase atual
    And oferece continuar a partir da fase correta
    And não reprocessa fases já concluídas
```

---

## 14. Roadmap de Implementação

### Prioridade 1 — Fundação Meta-Skills (sem dependências)
1. `academic-prd` — base de todo o pipeline
2. `academic-plan` — depende apenas de prd.md

### Prioridade 2 — Skills de Pesquisa
3. `academic-researcher` — consolidação + OpenAlex integration
4. `academic-bibliography-manager` — consolidação + OpenAlex DOI resolution

### Prioridade 3 — Skills de Redação
5. `academic-writer` — consolidação maior, requer análise de duplicidades
6. `academic-citation-manager` — consolidação + deterministic gate
7. `academic-media` — consolidação, usada como dependência do writer

### Prioridade 4 — Skills de Revisão e Qualidade
8. `academic-reviewer` — consolidação
9. `academic-humanizer` — consolidação

### Prioridade 5 — Agentes
10. `review-agent` — usa skills 4, 6, 8 (todas prontas)
11. `research-agent` — usa skills 3, 4 (prontas)
12. `writing-agent` — usa skills 5, 7, 9 (prontas)
13. `paper-generator-agent` — usa skills latex, latex-template-converter, pdf (todas prontas)
14. `academic-orchestrator` — usa todos os agentes e skills (last)

### Prioridade 6 — Cross-IDE Sync
15. Sincronização `.claude/skills/` ↔ `.agents/skills/` via `multi-ide-artifacts`

---

## 15. Referências de Skills Legadas

Para implementação de cada skill, consultar as seguintes skills legadas em `.agents_old/skills/`:

| Skill a criar | Ler antes de implementar |
|---|---|
| `academic-prd` | `academic-pipeline/skill.md` (seção de workflow), `skills.md` (seção PRD) |
| `academic-plan` | `academic-pipeline/skill.md` (stages e deliverables) |
| `academic-researcher` | `academic-researcher/`, `academic-deep-research/`, `openalex-paper-search/` |
| `academic-writer` | `academic-writing/`, `academic-writing-style/`, `scientific-writing/`, `academic-paper/`, `scientific-paper/` |
| `academic-citation-manager` | `citation-anchoring/`, `citation-audit/`, `citation-validator/`, `citation-management/` |
| `academic-bibliography-manager` | `citation-bibliography-generator/`, `openalex-database/` |
| `academic-reviewer` | `academic-paper-reviewer/`, `scientific-validation/`, `scientific-manuscript-review/` |
| `academic-humanizer` | `humanize/`, `humanize-academic-writing/`, `finnish-humanizer/` |
| `academic-media` | `scientific-eda/`, `scientific-paper-figure-generator/`, `scientific-schematics/` |
| `academic-orchestrator` | `academic-pipeline/skill.md` (estrutura de orquestração e checkpoints) |
| `paper-generator-agent` | `latex/skill.md`, `latex-template-converter/skill.md`, `pdf/skill.md` (skills de ferramenta já prontas) |

---

## 16. Glossário

| Termo | Definição |
|---|---|
| **Academic PRD** | Documento de requisitos do artigo (equivalente ao spec.md no SDD) |
| **SDD** | Spec-Driven Development — abordagem de desenvolvimento guiado por especificação |
| **Gate** | Validação bloqueante que impede avanço do pipeline se critérios não forem atendidos |
| **Checkpoint** | Ponto de confirmação humana obrigatória ou opcional |
| **Self-review determinístico** | Verificação automatizada com resultado binário (script/contagem) |
| **Self-review agêntico** | Avaliação qualitativa do próprio output pelo agente |
| **Citation↔Bibliography Gate** | Validação cruzada entre citações in-text e entradas no .bib |
| **Mid-entry** | Entrada no pipeline em uma fase que não a inicial |
| **tolkien** | Academic Article Production Multi-Agent System — nome do sistema |
