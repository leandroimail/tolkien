# Tolkien — Tutorial (pt-BR)

Guia passo a passo para configurar e usar o Sistema Multi-Agente de Produção de Artigos Acadêmicos.

---

## Pré-requisitos

Antes de começar, certifique-se de que os seguintes itens estão instalados no seu sistema:

| Requisito | Versão Mínima | Observação |
|-----------|--------------|------------|
| **Python** | 3.8+ | Verifique com `python3 --version` |
| **Node.js** | 16+ | Verifique com `node --version` |
| **git** | Qualquer | Para clonar o repositório |
| **Claude Code CLI** ou **OpenCode** | Mais recente | Instale uma dessas ferramentas |
| **Homebrew** (macOS) ou **apt-get** (Linux) | — | Usado pelo script de instalação para configurar dependências do sistema |

---

## Instalação

### Passo 1 — Clone o Repositório

```bash
git clone https://gitlab.com/leandroimail/tolkien.git
cd tolkien
```

### Passo 2 — Execute o Script de Instalação de Dependências

O script instala todos os pacotes do sistema, pacotes Node.js, ferramentas de automação de navegador e o ambiente virtual Python em uma única execução.

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

O script cria um ambiente virtual Python em `.venv/` na raiz do projeto.

### Passo 3 — Ative o Ambiente Virtual

```bash
source .venv/bin/activate
```

O prompt do terminal mudará para indicar que o ambiente está ativo. Você deve ativá-lo toda vez que abrir uma nova sessão de terminal e quiser executar skills baseadas em Python manualmente.

Para desativar posteriormente:

```bash
deactivate
```

> **Nota:** Quando você invoca skills através do Claude Code ou OpenCode, as ferramentas gerenciam o ambiente automaticamente. A ativação manual só é necessária se você executar scripts Python diretamente.

---

## Templates Disponíveis

O diretório `templates/` fornece pontos de partida prontos para usar antes ou junto com o pipeline:

| Arquivo | Finalidade |
|---------|-----------|
| `templates/research_request_form.md` | Formulário estruturado que mapeia todos os campos coletados pela entrevista do `academic-prd`. Preencha-o offline antes de iniciar o pipeline para ter suas respostas prontas. Cobre: tipo de artigo, perguntas de pesquisa, venue alvo, estilo de citação, critérios de inclusão/exclusão e estrutura esperada. |
| `templates/systematic_review_protocol.yaml` | Template de protocolo alinhado com PRISMA para revisões sistemáticas da literatura. Pré-popula a estrutura requerida pelo `academic-researcher` para artigos de revisão sistemática. |

Para usar o formulário como referência durante a entrevista do PRD:

```bash
# Abra o formulário em uma janela separada antes de invocar o orquestrador
cat templates/research_request_form.md
```

---

## Usando o tolkien com Claude Code

### Iniciando um Novo Projeto de Artigo

Abra o Claude Code no diretório tolkien e invoque o orquestrador:

```
/academic-orchestrator "Iniciar um novo artigo sobre sistemas multi-agente em saúde"
```

O orquestrador irá:
1. Invocar o `academic-prd` para conduzir uma entrevista estruturada de PRD
2. Fazer ~10 perguntas para definir os requisitos do artigo
3. Pausar no **Gate G1** para sua revisão do `prd.md`
4. Após aprovação, gerar o `plan.md` e pausar no **Gate G2**
5. Continuar automaticamente por cada fase, pausando em cada gate

### Invocando Agentes Individualmente

Você pode invocar qualquer agente diretamente pela frase de ativação para executar uma fase específica:

```
# Executar apenas a fase de pesquisa bibliográfica
/research-agent "Buscar artigos sobre geração aumentada por recuperação"

# Escrever ou revisar seções
/writing-agent "Redigir a seção de metodologia"

# Executar revisão por pares
/review-agent "Revisar o artigo completo"

# Compilar o PDF final
/paper-generator "Gerar artigo final"
```

### Invocando Skills Individualmente

Para controle mais granular, use as skills diretamente:

```bash
# Gerar apenas o PRD (sem o pipeline completo)
/academic-prd

# Validar citações contra a bibliografia
/academic-citation-manager

# Compilar LaTeX manualmente
/latex

# Pesquisar artigos no OpenAlex
/academic-researcher
```

---

## Usando o tolkien com OpenCode

O fluxo de trabalho é idêntico ao Claude Code. O tolkien armazena sua configuração para OpenCode em `.agents/` (em vez de `.claude/`), que o OpenCode lê automaticamente.

### Iniciando um Novo Projeto de Artigo (OpenCode)

Abra o OpenCode no diretório tolkien:

```
@academic-orchestrator Iniciar novo artigo sobre aprendizado federado em IoT
```

Ou use os gatilhos em linguagem natural:

```
start academic pipeline for a paper about federated learning in IoT
write full article on transformer-based summarization
```

### Invocando Agentes Individualmente (OpenCode)

```
@research-agent pesquisar literatura sobre embeddings em grafos de conhecimento
@writing-agent redigir a seção de resultados
@review-agent revisar artigo completo
@paper-generator gerar artigo final
```

---

## Exemplo: Criando um Artigo Completo do Início ao Fim

Este exemplo percorre o pipeline completo para um artigo hipotético sobre benchmarking de bancos de dados vetoriais.

### 1. Inicie o Orquestrador

```
/academic-orchestrator "Novo artigo: benchmarking de bancos de dados vetoriais para aplicações RAG"
```

