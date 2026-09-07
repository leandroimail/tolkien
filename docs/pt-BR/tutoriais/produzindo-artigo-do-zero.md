# Tutorial: Produzindo um Artigo Científico do Zero com tolkien

Este tutorial ensina o caminho completo de ponta a ponta para conceber, pesquisar, estruturar, redigir, validar e exportar um artigo científico com o **tolkien**, avançando com segurança através dos 7 gates de qualidade até a aprovação final.

> **Idioma / Language:** Português | [English Version](../../tutorials/producing-article-from-scratch.md)

---

## 1. Objetivo do Aprendizado

Ao final desta lição, você terá produzido um artigo científico completo e auditado:
- Requisitos e questões de pesquisa formalizados em `prd.md` (Gate G1).
- Cronograma e checklist operacional em `plan.md` (Gate G2).
- Base bibliográfica pesquisada e deduplicada em `references.bib`.
- Estrutura modular aprovada com Fichas de Escopo (*Scope Cards*) em `outline.md` (Gate G3).
- Texto substantivo com arquitetura CEI e zero citações órfãs (Gate G4).
- Congruência matemática de 100% entre a prosa e as tabelas/figuras (Gate G4.5).
- Parecer simulado de banca de periódicos com nota $\ge 7.0/10$ e zero pendências críticas (Gate G5).
- Manuscrito exportado em Word (.docx) ou LaTeX (.pdf) aprovado no `Output Format Gate`.

---

## 2. Pré-requisitos

Antes de iniciar, certifique-se de que seu ambiente atende aos seguintes requisitos:

1. **Python 3.10 ou superior:**
   ```bash
   python3 --version
   ```
2. **Dependências do tolkien instaladas no ambiente virtual:**
   Execute o script de bootstrap na raiz do repositório:
   ```bash
   bash resources/install_skills_deps.sh
   source .venv/bin/activate
   ```
3. **Ambiente de IA configurado:**
   O tolkien funciona nativamente no harness de sua preferência:
   - **Claude Code CLI** (com `.claude/`)
   - **OpenAI Codex** (com `.codex/`)
   - **OpenCode** (com `.opencode/`)
   - **Google Antigravity** (com `.agents/`)

---

## 3. Lição Passo a Passo

### Passo 1: Inicializar o Projeto do Artigo

Defina um identificador único (*slug*) para o seu artigo (por exemplo, `paper-redes-neurais`). Crie a pasta oficial sob `papers/`:

```bash
mkdir -p papers/paper-redes-neurais/{research,draft,review,output,resources}
```

> **Checkpoint:** Verifique se as pastas existem executando:
> ```bash
> ls -d papers/paper-redes-neurais/*/
> ```
> O terminal deve listar: `draft/`, `output/`, `research/`, `resources/`, `review/`.

---

### Passo 2: Entrevista de Requisitos — Academic PRD (Fase 0)

Inicie o processo acionando o orquestrador ou a skill de requisitos:
> `/academic-prd "Configurar novo artigo sobre robustez adversarial em redes neurais"`

Responda à entrevista interativa fornecendo:
- Pergunta de pesquisa central.
- Periódico ou conferência alvo (ex.: IEEE Transactions, Elsevier, Springer).
- Tipo de artigo (empírico, revisão sistemática ou teórico).
- Dados ou código disponíveis.

O agente sintetizará os requisitos em `papers/paper-redes-neurais/prd.md`.

> **Checkpoint (Gate G1):** Abra `papers/paper-redes-neurais/prd.md`, examine o escopo e confirme explicitamente digitando:
> `"Aprovo o PRD"` ou `"Gate G1 aprovado"`.

---

### Passo 3: Geração do Plano de Execução (Fase 1)

Com o PRD validado, solicite a criação do roteiro operacional de tarefas:
> `/academic-plan`

O agente lerá o `prd.md` e produzirá `papers/paper-redes-neurais/plan.md`, detalhando cada seção a redigir, tarefas parciais e critérios de aceitação.

> **Checkpoint (Gate G2):** Revise a sequência de tarefas em `plan.md`. Confirme digitando:
> `"Plano de execução aprovado"`.

---

