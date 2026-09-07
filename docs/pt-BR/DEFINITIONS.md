# Tolkien — Definições e Referência

> **Idioma / Language:** Português | [English Version](../DEFINITIONS.md)

Glossário completo, inventário de agentes, catálogo de skills e especificação de diretórios para o Sistema Multi-Agente de Produção de Artigos Acadêmicos.

---

## Glossário

| Termo | Definição |
|-------|-----------|
| **Academic SDD** | *Spec-Driven Development* adaptado para a escrita científica. Impõe sequenciamento estrito: PRD → Plano → Execução. Nenhuma fase pode iniciar antes que a anterior seja formalmente validada. |
| **Agente** | Um coordenador de alto nível que orquestra múltiplas skills para alcançar um objetivo complexo de múltiplos passos (ex.: conduzir o pipeline completo de pesquisa bibliográfica). Os agentes podem ser acionados por triggers no Google Antigravity, Claude Code, OpenCode ou Codex. |
| **Skill** | Uma capacidade atômica e especializada que executa uma tarefa específica (ex.: buscar na OpenAlex, compilar LaTeX, verificar marcadores de IA). Skills são acionadas via comandos `/skill-name`. |
| **Gate** | Um ponto de controle obrigatório que bloqueia o avanço do pipeline até que critérios de qualidade sejam plenamente atendidos. Gates: G1, G2, G3, G4 (Citação↔Bibliografia), **G4.5 (Integridade de Dados)**, G5 (Revisão 6-D) e o **Output Format Gate** (md/tex/docx). |
| **PRD** | *Product Requirements Document* — neste contexto, a especificação formal do artigo acadêmico. Define questões de pesquisa, periódicos-alvo, estilo de citação, idioma e restrições metodológicas. Armazenado como `prd.md`. |
| **prd.md** | O arquivo de requisitos do artigo gerado pela skill `academic-prd`. É a fonte única de verdade para todas as decisões do pipeline. |
| **plan.md** | O roteiro de implementação gerado pela skill `academic-plan` a partir do `prd.md`. Lista todas as fases com tarefas, entregáveis e critérios de aceitação. |
| **references.bib** | O arquivo de bibliografia BibTeX. Gerenciado pelo `academic-bibliography-manager`. Utilizado como fonte exclusiva de citações pelo `academic-citation-manager`. |
| **Scope Card (Ficha de Escopo)** | Comentário de metadados obrigatório (`<!-- SCOPE_CARD ... -->`) posicionado no topo de cada seção do rascunho, definindo Nível de Análise estrito, Questão Primária, Limites Fora de Escopo e Âncora Teórica. Evita confusão de níveis e desvio de escopo (*scope drift*). |
| **Arquitetura CEI** | Disciplina estrutural *Claim → Evidence → Interpretation* para parágrafos acadêmicos substantivos, assegurando que afirmações sejam imediatamente suportadas por evidências empíricas e interpretadas com mecanismos causais. |
| **6 Gatilhos de Motivação** | Pontos de inflexão obrigatórios onde o texto deve justificar causalmente o "porquê": (1) Decisão de Design Arquitetural, (2) Resultado Contraintuitivo, (3) Trade-off Técnico/Econômico, (4) Divergência com a Literatura, (5) Invocação de Limite de Escopo, (6) Empréstimo Conceitual/Metáfora. |
| **Loop de Revisão Contínua** | Ciclo de retroalimentação automatizado entre as Fases 5 e 7 (*escrever → validar (G4, G4.5) → revisão 6-D (G5) → reescrever/corrigir → reavaliar*), repetindo até a Aprovação Completa. |
| **Auditoria de Escrita** | Auditoria determinística prévia à banca executada pelo `academic-writing-reviewer`, verificando marcadores de IA (`AIM`), repetições/ecos (`REP`), tensões numéricas (`NUM`) e jargões computacionais sem glosa (`JAR-01`). Alimenta a Dimensão 5 da revisão 6-D. |
| **IMRaD** | Introdução, Metodologia, Resultados e Discussão (*Introduction, Methods, Results, and Discussion*) — estrutura padrão para artigos científicos empíricos. |
| **Revisão 6-D** | Revisão por pares em seis dimensões executada pelo `academic-reviewer` (escala de 0 a 100): (1) Rigor Científico e Metodologia (25%), (2) Integridade de Dados e Resultados (20%), (3) Originalidade e Contribuição (15%), (4) Coerência de Argumentação e Evidências (15%), (5) Qualidade da Escrita (15%), (6) Conformidade de Formatação e Bibliografia (10%). Simulada por uma banca com 5 papéis: Editor-Chefe + R1 Metodologia + R2 Domínio + R3 Perspectiva + Advogado do Diabo. |
| **Gate de Integridade de Dados (G4.5)** | O gate determinístico operado pelo `academic-data-validator`/`data-validation-agent` que valida a congruência do texto com os dados apresentados: números na prosa vs tabelas/figuras, consistência numérica interna (Ns, totais, porcentagens) e integridade bidirecional de tabelas/figuras. Alimenta a Dimensão 2. |
| **Output Format Gate** | O gate contínuo operado pelo `academic-format-validator`/`format-validation-agent` validando a formatação em Markdown, LaTeX (.tex) e Word (.docx). Reutiliza os validadores de `latex` e `docx`. Alimenta a Dimensão 6. Executado via hooks em todos os ambientes. |
| **process-record.md** | O diário de colaboração humano-IA gerado na Fase 9. Documenta decisões tomadas, resultados de gates e alterações realizadas durante a execução. |
| **OpenAlex** | Base de dados acadêmica aberta e gratuita utilizada pelo `academic-researcher` e `academic-bibliography-manager` para minerar literatura e enriquecer metadados BibTeX. Não requer chave de API. |
| **Gate Citação↔Bibliografia (G4)** | A validação do Gate G4 que assegura: (1) toda citação no texto possui entrada correspondente em `references.bib`; (2) toda entrada em `references.bib` é citada no rascunho; (3) todas as entradas `.bib` possuem os campos obrigatórios. |
| **Slug** | Um identificador curto e seguro para URL de um projeto de artigo (ex.: `vector-retrieval`). Usado como nome do diretório: `paper-{slug}/`. |
| **TinyTeX** | Distribuição LaTeX leve instalada pelo script `install_skills_deps.sh` caso não haja TeX no sistema. Fornece `pdflatex`, `bibtex` e `tlmgr`. |
| **.venv** | Ambiente virtual Python local criado na raiz do repositório por `install_skills_deps.sh`. Deve estar ativo para executar qualquer skill baseada em Python. |

