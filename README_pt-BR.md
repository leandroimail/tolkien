# tolkien

**Sistema Multi-Agente de Produção de Artigos Acadêmicos** — um framework para produzir artigos científicos completos e prontos para publicação, desde o primeiro prompt até o PDF final, utilizando agentes e skills especializados dentro do Google Antigravity, Claude Code, OpenCode e OpenAI Codex.

![Compatível com Google Antigravity](https://img.shields.io/badge/Google%20Antigravity-compatível-purple)
![Compatível com Claude Code](https://img.shields.io/badge/Claude%20Code-compatível-blue)
![Compatível com OpenCode](https://img.shields.io/badge/OpenCode-compatível-green)
![Compatível com OpenAI Codex](https://img.shields.io/badge/OpenAI%20Codex-compatível-orange)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-yellow)
![Plataforma macOS | Linux](https://img.shields.io/badge/Plataforma-macOS%20%7C%20Linux-lightgrey)

---

## Licença

Este projeto está licenciado sob a **GNU General Public License v2.0 (GPL-2.0)**.

Para o texto completo da licença, consulte o arquivo [LICENSE](LICENSE).

---

## Funcionalidades

- **Pipeline sequencial de 10 fases** com 7 gates de qualidade (G1–G5, G4.5 Gate de Integridade de Dados e Gate de Formato de Saída) — desde a pergunta de pesquisa até o PDF compilado
- **8 agentes especializados**: orquestrador, pesquisa, escrita, revisão, integridade de dados, validação de formato, gerador de artigo e busca web
- **24 skills atômicas**: busca bibliográfica (OpenAlex), compilação LaTeX, revisão por pares em 6 dimensões, humanização, validação de citações, congruência de dados e mais
- **Compatibilidade multi-IDE / multi-harness** — suporte nativo para Google Antigravity (`.agents/`, `AGENTS.md`), Claude Code (`.claude/`), OpenCode (`.opencode/`) e OpenAI Codex (`.codex/`) com formatos otimizados para cada ambiente
- **Desenvolvimento guiado por especificação (Academic SDD)** — todo artigo começa com um PRD validado e um plano de implementação

---

## Início Rápido

```bash
# 1. Clone o repositório
git clone https://gitlab.com/leandroimail/tolkien.git
cd tolkien

# 2. Instale todas as dependências (sistema, Node.js, Python)
bash resources/install_skills_deps.sh

# 3. Ative o ambiente virtual Python
source .venv/bin/activate

# 4. Inicie um novo projeto de artigo (Antigravity, Claude Code, OpenCode ou Codex)
/academic-orchestrator "Iniciar um novo artigo sobre arquiteturas transformer"
```

O orquestrador vai guiá-lo por uma entrevista estruturada de PRD e, em seguida, executar o pipeline completo automaticamente, pausando em cada checkpoint obrigatório para sua revisão.

---

## Documentação

| Documento | Descrição |
|-----------|-----------|
| [Central de Documentação](docs/pt-BR/README.md) | Mapa de navegação central, estrutura Diataxis e índice de documentos |
| [Arquitetura](docs/pt-BR/ARCHITECTURE.md) | Diagrama do sistema, modelo em 3 camadas, pipeline de 10 fases, critérios dos gates, fluxo de dados |
| [Definições](docs/pt-BR/DEFINITIONS.md) | Glossário, inventário de agentes, catálogo de skills, especificação de diretórios |
| [Tutorial](docs/pt-BR/TUTORIAL.md) | Guia passo a passo: instalação, uso com Antigravity, uso com Claude Code, uso com OpenCode, exemplo completo, solução de problemas |
| [Início Rápido](docs/pt-BR/QUICKSTART.md) | Guia rápido em 5 minutos com comandos prontos para copiar |
| [PRD do Sistema](docs/pt-BR/PRD-academic-multiagent-system.md) | Especificação técnica completa do próprio sistema tolkien |
| [Arquitetura Técnica](docs/pt-BR/tecnica/arquitetura.md) | Imersão técnica na arquitetura interna, fluxo de dados e invariantes |
| [Tutorial do Zero](docs/pt-BR/tutoriais/produzindo-artigo-do-zero.md) | Passo a passo prático de ponta a ponta para produção de um artigo científico |

---

## Compatibilidade

O tolkien é compatível com quatro IDEs e harnesses de IA, cada um com seu diretório de configuração nativo:

| Diretório | Ferramenta / Harness | Formato dos Agentes | Formato das Skills |
|-----------|----------------------|---------------------|-------------------|
| `.agents/` | [Google Antigravity](https://antigravity.google) | Markdown (`.md`) | `SKILL.md` (Agent Skills) |
| `.claude/` | [Claude Code](https://claude.ai/code) | Markdown (`.md`) | `SKILL.md` |
| `.agents/` | [OpenCode](https://opencode.ai) & [OpenAI Codex](https://openai.com/codex) | Markdown (`.md`) | `SKILL.md` |
| `.codex/` | [OpenAI Codex](https://openai.com/codex) | TOML (`.toml`) | `SKILL.md` |
| `.opencode/` | [OpenCode](https://opencode.ai) | Markdown com frontmatter (`.md`) | `SKILL.md` |

### Como funciona

- **Skills**: Todos os ambientes compartilham as mesmas skills em `.agents/skills/` (padrão Agent Skills open standard). Não é necessária nenhuma conversão.
- **Agentes (Google Antigravity)**: Descobre regras automaticamente em `AGENTS.md` e carrega skills de `.agents/skills/` via *progressive disclosure*. Executa agentes canônicos a partir de `.agents/agents/`.
- **Agentes (Claude Code)**: Lidos de `.claude/agents/` — formato Markdown com YAML frontmatter.
- **Agentes (OpenCode)**: Lidos de `.opencode/agents/` — formato Markdown com YAML frontmatter (frontmatter: `description`, `mode`, `permission`).
- **Agentes (Codex)**: Lidos de `.codex/agents/` — formato TOML com campos obrigatórios `name`, `description` e `developer_instructions`. O campo `model` é opcional e herda da sessão pai.

### Agentes disponíveis

| Agente | Função | Triggers Principais |
|--------|--------|---------------------|
| `academic-orchestrator` | Coordenador mestre do pipeline de 10 fases e gates | `/academic-orchestrator`, `"start academic pipeline"` |
| `research-agent` | Pesquisa bibliográfica sistemática + validação | `/research-agent`, `"search literature"` |
| `writing-agent` | Redação integral, geração de mídia e humanização | `/writing-agent`, `"write section"`, `"draft article"` |
| `review-agent` | Validação de citações + painel de revisão por pares 6-D | `/review-agent`, `"review article"`, `"peer review"` |
| `data-validation-agent` | Congruência numérica texto ↔ dados (Gate G4.5) | `/data-validation-agent`, `"validate data congruence"` |
| `format-validation-agent` | Validação multi-formato contínua (Gate de Formato de Saída) | `/format-validation-agent`, `"validate formatting"` |
| `paper-generator-agent` | Geração LaTeX/PDF/DOCX e exportação final | `/paper-generator`, `"generate final paper"` |
| `web-browser-search-agent` | Busca web e automação de navegador | `/web-browser-search`, `"search the web"` |

---

## Estrutura de Projetos

### Diretório do Sistema

```
tolkien/
├── .agents/                    ← Raiz canônica (Antigravity, Codex, OpenCode)
│   ├── agents/                 ← Descritores canônicos de agentes (.md)
│   └── skills/                 ← 24 skills atômicas (SKILL.md, scripts)
├── .claude/                    ← Espelho de configuração do Claude Code
│   ├── agents/                 ← Subagentes Claude (.md)
│   ├── skills/                 ← Espelho de skills Claude
│   └── settings.json           ← Hooks do Claude Code
├── .codex/                     ← Configuração do OpenAI Codex
│   ├── agents/                 ← Descritores de subagentes Codex (.toml)
│   └── hooks.json              ← Hooks de ciclo de vida Codex
├── .opencode/                  ← Configuração do OpenCode
│   ├── agents/                 ← Descritores de subagentes OpenCode (.md)
│   └── plugins/                ← Plugins de validação OpenCode
├── resources/                  ← Scripts de instalação e dependências
│   ├── install_skills_deps.sh  ← Script principal de instalação
│   └── requirements_skills.txt ← Lista de pacotes Python
├── templates/                  ← Templates prontos para uso
│   ├── research_request_form.md ← Formulário para entrevista do PRD
│   └── systematic_review_protocol.yaml ← Protocolo PRISMA
├── .venv/                      ← Ambiente virtual Python
├── docs/                       ← Documentação do sistema
├── papers/                     ← Projetos de artigos
├── projects/                   ← Diretório raiz alternativo
├── AGENTS.md                   ← Regras canônicas e documentação do sistema
└── CLAUDE.md                   ← Instruções raiz para Claude Code
```

### Estrutura de Projetos de Artigos

Todos os projetos de artigos devem ser criados em um dos diretórios raiz válidos:

```text
projects/   papers/   .projects/   .papers/
```

Cada projeto segue uma estrutura padrão:

```text
papers/paper-{slug}/
├── prd.md                 # Requisitos do artigo
├── plan.md                # Roteiro de execução
├── research/              # Literatura + references.bib
├── draft/                 # Seções do artigo em Markdown
├── review/                # Relatórios de revisão + histórico de revisões
├── output/                # Entregáveis finais (PDF, LaTeX, DOCX)
└── process-record.md      # Histórico de colaboração humano-IA
```

---

## Visão Geral do Pipeline

```mermaid
flowchart LR
    p0["Fase 0\nGeração do PRD"] -->|G1| p1["Fase 1\nPlano de Implementação"]
    p1 -->|G2| p2["Fase 2\nPesquisa Bibliográfica"]
    p2 --> p3["Fase 3\nEstrutura (Outline)"]
    p3 -->|G3| p4["Fase 4\nRedação Completa"]
    p4 --> p5["Fase 5\nValidação de Citações"]
    p5 -->|G4| p6["Fase 6\nHumanização"]
    p6 --> p7["Fase 7\nRevisão por Pares"]
    p7 -->|G5| p8["Fase 8\nGeração do Output"]
    p8 -->|G5.5| p9["Fase 9\nDocumentação do Processo"]
```

Consulte [docs/pt-BR/ARCHITECTURE.md](docs/pt-BR/ARCHITECTURE.md) para o diagrama completo do pipeline com critérios dos gates.

---

## Pré-requisitos

- macOS ou Linux
- Python 3.8+
- Node.js 16+
- [Google Antigravity](https://antigravity.google), [Claude Code CLI](https://claude.ai/code), [OpenCode](https://opencode.ai) ou [OpenAI Codex](https://openai.com/codex)
- Homebrew (macOS) ou apt-get (Linux) para dependências do sistema

Execute `bash resources/install_skills_deps.sh` para instalar todas as dependências restantes automaticamente.
