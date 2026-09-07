# Tolkien — Tutorial

> **Idioma / Language:** Português | [English Version](../TUTORIAL.md)

Guia passo a passo para configuração e uso do Sistema Multiagente de Produção de Artigos Científicos.

---

## Pré-requisitos

Antes de começar, certifique-se de que seu ambiente atende aos seguintes requisitos:

| Requisito | Versão Mínima | Notas |
|-----------|---------------|-------|
| **Python** | 3.10+ | Verifique com `python3 --version` |
| **Node.js** | 18+ | Verifique com `node --version` |
| **git** | Qualquer | Para clonar o repositório |
| **Harness / CLI de IA** | Recente | **Claude Code**, **OpenCode**, **OpenAI Codex** ou **Google Antigravity** |
| **Homebrew** (macOS) ou **apt-get** (Linux) | — | Usado pelo script para instalar dependências de sistema |

---

## Instalação

### Passo 1 — Clonar o Repositório

```bash
git clone https://gitlab.com/leandroimail/tolkien.git
cd tolkien
```

### Passo 2 — Executar o Instalador de Dependências

O script instala todos os pacotes de sistema, pacotes Node.js, ferramentas de automação web e cria o ambiente virtual Python `.venv/`:

```bash
bash resources/install_skills_deps.sh
```

**O que o script instala:**

| Categoria | Pacotes |
|-----------|---------|
| Sistema (macOS) | Tesseract OCR, Poppler, TinyTeX, LibreOffice |
| Sistema (Linux) | `tesseract-ocr`, `poppler-utils`, `libreoffice`, `chromium` |
| Node.js (npm) | `docx`, `agent-browser`, `@playwright/cli` |
| Playwright | Navegador Chromium |
| Python (.venv) | `pyyaml`, `requests`, `pandas`, `matplotlib`, `pypdf`, `pdfplumber`, `reportlab`, `pillow`, `pytesseract`, `pdf2image`, `defusedxml`, `duckduckgo-search` |

### Passo 3 — Ativar o Ambiente Virtual

```bash
source .venv/bin/activate
```

Seu terminal indicará que o ambiente está ativo. Ative-o sempre que for executar scripts ou validadores Python manualmente.

Para desativar:

```bash
deactivate
```

---

## Templates Disponíveis e Governança do Artigo

O diretório `templates/` fornece bases prontas para acelerar a inicialização:

| Arquivo | Finalidade |
|---------|------------|
| `templates/research_request_form.md` | Formulário estruturado com os campos da entrevista do `academic-prd`. Preencha offline antes de iniciar. |
| `templates/systematic_review_protocol.yaml` | Protocolo alinhado ao PRISMA para revisões sistemáticas de literatura via `academic-researcher`. |
| `templates/paper/style-guide.md.template` | Diretrizes de voz autoral, assertividade e estrutura de parágrafos CEI. |
| `templates/paper/anti-style-guide.md.template` | Catálogo de clichês proibidos, marcadores de IA e vícios estilísticos (tom de mestrado). |
| `templates/paper/human-decisions.md.template` | Registro de decisões metodológicas humanas que preservam a autenticidade da autoria. |

### Diretório de Governança do Artigo (`resources/`)

Em qualquer projeto de artigo (`papers/paper-{slug}/`), você pode criar opcionalmente a pasta `resources/` contendo:
- `resources/style-guide.md`: Guia de estilo do autor.
- `resources/anti-style-guide.md`: Vícios e clichês banidos.
- `resources/human-decisions.md`: Decisões de enquadramento e metodologia humana.

O `writing-agent` e o `academic-writer` respeitam automaticamente essas diretrizes durante a redação.

---

## Suporte Multi-IDE

O tolkien opera com paridade em múltiplos ambientes de IA:

### 1. Claude Code (CLI)
Utiliza `CLAUDE.md` e espelho em `.claude/`:
```bash
/academic-orchestrator "Iniciar um novo artigo sobre [tema]"
```

### 2. OpenAI Codex CLI & IDE
Lê `AGENTS.md` e descobre skills nativamente em `.agents/skills/`. Descritores em `.codex/agents/*.toml`:
```bash
$academic-orchestrator "Iniciar um novo artigo sobre [tema]"
```

### 3. OpenCode
Lê `AGENTS.md` e descobre skills nativamente em `.agents/skills/` e agentes em `.opencode/agents/*.md`:
```bash
@academic-orchestrator "Iniciar um novo artigo sobre [tema]"
```

### 4. Google Antigravity / Gemini CLI
Descobre regras de espaço de trabalho automaticamente em `AGENTS.md` e todas as 24 skills em `.agents/skills/` via *progressive disclosure*. Executa os agentes canônicos definidos em `.agents/agents/*.md`:
```bash
/academic-orchestrator "Iniciar um novo artigo sobre [tema]"
```
Você também pode disparar diretamente qualquer agente ou skill especializada usando triggers de barra (ex.: `/research-agent`, `/writing-agent`, `/review-agent`, `/academic-prd`, `/academic-plan`, `/academic-data-validator`, `/academic-format-validator`).

