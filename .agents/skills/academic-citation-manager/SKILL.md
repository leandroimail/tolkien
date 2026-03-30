---
name: academic-citation-manager
description: >
  Gestão e validação de citações in-text — formato, completude, consistência e
  validação cruzada com references.bib (gate Citation↔Bibliography).
  Trigger: /academic-citation-manager, "verificar citações", "formatar citações",
  "citation audit", "check citations", "citation gate".
allowed-tools: [Read, Write, Edit, Bash, Grep]
metadata:
  version: "1.0"
  depends_on: "academic-bibliography-manager"
---

# Academic Citation Manager

Gestão e validação de citações in-text no draft do artigo acadêmico. Responsável pelo gate determinístico Citation↔Bibliography que bloqueia o pipeline se houver inconsistências.

## When To Use

- Rastrear todas as citações `\cite{key}` ou `(Autor, Ano)` no draft
- Validar formato de citação conforme estilo do PRD
- Identificar citações órfãs (no texto mas sem entrada no `.bib`)
- Identificar citações fantasma (no `.bib` mas não citadas no texto)
- Executar o gate Citation↔Bibliography antes da revisão
- Detectar chaves duplicadas citando a mesma obra

## When Not To Use

- Para validar os campos do `.bib` → use `academic-bibliography-manager`
- Para buscar novos papers → use `academic-researcher`
- Para redigir o text → use `academic-writer`

## Prerequisites

1. **Draft completo** — `draft/*.md` (todas as seções)
2. **`research/references.bib`** — validado pelo bibliography-manager
3. **`prd.md`** — para identificar estilo de citação (APA, IEEE, ABNT etc.)

## Method

### Fase 1: Extração de Citações

Varrer todos os arquivos `draft/*.md` e extrair:
- Todas as ocorrências de `\cite{key}` (LaTeX style)
- Todas as ocorrências de `(Autor, Ano)` ou `[N]` (texto inline)
- Posição exata: arquivo, linha, contexto

```bash
python scripts/extract_citations.py draft/
```

### Fase 2: Extração de Chaves do .bib

Parsear `research/references.bib` e extrair todas as chaves de citação.

### Fase 3: Gate Citation↔Bibliography (BLOQUEANTE)

```
REGRA 1: ∀ key em \cite{key} no draft → ∃ entrada @{type}{key,...} em references.bib
         Violação = CITAÇÃO ÓRFÃ

REGRA 2: ∀ key em references.bib → ∃ pelo menos 1 \cite{key} no draft
         Violação = CITAÇÃO FANTASMA

REGRA 3: ∀ entry em references.bib → campos obrigatórios por tipo preenchidos
         Violação = ENTRADA INCOMPLETA

RESULTADO ESPERADO: 0 violações
BLOQUEANTE: Sim — pipeline não avança se resultado ≠ 0
```

```bash
python scripts/citation_gate.py draft/ research/references.bib
```

### Fase 4: Validação de Formato

Por estilo de citação:

| Estilo | Formato In-Text | Exemplo |
|--------|----------------|---------|
| APA | (Autor, Ano) | (Smith, 2023) |
| IEEE | [N] | [1] |
| Vancouver | (N) | (1) |
| ABNT | (AUTOR, Ano) | (SILVA, 2023) |
| Chicago | (Autor Ano) or footnotes | (Smith 2023) |

### Fase 5: Detecção de Problemas

- **Duplicata de citação**: mesma obra citada com chaves diferentes
- **Autocitação excessiva**: > 15% das citações são do mesmo autor
- **Citações desbalanceadas**: concentração desproporcional em uma seção
- **Citações antigas**: > 50% das fontes com mais de 10 anos (flag, não bloqueante)

### Fase 6: Correção e Relatório

1. Corrigir problemas automaticamente quando possível
2. Gerar relatório: `review/citation-report.md`

## Self-Review

### Determinístico
- [ ] Gate Citation↔Bibliography: 0 violações das 3 regras
- [ ] 100% das citações no formato correto para o estilo do PRD
- [ ] 0 chaves duplicadas referenciando a mesma obra

### Agêntico
- Re-executar gate após correções para confirmar 0 inconsistências
- Verificar distribuição de citações entre seções

## Output

```markdown
### Citation Validation Report
- **Citations in draft**: N unique keys
- **Entries in .bib**: M entries
- **Orphan citations** (in text, not in .bib): N → list
- **Phantom citations** (in .bib, not in text): N → list
- **Format violations**: N → list with corrections
- **Gate result**: ✅ PASS (0 violations) | ❌ FAIL (N violations)
```

## References

- `references/citation-formats.md` — guia de formatos por estilo
- `references/citation-quality.md` — métricas de qualidade bibliográfica