---

## Agentes

O tolkien inclui 8 agentes especializados. As definições canônicas residem em `.agents/agents/` (Markdown), com espelhos correspondentes em `.claude/agents/` (Claude Code), `.codex/agents/` (OpenAI Codex TOML) e `.opencode/agents/` (OpenCode Markdown).

### academic-orchestrator

| Propriedade | Valor |
|-------------|-------|
| **Objetivo** | Coordenador Mestre. Executa o pipeline de 10 fases, gerencia checkpoints, aplica gates e conduz o Loop de Revisão Contínua. |
| **Triggers** | `/academic-orchestrator`, `"start academic pipeline"`, `"write full article"`, `"academic pipeline"`, `/status` |
| **Aciona** | Todos os agentes e skills do pipeline, em ordem |
| **Arquivo** | `.agents/agents/academic-orchestrator.md` / `.claude/agents/academic-orchestrator.md` |

### research-agent

| Propriedade | Valor |
|-------------|-------|
| **Objetivo** | Levantamento bibliográfico sistemático, triagem de fontes e síntese de referências. |
| **Triggers** | `/research-agent`, `"research for paper"`, `"search literature and validate bib"` |
| **Aciona** | `academic-researcher`, `academic-bibliography-manager`, `web-browser-search-agent` |
| **Arquivo** | `.agents/agents/research-agent.md` / `.claude/agents/research-agent.md` |

### writing-agent

| Propriedade | Valor |
|-------------|-------|
| **Objetivo** | Redação integral de seções (com Scope Cards e CEI), geração de mídia científica, humanização de registro e auditoria prévia de escrita. |
| **Triggers** | `/writing-agent`, `"draft full article"`, `"write and humanize"`, `"write section"` |
| **Aciona** | `academic-writer`, `academic-media`, `academic-humanizer`, `academic-writing-reviewer` |
| **Arquivo** | `.agents/agents/writing-agent.md` / `.claude/agents/writing-agent.md` |

### review-agent

| Propriedade | Valor |
|-------------|-------|
| **Objetivo** | Validação Citação↔Bibliografia (G4), Gate de Integridade de Dados (G4.5), auditoria de prosa e painel de revisão por pares 6-D. |
| **Triggers** | `/review-agent`, `"review full article"`, `"execute academic review"`, `"verify citations"` |
| **Aciona** | `academic-citation-manager`, `academic-bibliography-manager`, `academic-data-validator`, `academic-writing-reviewer`, `academic-reviewer`, `web-browser-search-agent` |
| **Arquivo** | `.agents/agents/review-agent.md` / `.claude/agents/review-agent.md` |

### data-validation-agent

| Propriedade | Valor |
|-------------|-------|
| **Objetivo** | Gate de Integridade de Dados determinístico (G4.5): valida congruência numérica entre texto e tabelas/figuras, integridade de floats e aritmética. |
| **Triggers** | `/data-validation-agent`, `"validate data congruence"`, `"check data integrity"` |
| **Aciona** | `academic-data-validator`, `academic-media` |
| **Arquivo** | `.agents/agents/data-validation-agent.md` / `.claude/agents/data-validation-agent.md` |

