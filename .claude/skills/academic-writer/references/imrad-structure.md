# Estrutura IMRaD e Diretrizes por Seção (imrad-structure.md)

> Arquitetura detalhada de seções para artigos científicos, revisões sistemáticas e estudos de caso.

---

## 1. Diretrizes por Seção (O que deve e o que NÃO deve ter)

| Seção | Deve Conter Obrigatoriamente | É Estritamente Proibido Conter |
|---|---|---|
| **Abstract** | Contexto sucinto, gap concreto, objetivo, método, principais resultados com números-chave e conclusão com implicação. | Citações bibliográficas formais, abreviações não definidas, jargão opaco sem glosa. |
| **Introdução** | Contextualização do problema, gap claro na literatura, pergunta de pesquisa, objetivo, tese central e roteiro do artigo. | Resultados antecipados em detalhe, interpretação de achados, conclusões finais. |
| **Referencial Teórico** | Mapeamento do estado da arte, síntese crítica de teorias clássicas e contemporâneas, delimitação de conceitos chave. | Descrição do método do próprio autor, dados da pesquisa própria. |
| **Metodologia** | Desenho da pesquisa, corpus/amostra, variáveis/métricas, procedimentos de coleta/execução, reprodutibilidade e governança humana. | Interpretação de resultados ou discussões conceituais abstratas. |
| **Resultados / Achados** | Fatos empíricos, dados de tabelas e figuras, estatísticas descritivas e inferenciais organizadas com estrutura CEI. | Especulações não suportadas pelos dados, confronto aprofundado com a literatura prévia. |
| **Discussão** | Diálogo dos resultados com a literatura prévia, interpretação causal do "porquê" (cumprindo os 6 Gatilhos de Motivação), limitações e trade-offs. | Novos dados ou tabelas que não foram apresentados na seção de Resultados. |
| **Conclusão** | Resposta direta à pergunta de pesquisa, contribuições teóricas e práticas, limitações fundamentadas e agenda de pesquisa futura. | Apresentação de novos resultados ou repetição literal da Introdução. |

---

## 2. A Ficha de Escopo da Seção (`Scope Card`)

Antes de gerar qualquer seção, o `academic-writer` deve inserir o bloco de metadados no topo do arquivo rascunho:

```markdown
<!-- SCOPE_CARD
Section: {nome_da_secao}.md
Level_of_Analysis: {Ex.: Team of Agents [STRICT] (NOT Entire Organization)}
Primary_Question: {A pergunta específica que este texto responde}
Out_of_Scope: {Tópicos vizinhos estritamente proibidos de expandir}
Theoretical_Anchor: {Teoria ou construto base}
Mandatory_Inputs: {Arquivos de pesquisa ou tabelas de onde os dados provêm}
-->
```