### 2. Responda a Entrevista do PRD (Gate G1)

A skill `academic-prd` faz perguntas estruturadas. Exemplo de respostas:

| Pergunta | Exemplo de Resposta |
|---------|---------------------|
| Tipo de artigo | Pesquisa experimental / estudo de benchmark |
| Venue alvo | SIGMOD 2026 |
| Idioma | Inglês |
| Pergunta de pesquisa | Qual banco de dados vetorial oferece o melhor equilíbrio recall-latência para cargas RAG? |
| Estilo de citação | IEEE |
| Estrutura | IMRaD |

Após completar a entrevista, revise `papers/paper-vector-rag/prd.md` e aprove para passar o Gate G1.

### 3. Revise o Plano de Implementação (Gate G2)

O orquestrador gera o `plan.md` automaticamente. Revise o plano de 9 fases e aprove para passar o Gate G2.

### 4. Pesquisa Bibliográfica (Fase 2)

O orquestrador invoca o `research-agent`, que executa o `academic-researcher` contra a API OpenAlex usando as palavras-chave do seu PRD. O resultado é salvo em:

```
papers/paper-vector-rag/research/literature.md
papers/paper-vector-rag/research/references.bib
```

### 5. Aprovação da Estrutura (Fase 3 → Gate G3)

A skill `academic-writer` (modo outline) gera `draft/outline.md` com cabeçalhos de seções e alocações de palavras. Revise e aprove para passar o Gate G3.

### 6. Redação Completa (Fase 4)

O `writing-agent` redige cada seção sequencialmente. Figuras e gráficos são gerados pelo `academic-media` e salvos em `output/figures/`. Esta é a fase mais longa.

### 7. Validação de Citações (Fase 5 → Gate G4)

O `review-agent` executa `academic-citation-manager` e `academic-bibliography-manager`. Essas ferramentas verificam que:
- Cada `\cite{key}` no rascunho tem uma entrada correspondente em `references.bib`
- Cada entrada em `references.bib` é citada pelo menos uma vez
- Cada entrada BibTeX possui todos os campos obrigatórios

Um relatório de violações é escrito em `review/citation-report.md`. Corrija quaisquer violações antes que o Gate G4 seja liberado.

### 8. Humanização (Fase 6)

O `academic-humanizer` ajusta o registro do rascunho — removendo marcadores típicos de escrita gerada por IA enquanto preserva o rigor acadêmico e o vocabulário específico da área.

### 9. Revisão por Pares (Fase 7 → Gate G5)

O `academic-reviewer` simula um painel de 5 revisores. O relatório de revisão é salvo em `review/review-report.md`. A pontuação composta deve ser ≥ 65/100 sem nenhuma questão CRÍTICA para passar o Gate G5. Se a pontuação estiver abaixo do limite, o orquestrador retorna à fase de redação para revisões.

### 10. Geração do Output (Fase 8 → Gate G5.5)

O `paper-generator-agent` compila o documento LaTeX e exporta PDF e DOCX. Todos os arquivos são salvos em `output/`:

```
papers/paper-vector-rag/output/paper.tex
papers/paper-vector-rag/output/paper.pdf
papers/paper-vector-rag/output/paper.docx
```

O Gate G5.5 verifica que o `pdflatex` termina com código 0 e todas as referências são resolvidas.

### 11. Documentação do Processo (Fase 9)

O orquestrador escreve o `process-record.md` — um registro de cada decisão, resultado de gate e revisão durante a execução do pipeline.

---

## Solução de Problemas

### `pdflatex: command not found`

O TinyTeX não foi instalado ou seu diretório bin não está no `PATH`. Re-execute o script de instalação:

```bash
bash resources/install_skills_deps.sh
```

Ou adicione o TinyTeX manualmente ao seu perfil do shell:

```bash
# macOS (Apple Silicon)
export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"

# macOS (Intel)
export PATH="$HOME/.TinyTeX/bin/x86_64-darwin:$PATH"

# Linux (x86_64)
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
```

### `ModuleNotFoundError` ao executar uma skill Python

O ambiente virtual não está ativo. Execute:

```bash
source .venv/bin/activate
```

Se o diretório `.venv/` não existir, re-execute:

```bash
bash resources/install_skills_deps.sh
```

### `academic-researcher` não retorna resultados

A API OpenAlex é uma API pública com limites de taxa. Se você receber resultados vazios:
- Aguarde alguns segundos e tente novamente
- Restrinja as palavras-chave de busca no `prd.md`
- O OpenAlex não exige chave de API, mas é recomendado incluir um cabeçalho de e-mail educado para uso em alto volume

### Gate não está sendo liberado apesar de corrigir as violações

Invoque novamente o agente relevante explicitamente para re-executar a validação:

```
/review-agent "execute academic review"
```

O orquestrador verifica o estado do gate com base no arquivo de relatório mais recente, não em um cache.

### Compilação LaTeX falha com referências indefinidas

Certifique-se de que `references.bib` está no local correto (`research/references.bib`) e que o template LaTeX inclui `\bibliography{../research/references}`. A skill `latex` pode diagnosticar a maioria dos erros de compilação automaticamente.

### Skills não são reconhecidas no OpenCode

Confirme que os diretórios `.agents/skills/` e `.agents/agents/` existem e contêm as definições das skills. Use a skill `multi-ide-artifacts` para re-sincronizar se necessário:

```
/multi-ide-artifacts sync claude-to-opencode
```