### format-validation-agent

| Propriedade | Valor |
|-------------|-------|
| **Objetivo** | Output Format Gate contínuo: valida formatação estrutural em Markdown, LaTeX (.tex) e Word (.docx). |
| **Triggers** | `/format-validation-agent`, `"validate formatting"`, `"check format"`, `"validate docx"` |
| **Aciona** | `academic-format-validator`, `latex`, `docx` |
| **Arquivo** | `.agents/agents/format-validation-agent.md` / `.claude/agents/format-validation-agent.md` |

### paper-generator-agent

| Propriedade | Valor |
|-------------|-------|
| **Objetivo** | Converte o rascunho revisado no documento final PDF ou DOCX usando LaTeX ou Word. |
| **Triggers** | `/paper-generator`, `"generate final paper"`, `"compile LaTeX"`, `"generate paper PDF"`, `"export paper"` |
| **Aciona** | `latex`, `latex-template-converter`, `pdf`, `docx`, `academic-format-validator` |
| **Arquivo** | `.agents/agents/paper-generator-agent.md` / `.claude/agents/paper-generator-agent.md` |

### web-browser-search-agent

| Propriedade | Valor |
|-------------|-------|
| **Objetivo** | Busca na web e automação de navegador para literatura cinzenta, recuperação de textos integrais, resolução de DOIs e checagem de retratações. |
| **Triggers** | Invocado internamente por `research-agent` e `review-agent`; também: `/web-browser-search`, `"search the web"`, `"browse URL"`, `"validate DOI online"` |
| **Aciona** | `web-browser-search`, `duckducksearch`, `agent-browser`, `playwright-cli` |
| **Arquivo** | `.agents/agents/web-browser-search-agent.md` / `.claude/agents/web-browser-search-agent.md` |

---

## Inventário de Skills

O tolkien inclui **24 skills** (12 skills de pipeline + 12 skills de ferramenta). Todas as definições canônicas residem em `.agents/skills/` e são espelhadas em `.claude/skills/`.

### Skills de Pipeline (12)

| Skill | Trigger | Função | Fase do Pipeline |
|-------|---------|--------|------------------|
| `academic-prd` | `/academic-prd` | Entrevista estruturada para gerar `prd.md` | Fase 0 |
| `academic-plan` | `/academic-plan` | Gera o plano operacional `plan.md` a partir de um PRD aprovado | Fase 1 |
| `academic-researcher` | `/academic-researcher` | Busca sistemática via API OpenAlex; produz `literature.md` e `references.bib` | Fase 2 |
| `academic-writer` | `/academic-writer`, `"write section"` | Redige seções no formato IMRaD ou temático com Scope Cards e arquitetura CEI | Fases 3–4 |
| `academic-citation-manager` | `/academic-citation-manager`, `"verify citations"` | Valida citações no texto contra `references.bib` (Gate G4) | Fase 5 |
| `academic-bibliography-manager` | `/academic-bibliography-manager`, `"validate bibliography"` | Valida, deduplica e enriquece `references.bib` via OpenAlex | Fase 5 |
| `academic-data-validator` | `/academic-data-validator`, `"validate data congruence"` | Gate de Integridade de Dados (G4.5): valida congruência texto ↔ tabelas/figuras, integridade de floats e aritmética | Fase 5.5 |
| `academic-format-validator` | `/academic-format-validator`, `"validate formatting"` | Output Format Gate: valida integridade de Markdown, LaTeX e Word (.docx) | Fase 8 |
| `academic-writing-reviewer` | `/academic-writing-reviewer`, `"audit writing"` | Auditoria estática de escrita: marcadores de IA (`AIM`), repetições (`REP`), tensões numéricas (`NUM`) e jargões (`JAR`); alimenta Dimensão 5 | Fases 6–7 |
| `academic-reviewer` | `/academic-reviewer`, `"review article"` | Simula revisão por pares 6-D com painel de 5 papéis: Editor-Chefe + 3 avaliadores + Advogado do Diabo | Fase 7 |
| `academic-humanizer` | `/academic-humanizer`, `"humanize"` | Ajusta registro e remove marcas de IA em passadas local e global. Suporta EN e PT-BR. | Fase 6 |
| `academic-media` | `/academic-media`, `"create figure"` | Gera figuras, esquemas conceituais e gráficos de análise exploratória (EDA) | Fases 4, 8 |

### Skills de Ferramenta (12)

