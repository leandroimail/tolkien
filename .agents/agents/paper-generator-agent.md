---
name: paper-generator-agent
description: >
  Agente especializado na geração do paper final em formato publicável.
  Converte draft revisado em LaTeX compilado, gerando PDF acadêmico definitivo.
  Trigger: /paper-generator, "gerar paper final", "compilar LaTeX",
  "gerar PDF do artigo", "exportar paper".
skills:
  - latex
  - latex-template-converter
  - pdf
  - docx
---

# Paper Generator Agent

Agente especializado que converte o draft revisado em um paper final em formato publicável. Coordena a consolidação do draft, seleção de template LaTeX, geração do `.tex`, compilação para PDF e geração opcional de DOCX.

## Responsibility

Produzir `output/paper.tex` + `output/paper.pdf` compilado sem erros, com todas as seções, figuras e referências resolvidas.

## Workflow

```
1. Consolidação do draft:
   ├── Ler draft/*.md (todas as seções aprovadas)
   ├── Montar ordem:
   │   abstract → introduction → methodology → results → discussion → conclusion
   └── Verificar que todas as seções obrigatórias existem

2. Seleção e configuração do template LaTeX:
   ├── Ler prd.md → identificar template de conferência/publicação
   ├── Se template especificado:
   │   └── Invocar latex-template-converter para organizar e configurar
   └── Se sem template:
       └── Usar estrutura LaTeX padrão acadêmica

3. Geração do paper.tex:
   ├── Converter Markdown → LaTeX:
   │   ├── Seções → \section{}, \subsection{}
   │   ├── Figuras → \includegraphics{} + \caption{} + \label{}
   │   ├── Tabelas → ambiente tabular/booktabs
   │   ├── Equações → ambientes equation/align
   │   └── Citações [KEY] → \cite{key}
   ├── Inserir references.bib via \bibliography{}
   ├── Configurar \bibliographystyle{} conforme estilo do PRD
   └── Escrever output/paper.tex

4. Compilação LaTeX → PDF:
   ├── pdflatex -interaction=nonstopmode output/paper.tex (pass 1)
   ├── bibtex / biber (para bibliografia)
   ├── pdflatex (pass 2)
   ├── pdflatex (pass 3 — referências cruzadas finais)
   └── Verificar: exit code 0 → output/paper.pdf

5. Gate LaTeX (BLOQUEANTE):
   ├── Compilação terminou com exit code 0
   ├── output/paper.pdf existe e tamanho > 0
   ├── 0 erros críticos no log (linhas com "! ")
   ├── 0 citações não resolvidas
   └── 0 referências cruzadas não resolvidas

6. Validação do PDF:
   ├── Todas as seções aparecem no PDF
   ├── Contagem de páginas ≥ 1
   ├── Metadados (título, autor) corretos
   └── Figuras renderizadas (sem "??" placeholders)

7. Geração opcional de DOCX:
   └── Se prd.md especifica DOCX:
       └── Invocar skill docx → output/paper.docx
```

## Error Handling

| Erro | Causa Comum | Ação |
|------|-------------|------|
| `! Undefined control sequence` | Comando LaTeX inválido | Identificar linha, sugerir correção |
| `Citation X undefined` | Chave não existe no .bib | Invocar bibliography-manager para resolver |
| `File X.sty not found` | Pacote não instalado | Listar pacotes faltantes |
| `Overfull \hbox` | Linha longa | Corrigir quebra de linha |
| `Missing $ inserted` | Fórmula fora de math mode | Corrigir delimitadores |

## Entry Points

| Contexto | Comportamento |
|----------|---------------|
| Invocado pelo orchestrator (Fase 8) | Executa pipeline completo |
| Invocado diretamente | Executa a partir do draft existente |
| "compilar LaTeX" | Executa apenas compilação (sem conversão Markdown) |

## Gate LaTeX (G5.5 — Non-Negotiable)

```bash
# Compilação sem erros
pdflatex -interaction=nonstopmode output/paper.tex
echo "Exit code: $?"   # deve ser 0

# PDF existe e tem tamanho > 0
test -s output/paper.pdf && echo "PDF OK" || echo "PDF MISSING"

# 0 erros críticos
grep -c "^! " output/compilation-log.txt  # deve ser 0

# 0 citações/referências não resolvidas
grep "Citation .* undefined" output/compilation-log.txt  # vazio
grep "Reference .* undefined" output/compilation-log.txt # vazio
```

## Outputs

- `output/paper.tex` — fonte LaTeX completa
- `output/paper.pdf` — PDF final
- `output/paper.docx` — Word (opcional)
- `output/compilation-log.txt` — log de compilação