### Passo 4: Pesquisa Bibliográfica e Curadoria (Fase 2)

Acione o agente de pesquisa para minerar a literatura acadêmica relevante:
> `/research-agent "Pesquisar literatura sobre adversarial training e robustez certificada"`

O agente consulta a API da OpenAlex, resolve os DOIs e gera dois artefatos:
1. `papers/paper-redes-neurais/research/literature_review.md` (síntese analítica das obras).
2. `papers/paper-redes-neurais/research/references.bib` (arquivo BibTeX limpo e enriquecido).

> **Checkpoint:** Valide o arquivo `.bib` executando:
> ```bash
> head -n 25 papers/paper-redes-neurais/research/references.bib
> ```
> Confirme que as entradas contêm campos completos (`author`, `title`, `journal`/`booktitle`, `year`, `doi`).

---

### Passo 5: Estruturação das Seções e Fichas de Escopo (Fase 3)

Solicite ao agente de escrita o delineamento da arquitetura do manuscrito:
> `/writing-agent "Criar outline do artigo com Scope Cards por seção"`

O agente gerará o sumário expandido em `papers/paper-redes-neurais/outline.md`. Cada seção terá uma **Ficha de Escopo** obrigatória:

```markdown
<!-- SCOPE CARD
section: 01-introduction
core_claim: A robustez adversarial tradicional falha em modelos de larga escala.
required_citations: [Goodfellow2015, Madry2018]
excluded_topics: [Detalhes matemáticos de otimização convexa]
connection: Prepara o terreno para os fundamentos teóricos em 02-theory.
-->
```

> **Checkpoint (Gate G3):** Confirme se a tese de cada seção está delimitada e confirme digitando:
> `"Arquitetura e Scope Cards aprovadas"`.

---

### Passo 6: Redação Modular com Padrão CEI (Fase 4)

Com a estrutura aprovada, ordene a redação das seções:
> `/writing-agent "Redigir todas as seções do manuscrito"`

O `writing-agent` redigirá seção por seção sob `papers/paper-redes-neurais/draft/`:
- `00-abstract.md`
- `01-introduction.md`
- `02-theory.md`
- `03-methodology.md`
- `04-findings.md`
- `05-discussion.md`
- `06-conclusion.md`
- `07-tables.md`
- `08-figure-legends.md`

Cada parágrafo substantivo seguirá o padrão **CEI** (*Claim $\rightarrow$ Evidence $\rightarrow$ Interpretation*).

> **Checkpoint:** Verifique a presença de todos os arquivos de rascunho:
> ```bash
> ls papers/paper-redes-neurais/draft/
> ```

---

### Passo 7: Validações Determinísticas de Citação e Dados (Fase 5)

Antes de qualquer revisão humana, execute os gates de validação algorítmica:

1. **Gate G4 (Citação ↔ Bibliografia):**
   ```bash
   python .agents/skills/academic-citation-manager/scripts/citation_gate.py \
     papers/paper-redes-neurais/draft \
     papers/paper-redes-neurais/research/references.bib
   ```
   *Resultado esperado:* `GATE PASS: 0 orphan citations, 0 missing keys.`

2. **Gate G4.5 (Integridade de Dados):**
   ```bash
   python .agents/skills/academic-data-validator/scripts/data_congruence_gate.py \
     papers/paper-redes-neurais
   ```
   *Resultado esperado:* `DATA CONGRUENCE: PASS` (0 inconsistências entre texto e tabelas).

> **Checkpoint:** Os relatórios `review/citation-audit-report.md` e `review/data-congruence-report.md` foram criados sem bloqueios.

---

### Passo 8: Humanização e Auditoria de Qualidade de Prosa (Fase 6)

Remova o "tom de IA" e verifique se há desvios estilísticos:

1. **Passada de Humanização:**
   > `/academic-humanizer "Ajustar cadência, tom sênior e eliminar clichês de IA no rascunho"`

2. **Auditoria Estática de Prosa:**
   ```bash
   python .agents/skills/academic-writing-reviewer/scripts/audit_writing.py \
     papers/paper-redes-neurais/draft \
     --output papers/paper-redes-neurais/review/writing-review-report.md
   ```