| Skill | Trigger | Função |
|-------|---------|--------|
| `latex` | `/latex` | Compilação em LaTeX, formatação e depuração de erros |
| `latex-template-converter` | `/latex-template-converter` | Adapta documentos para templates de periódicos e conferências (ACM, IEEE, SBC, Springer) |
| `pdf` | `/pdf` | Extração de texto/tabelas de PDF, fusão, divisão e geração |
| `docx` | `/docx` | Criação, edição e formatação de documentos Word (.docx) |
| `xlsx` | `/xlsx` | Leitura, edição e processamento de fórmulas em planilhas |
| `agent-browser` | `/agent-browser` | Automação de navegador: preenchimento de formulários, cliques, screenshots e raspagem |
| `playwright-cli` | `/playwright-cli` | Automação e testes de páginas via Playwright CLI |
| `web-search` | `/web-search` | Busca web com resultados classificados e snippets |
| `web-browser-search` | `/web-browser-search` | Busca unificada (DuckDuckGo/Brave) com navegação em páginas |
| `duckducksearch` | `/duckducksearch` | Busca DuckDuckGo com filtros de mídia e notícias |
| `creating-skills` | `/creating-skills` | Framework para criar, validar e publicar novas skills |
| `multi-ide-artifacts` | `/multi-ide-artifacts` | Converte e sincroniza artefatos entre Claude Code, OpenCode, Codex e Antigravity |

---

## Estrutura de Diretórios de Projetos de Artigos

Cada projeto de artigo deve seguir rigorosamente a estrutura abaixo. O diretório `output/` armazena todos os entregáveis finais:

```text
{root}/paper-{slug}/
├── prd.md                     # Requisitos do artigo (gerado pelo academic-prd)
├── plan.md                    # Plano de implementação (gerado pelo academic-plan)
├── process-record.md          # Registro de colaboração humano-IA (gerado na Fase 9)
│
├── resources/                 # (OPCIONAL) Governança do artigo e arquivos base
│   ├── style-guide.md         # Voz do autor, tom e regras CEI específicas
│   ├── anti-style-guide.md    # Clichês banidos, marcadores de IA e vícios
│   └── human-decisions.md     # Decisões metodológicas do pesquisador
│
├── research/
│   ├── literature.md          # Síntese das obras e literatura analisada
│   ├── search-strategy.md     # Metodologia documentada de busca (bases, strings)
│   └── references.bib         # Arquivo BibTeX — fonte única de verdade para citações
│
├── draft/
│   ├── outline.md             # Estrutura aprovada com orçamento de palavras
│   ├── 00-abstract.md         # Seções em rascunho com Scope Cards e parágrafos CEI
│   ├── 01-introduction.md
│   ├── 02-theory.md
│   ├── 03-methodology.md
│   ├── 04-findings.md
│   ├── 05-discussion.md
│   ├── 06-conclusion.md
│   ├── 07-tables.md
│   └── 08-figure-legends.md
│
├── review/
│   ├── citation-report.md     # Gate G4: Relatório de validação Citação↔Bibliografia
│   ├── data-congruence-report.md # Gate G4.5: Relatório de integridade e congruência de dados
│   ├── writing-review-report.md  # Auditoria de escrita (AIM, REP, NUM, JAR)
│   ├── review-report.md       # Resultados da revisão 6-D, notas e Roadmap de revisão
│   ├── format-validation-report.md # Relatório do Output Format Gate
│   └── revision-log.md        # Histórico de revisões com justificativas
│
└── output/                    # TODOS os entregáveis finais residem aqui
    ├── paper.tex
    ├── paper.pdf
    ├── paper.docx
    └── figures/
```

**Diretórios raiz permitidos:**
```
projects/      papers/      .projects/      .papers/
```

Exemplo de caminho absoluto: `/caminho/para/tolkien/papers/paper-vector-retrieval/`

---

## Diretórios de Configuração Multi-IDE

O tolkien está configurado nos seguintes diretórios para garantir interoperabilidade total:

| Diretório | Plataforma / IDE Alvo | Conteúdo |
|-----------|-----------------------|----------|
| `.agents/` | Google Antigravity, OpenAI Codex, OpenCode | Raiz canônica: `agents/` (.md) e `skills/` (.md, scripts, referências) |
| `.claude/` | Claude Code (CLI) | Espelho: `agents/` (.md), `skills/` e hooks em `settings.json` |
| `.codex/` | OpenAI Codex | Descritores `agents/*.toml` e hooks em `hooks.json` |
| `.opencode/` | OpenCode | Descritores `agents/*.md` e plugin `plugins/format-validator.js` |
| Raiz | Todas as plataformas | `AGENTS.md` (regras canônicas) e `CLAUDE.md` |

### Ambiente Virtual Python

O diretório `.venv/` na raiz do repositório é o ambiente Python compartilhado para todas as skills. Ele deve ser ativado antes de executar skills baseadas em scripts Python:

```bash
# Ativar
source .venv/bin/activate

# Desativar
deactivate
```
