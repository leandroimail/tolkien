---
name: academic-bibliography-manager
description: >
  Gestão e validação do references.bib — completude de campos, formato BibTeX,
  enriquecimento via OpenAlex, detecção de duplicatas e retrações.
  Trigger: /academic-bibliography-manager, "validar bibliografia", "gerar BibTeX",
  "resolver DOI", "enriquecer referências", "verificar .bib".
allowed-tools: [Read, Write, Edit, Bash, WebFetch]
metadata:
  version: "1.0"
  depends_on: "academic-researcher"
---

# Academic Bibliography Manager

Gestão, validação e enriquecimento do arquivo `references.bib` de um projeto de artigo acadêmico. Garante integridade bibliográfica como pré-requisito para o gate Citation↔Bibliography.

## When To Use

- Validar completude de campos obrigatórios em cada entrada BibTeX
- Enriquecer entradas incompletas via OpenAlex API
- Resolver DOI → metadados completos → BibTeX
- Detectar e remover duplicatas (por DOI ou título)
- Verificar se artigos foram retratados (`is_retracted`)
- Formatar `.bib` conforme estilo do PRD (APA, IEEE, ABNT etc.)
- Antes do gate Citation↔Bibliography (pré-requisito)

## When Not To Use

- Para gerenciar citações **in-text** no draft → use `academic-citation-manager`
- Para buscar literatura e triagem → use `academic-researcher`
- Para formatar o paper final em LaTeX → use skill `latex`

## Prerequisites

1. **`research/references.bib`** — arquivo BibTeX bruto (gerado pelo researcher ou manualmente)
2. **`prd.md`** — para identificar estilo de citação e campo da disciplina
3. Conexão com internet (para OpenAlex API — opcional mas recomendado)

## Method

### Fase 1: Carga e Inventário

1. Ler `research/references.bib` e parsear todas as entradas
2. Classificar cada entrada por tipo (`@article`, `@inproceedings`, `@book`, `@misc`)
3. Gerar inventário: total de entradas, tipos, campos presentes/ausentes

### Fase 2: Validação de Campos Obrigatórios

Campos obrigatórios por tipo:

| Tipo | Campos Obrigatórios |
|------|-------------------|
| `@article` | author, title, journal, year, volume, pages |
| `@inproceedings` | author, title, booktitle, year |
| `@book` | author/editor, title, publisher, year |
| `@misc` | author, title, year, url, note |

Executar validador:
```bash
python scripts/validate_bib.py research/references.bib
```

### Fase 3: Detecção de Duplicatas

Critérios de duplicata:
- DOI idêntico entre duas entradas
- Título com similaridade ≥ 90% (normalizado lowercase, sem pontuação)
- Mesmo author + year + título similar

```bash
python scripts/check_bib_duplicates.py research/references.bib
```

### Fase 4: Enriquecimento via OpenAlex

Para entradas com campos faltantes que possuem DOI:

```bash
# Polite pool: inclui email para 10 req/s
curl -s "https://api.openalex.org/works/https://doi.org/{DOI}?mailto={email}"
```

Mapeamento OpenAlex → BibTeX:
- `title` → `title`
- `authorships[*].author.display_name` → `author` (formato "Last, First and ...")
- `primary_location.source.display_name` → `journal`
- `publication_year` → `year`
- `biblio.volume` → `volume`
- `biblio.first_page`-`biblio.last_page` → `pages`
- `doi` → `doi`
- `is_retracted` → flag de alerta

### Fase 5: Verificação de Retrações

Para cada entrada com DOI, verificar `is_retracted` via OpenAlex:
- Se `true`: emitir **ALERTA CRÍTICO** e sugerir remoção ou substituição

### Fase 6: Formatação e Saída

1. Padronizar formatação do `.bib`:
   - Campos em ordem consistente
   - Chaves de citação no formato `PrimeiroAutorAnoKeyword`
   - Caracteres especiais protegidos com `{}`
   - Páginas com `--` (duplo dash)
2. Escrever `research/references.bib` atualizado
3. Gerar relatório em `review/bibliography-report.md`

## Self-Review

### Determinístico
- [ ] 0 entradas com campos obrigatórios faltantes
- [ ] 0 duplicatas detectadas
- [ ] 0 retrações não tratadas
- [ ] Todas as chaves de citação são únicas

### Agêntico
- Avaliar cobertura: as referências cobrem adequadamente as questões do PRD?
- Verificar atualidade: fontes dos últimos 5-10 anos para campos ativos?
- Recomendar fontes adicionais se cobertura temática for insuficiente

## Output

```markdown
### Bibliography Report
- **Total entries**: N
- **Validated**: N/N (100%)
- **Enriched via OpenAlex**: N entries
- **Duplicates removed**: N
- **Retractions found**: N (CRITICAL if > 0)
- **Status**: ✅ Ready for citation gate | ❌ N issues to resolve
```

## References

- `references/openalex-api.md` — guia completo da API OpenAlex
- `references/bibtex-types.md` — campos obrigatórios por tipo de entrada
