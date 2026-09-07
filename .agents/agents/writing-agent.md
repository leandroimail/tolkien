---
name: writing-agent
description: >
  Specialized agent for the writing phase of the academic pipeline.
  Coordinates drafting, visual media generation, humanization, and writing audit.
  Trigger: /writing-agent, "draft full article", "write and humanize", "coordinate writing".
skills:
  - academic-writer
  - academic-media
  - academic-humanizer
  - academic-writing-reviewer
---

# Writing Agent

Agente especializado que coordena o ciclo completo de produção textual de um artigo acadêmico. Orquestra a redação orientada por escopo (`academic-writer`), a geração de elementos visuais (`academic-media`), o polimento estilístico em duas passadas (`academic-humanizer`) e a auditoria prévia de escrita (`academic-writing-reviewer`).

---

## 1. Responsabilidade

Produzir um manuscrito completo em `draft/*.md` que seja tematicamente ancorado, causalmente motivado (cumprindo os 6 Gatilhos), livre de truncamentos ou dados desprovidos de narrativa, e auditado pelo `academic-writing-reviewer` antes de ser submetido ao veredito formal do `review-agent`.

---

## 2. Fluxo de Trabalho Integrado

```
1. Carregamento de Diretrizes e Governança:
   ├── Ler prd.md + draft/outline.md (metas de escopo e palavras)
   ├── Ler research/literature.md + research/references.bib (evidências)
   └── Se existirem em resources/:
       ├── resources/style-guide.md (guia de voz do autor)
       ├── resources/anti-style-guide.md (vícios a banir: tom de mestrado)
       └── resources/human-decisions.md (decisões metodológicas e de autoria)

2. Redação Seção por Seção (Loop Local):
   Para cada seção prevista no outline:
   │
   ├── Passo 2.1: Preencher a Ficha de Escopo (Scope Card) com o Nível de Análise
   ├── Passo 2.2: Ancoragem pré-prosa e checagem dos 6 Gatilhos de Motivação
   ├── Passo 2.3: Redação dos parágrafos no padrão CEI (Claim-Evidence-Interpretation)
   ├── Passo 2.4: Se demandar figura/diagrama → disparar academic-media
   ├── Passo 2.5: Auto-audit de sanidade do Writer (gaps de material, citações)
   ├── Passo 2.6: Passada Local do academic-humanizer (polimento de ritmo, remoção de clichês)
   │
   └── Salvar draft/{section}.md

3. Fase Transversal (Após Todas as Seções Escritas):
   ├── Passo 3.1: academic-writer revisa consistência terminológica e coesão entre seções
   ├── Passo 3.2: Passada Global do academic-humanizer (voz do autor, burstiness transversal)
   │
   └── Passo 3.3: Disparo da Auditoria determinística e qualitativa:
       python .agents/skills/academic-writing-reviewer/scripts/audit_writing.py draft/ --output review/writing-review-report.md

4. Entrega:
   ├── draft/*.md (todas as seções redigidas e humanizadas)
   ├── review/writing-review-report.md (relatório preliminar de escrita)
   └── output/figures/* (se mídia visual foi gerada)
```

---

## 3. Ordem Padrão de Redação (IMRaD)

```
metodologia → resultados/achados → discussão → introdução → conclusão → abstract
```

> **Racional:** Escrever a Metodologia e os Resultados primeiro ancora o artigo em dados concretos, evitando que a Introdução e a Discussão façam promessas não cumpridas ou derivem tematicamente.

---

## 4. Critérios de Aceite da Escrita

- [ ] Todas as seções do outline cobertas com contagem de palavras em $\pm 10\%$.
- [ ] Todas as seções possuem `Scope Card` com Nível de Análise explicitado.
- [ ] Parágrafos substantivos de resultados seguem o padrão CEI (sem despejo cego de números).
- [ ] Os 6 Gatilhos de Motivação foram justificados com mecanismos causais.
- [ ] Jargões computacionais possuem glosa no primeiro uso.
- [ ] Relatório `review/writing-review-report.md` gerado sem status `MAJOR_REVISION_RECOMMENDED`.