> **Checkpoint:** O relatório `writing-review-report.md` atesta score $\ge 70/100$ e status `PASS_FOR_DIM5`.

---

### Passo 9: Painel de Revisão por Pares 6-D e Loop Contínuo (Fase 7)

Convoque o comitê avaliador simulado:
> `/review-agent "Executar revisão por pares completa em 6 dimensões"`

O agente simula o Editor-Chefe, três revisores temáticos e o Advogado do Diabo, avaliando Originalidade, Metodologia, Fundamentação, Clareza, Prosa e Rigor Conclusivo.

- **Se o veredito for `ACCEPT` (Nota $\ge 7.0/10$ e 0 erros críticos):** O manuscrito está aprovado no Gate G5.
- **Se o veredito for `REVISE_AND_RESUBMIT`:** O orquestrador acionará o `writing-agent` para corrigir os apontamentos e retornará automaticamente ao Passo 7.

> **Checkpoint (Gate G5):** O relatório `papers/paper-redes-neurais/review/peer-review-report.md` exibe `Verdict: Accept`.

---

### Passo 10: Compilação dos Entregáveis Finais (Fase 8 e 9)

Com todos os gates superados, gere os documentos finais prontos para submissão:
> `/paper-generator "Exportar artigo final em formato Word DOCX e submissão cega"`

O agente executa o `Output Format Gate` e compila os arquivos em `papers/paper-redes-neurais/output/`:
- `Main-Text-anonymised.docx` (Corpo do artigo anonimizado para blind review).
- `Title-Page.docx` (Página de título com autores, afiliações e notas biográficas).
- `Submission-Summary.docx` (Resumo executivo de submissão).

> **Checkpoint (Output Format Gate):**
> Execute o validador para certificar integridade absoluta do arquivo:
> ```bash
> python .agents/skills/academic-format-validator/scripts/validate_formats.py \
>   papers/paper-redes-neurais
> ```
> O resultado final deve ser: `Output Format Gate: PASS (0 blocking, 0 warnings)`.

---

## 4. Resultado Esperado

Ao concluir este tutorial, seu diretório apresentará a seguinte estrutura consolidada:

```text
papers/paper-redes-neurais/
├── prd.md                              ← Requisitos aprovados [Gate G1]
├── plan.md                             ← Roteiro de tarefas concluídas [Gate G2]
├── outline.md                          ← Estrutura com Scope Cards [Gate G3]
├── research/
│   ├── literature_review.md            ← Análise da literatura OpenAlex
│   └── references.bib                  ← Base BibTeX enriquecida
├── draft/
│   ├── 00-abstract.md a 06-conclusion.md ← Seções em prosa CEI
│   ├── 07-tables.md                    ← Tabelas do estudo
│   └── 08-figure-legends.md            ← Legendas de figuras
├── review/
│   ├── citation-audit-report.md        ← Validação G4 (0 órfãs)
│   ├── data-congruence-report.md       ← Validação G4.5 (100% congruência)
│   ├── writing-review-report.md        ← Score Dimensão 5 (sem vícios de IA)
│   ├── peer-review-report.md           ← Parecer 6-D [Gate G5: Accept]
│   └── format-validation-report.md     ← Parecer Output Format Gate
├── output/
│   ├── Main-Text-anonymised.docx       ← Manuscrito final para submissão
│   └── Title-Page.docx                 ← Identificação dos autores
└── process-record.md                   ← Log de decisões e governança humana
```

---

## 5. Próximos Passos

Agora que você dominou o ciclo completo de produção científica:

1. **Customizar o Guia de Estilo:** Crie `papers/paper-redes-neurais/resources/style-guide.md` para orientar o vocabulário e o tom específico do seu nicho de pesquisa.
2. **Exportar para LaTeX:** Se o seu periódico exigir TeX/PDF, use a skill `latex-template-converter` para migrar para o modelo oficial (IEEEtran, ACM sigconf, Springer LNCS ou NeurIPS).
3. **Auditoria de Integridade Contínua:** Mantenha os hooks de formato ativados no seu IDE para evitar commits com quebra de markdown ou erros sintáticos.