---

## Exemplo: Criando um Artigo Completo do Início ao Fim

Roteiro de execução para um artigo empírico completo.

### 1. Inicie o Orquestrador

```
/academic-orchestrator "Novo artigo: benchmarking de bancos de dados vetoriais para aplicações RAG"
```

### 2. Responda a Entrevista do PRD (Gate G1)

A skill `academic-prd` conduz a entrevista inicial para definir objetivos, escopo, venue alvo e referências.
Ao finalizar, aprove `papers/paper-vector-rag/prd.md` para liberar o **Gate G1**.

### 3. Revise o Plano de Implementação (Gate G2)

O orquestrador gera `plan.md` via `academic-plan`. Aprove o plano para liberar o **Gate G2**.

### 4. Pesquisa Bibliográfica (Fase 2)

O `research-agent` executa o `academic-researcher` contra o OpenAlex e consolida:
- `papers/paper-vector-rag/research/literature.md`
- `papers/paper-vector-rag/research/references.bib`

### 5. Aprovação do Outline (Fase 3 → Gate G3)

O `writing-agent` gera `draft/outline.md` com alocação de palavras e Fichas de Escopo preliminares. Aprove para liberar o **Gate G3**.

### 6. Redação com Fichas de Escopo & CEI (Fase 4)

O `writing-agent` redige cada seção seguindo:
1. **Ficha de Escopo (Scope Card)**: Cada seção inicia com `<!-- SCOPE_CARD ... -->` delimitando o nível estrito de análise.
2. **Gatilhos de Motivação & CEI**: Todo parágrafo substantivo segue o padrão *Claim → Evidence → Interpretation* e justifica decisões de design com os 6 Gatilhos de Motivação.
3. **Mídia e Diagramas**: O `academic-media` gera ilustrações científicas em `output/figures/`.

### 7. Gates de Citações e Integridade de Dados (Fases 5 e 5.5 → Gates G4 e G4.5)

- **Gate G4 (Citação↔Bibliografia)**: O `review-agent` verifica se todas as citações do texto batem com o `.bib` (0 órfãs, 0 fantasmas) em `review/citation-report.md`.
- **Gate G4.5 (Integridade de Dados)**: O `data-validation-agent` executa o `academic-data-validator` (`data_congruence_gate.py`), validando a congruência entre números do texto e tabelas/figuras, integridade bidirecional de floats e aritmética em `review/data-congruence-report.md`.

### 8. Humanização & Auditoria de Escrita (Fase 6)

- O `academic-humanizer` realiza passadas locais por seção e uma passada transversal no rascunho completo.
- O `academic-writing-reviewer` executa auditoria determinística:
  ```bash
  python .agents/skills/academic-writing-reviewer/scripts/audit_writing.py \
    papers/paper-vector-rag/draft \
    --output papers/paper-vector-rag/review/writing-review-report.md
  ```
  Mede marcadores de IA (`AIM`), repetições (`REP`), tensões numéricas (`NUM`) e glosa de jargões (`JAR-01`).

### 9. Revisão por Pares 6-D & Loop Contínuo (Fase 7 → Gate G5)

O `review-agent` simula o painel com 5 avaliadores. A Dimensão 5 consome diretamente a auditoria de escrita.
- **Loop Contínuo de Revisão**: Se qualquer gate falhar ou a nota for < 65, o orquestrador aciona automaticamente a reescrita com o `writing-agent` e reavalia até a **Aprovação Completa**.

### 10. Output Format Gate & Geração dos Entregáveis (Fase 8)

O `format-validation-agent` roda o `academic-format-validator` (`validate_formats.py`) assegurando zero quebras em Markdown, LaTeX (.tex) ou Word (.docx).
O `paper-generator-agent` compila os arquivos finais em `output/`:
- `output/paper.tex` / `output/paper.pdf`
- `output/paper.docx`

### 11. Documentação do Processo (Fase 9)

O orquestrador registra o histórico em `process-record.md`, documentando checkpoints humanos, relatórios de gates e decisões.

---

## Solução de Problemas

### `ModuleNotFoundError` ao executar scripts Python

O ambiente virtual não está ativo. Execute:

```bash
source .venv/bin/activate
```

### O Gate de Citações falha com citações órfãs ou fantasmas

Execute o script de diagnóstico isolado:

```bash
python .agents/skills/academic-citation-manager/scripts/citation_gate.py \
  papers/paper-{slug}/draft papers/paper-{slug}/research/references.bib
```

### O Gate de Dados aponta tabelas ou figuras órfãs/pendentes

Execute o checker de floats:

```bash
python .agents/skills/academic-data-validator/scripts/check_float_integrity.py papers/paper-{slug}/draft
```

Verifique se toda tabela em `07-tables.md` e figura em `08-figure-legends.md` está referenciada no corpo do texto.

### O Output Format Gate aponta falhas

Execute o validador de formatos:

```bash
python .agents/skills/academic-format-validator/scripts/validate_formats.py papers/paper-{slug}
```

Consulte `review/format-validation-report.md` para ver o log de compilação ou de sintaxe markdown.
