# Início Rápido — tolkien em 5 Minutos

> **Idioma / Language:** Português | [English Version](../QUICKSTART.md)

---

### 1. Instalação

Execute na raiz do repositório tolkien:

```bash
bash resources/install_skills_deps.sh
source .venv/bin/activate
```

O script instala todos os pacotes do sistema (Tesseract, Poppler, TinyTeX, LibreOffice), pacotes Node.js, Chromium do Playwright e dependências Python.

O diretório `resources/` contém:
- `install_skills_deps.sh` — script principal de instalação
- `requirements_skills.txt` — lista de pacotes Python

**Templates:** Antes de começar, você pode copiar `templates/research_request_form.md` para preparar os requisitos do seu artigo offline.

---

### 2. Iniciar um Novo Artigo

No Google Antigravity, Claude Code, OpenCode ou Codex, execute:

```bash
/academic-orchestrator "Iniciar um novo artigo sobre [seu tema]"
```

O orquestrador vai conduzi-lo por uma entrevista estruturada de ~10 minutos para construir o `prd.md` e depois coordenar o avanço pelos gates.

---

### 3. Passar pelos Gates

O pipeline possui checkpoints mandatórios de qualidade (Gates) e executa um **Loop Contínuo de Revisão** nas Fases 5 a 7:

| Gate | Fase | O que fazer |
|------|------|------------|
| **G1** | Após o PRD | Revise `prd.md`. Confirme que todos os 10 campos mandatórios estão preenchidos. |
| **G2** | Após o Plano | Revise `plan.md`. Confirme que o roteiro cobre todas as fases necessárias. |
| **G3** | Após o Outline | Revise `draft/outline.md`. Confirme a estrutura de seções, orçamentos de palavras e Fichas de Escopo. |
| **G4** | Após Citações | Revise `review/citation-report.md`. Certifique-se de 0 citações órfãs e 0 chaves fantasmas. |
| **G4.5** | Após Integridade de Dados | Revise `review/data-congruence-report.md`. Verifique se os números da prosa conferem com tabelas/figuras, integridade de floats e totais aritméticos. |
| **G5** | Após Revisão por Pares | Revise `review/review-report.md`. Se a pontuação < 65 ou houver itens CRÍTICOS do Advogado do Diabo, o Loop Contínuo reescreve as seções afetadas até aprovação completa. |
| **Output Format Gate** | Após Entregáveis | Revise `review/format-validation-report.md`. Confirme que Markdown, LaTeX e Word (.docx) compilam sem erros estruturais. |

---

### 4. Encontrar os Resultados

Todos os entregáveis vão para `output/`:

```
papers/paper-{slug}/output/
├── paper.pdf      # PDF compilado final
├── paper.tex      # Código-fonte LaTeX
├── paper.docx     # Documento Word
└── figures/       # Figuras e diagramas gerados
```

---

### Armadilhas Comuns

- **Esquecer de ativar o `.venv`** — Skills Python vão falhar. Execute `source .venv/bin/activate` antes.
- **Pular a revisão de gate** — Os gates existem para detectar problemas cedo. Leia os relatórios em `review/` antes de aprovar.
- **Diretório raiz errado** — Projetos de artigos devem estar em `projects/`, `papers/`, `.projects/` ou `.papers/`.
- **`references.bib` desatualizado** — Se você adicionar citações ao rascunho manualmente, re-execute `/academic-bibliography-manager` para enriquecer e validar as novas entradas.

---

### Comandos Principais em Resumo

```bash
# Orquestrador do pipeline completo (recomendado)
/academic-orchestrator "tema"

# Agentes especializados
/research-agent          # Busca bibliográfica, triagem e referências
/writing-agent           # Redação com Scope Cards + CEI, humanização e auditoria
/review-agent            # Gate de citações, integridade de dados e revisão 6-D
/data-validation-agent   # Gate de Integridade de Dados (G4.5)
/format-validation-agent # Gate de Formatação (md/tex/docx)
/paper-generator         # Compilação final LaTeX/PDF/DOCX
/web-browser-search      # Busca web e navegação interativa

# Skills especializadas
/academic-prd                    # Apenas entrevista do PRD
/academic-plan                   # Geração do plano de implementação
/academic-researcher             # Busca bibliográfica no OpenAlex
/academic-writer                 # Redação de seções com arquitetura CEI
/academic-citation-manager       # Auditoria de citações (Gate G4)
/academic-bibliography-manager   # Validação e enriquecimento do BibTeX
/academic-data-validator         # Congruência de dados e floats (Gate G4.5)
/academic-writing-reviewer       # Auditoria de qualidade de escrita (AIM, REP, NUM, JAR)
/academic-humanizer              # Remoção de marcadores de IA em duas passadas
/academic-reviewer               # Simulação do painel de revisão 6-D
/academic-format-validator       # Validação de formatação de saída
/latex                           # Compilação e diagnóstico LaTeX
```
