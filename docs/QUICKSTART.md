# Quick Start / Início Rápido

---

## English — 5-Minute Crash Course

### 1. Install

Run from the tolkien repository root:

```bash
bash resources/install_skills_deps.sh
source .venv/bin/activate
```

That's it — the script installs all system packages (Tesseract, Poppler, TinyTeX, LibreOffice), Node.js packages, and Python dependencies.

The `resources/` directory contains:
- `install_skills_deps.sh` — main installer script
- `requirements_skills.txt` — Python package list

**Templates:** Before starting, you can copy `templates/research_request_form.md` to prepare your paper requirements offline.

### 2. Start a New Paper

In Claude Code or OpenCode, run:

```
/academic-orchestrator "Start a new paper about [your topic]"
```

The orchestrator will interview you for ~10 minutes to build `prd.md`, then run the pipeline automatically.

### 3. Work Through the Gates

The pipeline pauses at 6 checkpoints. Your job at each one:

| Gate | What to do |
|------|-----------|
| G1 — After PRD | Review `prd.md`. Confirm all 10 fields are correct. |
| G2 — After Plan | Review `plan.md`. Confirm the 9-phase roadmap matches your intent. |
| G3 — After Outline | Review `draft/outline.md`. Confirm section structure and word budgets. |
| G4 — After Citations | Review `review/citation-report.md`. Fix any violations, then re-run `/review-agent "verify citations"`. |
| G5 — After Review | Review `review/review-report.md`. If score < 65, revise with `/writing-agent` and re-run `/review-agent`. |
| G5.5 — After LaTeX | Confirm `output/paper.pdf` opens and renders correctly. |

### 4. Find Your Output

All deliverables land in `output/`:

```
papers/paper-{slug}/output/
├── paper.pdf      # Final compiled PDF
├── paper.tex      # LaTeX source
└── paper.docx     # Word document
```

### Common Pitfalls

- **Forgetting to activate `.venv`** — Python skills will fail. Run `source .venv/bin/activate` first.
- **Skipping gate review** — The gates exist to catch problems early. Do not approve a gate without reading its output file.
- **Wrong project root** — Paper projects must be under `projects/`, `papers/`, `.projects/`, or `.papers/`. Projects outside these directories may not be recognized.
- **Stale `references.bib`** — If you add citations to the draft manually, re-run `/academic-bibliography-manager` to enrich and validate the new entries.

### Key Commands at a Glance

```bash
# Full pipeline (recommended)
/academic-orchestrator "topic"

# Individual agents
/research-agent       # literature search
/writing-agent        # drafting + humanization
/review-agent         # citation check + peer review
/paper-generator      # compile PDF/DOCX

# Individual skills
/academic-prd                    # PRD interview only
/academic-researcher             # OpenAlex search only
/academic-citation-manager       # citation audit only
/academic-bibliography-manager   # bibliography validation only
/academic-reviewer               # peer review only
/latex                           # LaTeX compile only
```

---

---

## Português — Início Rápido em 5 Minutos

### 1. Instalação

Execute na raiz do repositório tolkien:

```bash
bash resources/install_skills_deps.sh
source .venv/bin/activate
```

Pronto — o script instala todos os pacotes do sistema (Tesseract, Poppler, TinyTeX, LibreOffice), pacotes Node.js e dependências Python.

O diretório `resources/` contém:
- `install_skills_deps.sh` — script principal de instalação
- `requirements_skills.txt` — lista de pacotes Python

**Templates:** Antes de começar, você pode copiar `templates/research_request_form.md` para preparar os requisitos do seu artigo offline.

### 2. Iniciar um Novo Artigo

No Claude Code ou OpenCode, execute:

```
/academic-orchestrator "Iniciar um novo artigo sobre [seu tema]"
```

O orquestrador vai conduzi-lo por uma entrevista de ~10 minutos para construir o `prd.md` e depois executar o pipeline automaticamente.

### 3. Passar pelos Gates

O pipeline pausa em 6 checkpoints. O que fazer em cada um:

| Gate | O que fazer |
|------|------------|
| G1 — Após o PRD | Revise `prd.md`. Confirme que todos os 10 campos estão corretos. |
| G2 — Após o Plano | Revise `plan.md`. Confirme que o roteiro de 9 fases corresponde à sua intenção. |
| G3 — Após o Outline | Revise `draft/outline.md`. Confirme a estrutura de seções e as alocações de palavras. |
| G4 — Após Citações | Revise `review/citation-report.md`. Corrija as violações e re-execute `/review-agent "verificar citações"`. |
| G5 — Após Revisão | Revise `review/review-report.md`. Se a pontuação < 65, revise com `/writing-agent` e re-execute `/review-agent`. |
| G5.5 — Após LaTeX | Confirme que `output/paper.pdf` abre e renderiza corretamente. |

### 4. Encontrar os Resultados

Todos os entregáveis vão para `output/`:

```
papers/paper-{slug}/output/
├── paper.pdf      # PDF compilado final
├── paper.tex      # Código-fonte LaTeX
└── paper.docx     # Documento Word
```

### Armadilhas Comuns

- **Esquecer de ativar o `.venv`** — Skills Python vão falhar. Execute `source .venv/bin/activate` antes.
- **Pular a revisão de gate** — Os gates existem para detectar problemas cedo. Não aprove um gate sem ler o arquivo de saída correspondente.
- **Diretório raiz errado** — Projetos de artigos devem estar em `projects/`, `papers/`, `.projects/` ou `.papers/`. Projetos fora desses diretórios podem não ser reconhecidos.
- **`references.bib` desatualizado** — Se você adicionar citações ao rascunho manualmente, re-execute `/academic-bibliography-manager` para enriquecer e validar as novas entradas.

### Comandos Principais em Resumo

```bash
# Pipeline completo (recomendado)
/academic-orchestrator "tema"

# Agentes individuais
/research-agent       # busca bibliográfica
/writing-agent        # redação + humanização
/review-agent         # verificação de citações + revisão por pares
/paper-generator      # compilar PDF/DOCX

# Skills individuais
/academic-prd                    # apenas entrevista do PRD
/academic-researcher             # apenas busca no OpenAlex
/academic-citation-manager       # apenas auditoria de citações
/academic-bibliography-manager   # apenas validação da bibliografia
/academic-reviewer               # apenas revisão por pares
/latex                           # apenas compilação LaTeX
```
