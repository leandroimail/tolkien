# Catálogo de Padrões e Vícios de IA (ai-patterns.md)

> Base empírica: Kobak et al. (Science Advances 2025), WikiProject AI Cleanup (Wikipédia) e corpus acadêmico luso-brasileiro.
> Objetivo: Identificar e remover a "voz de máquina", devolvendo a naturalidade e autoridade à prosa acadêmica.

---

## 1. Vocabulário Inflado e Rotação Lexical Fixa

Modelos de linguagem recorrem a um léxico artificialmente pomposo para soar autoritativos:

| Termo em Inglês (Kobak 2025) | Equivalente em Português | Por que evitar | Alternativa Humana Direta |
|---|---|---|---|
| **delve / delves into** (28× mais frequente) | debruçar-se sobre, aprofundar-se | Clichê máximo de IA pós-2023 | investigar, analisar, examinar, mensurar |
| **underscore / underscores** (13.8×) | ressaltar, sublinhar, evidenciar | Usado como muleta semântica | indicar, mostrar, corroborar, demonstrar |
| **showcase / showcasing** (10.7×) | apresentar com orgulho, ilustrar | Tom de marketing/showcase | relatar, reportar, documentar |
| **pivotal / crucial** | crucial, preponderante, basilar | Elogio vazio de significância | central, relevante, necessário |
| **tapestry / realm** | tapeçaria, ecossistema (vago) | Metáfora poética fora de lugar | estrutura, conjunto, dinâmica, sistema |
| **testament to** | testemunho inequívoco de | Retórica inflada | evidência de, indício de, sinal de |
| **robust / robustly** | robusto, de forma robusta | Repetição sem prova técnica | confiável, consistente (ou dar a estatística) |
| **seamless / seamlessly** | perfeito, sem atrito, fluido | Promessa publicitária | integrado, direto, contínuo |
| **foster / leveraging** | fomentar, alavancar | Jargão corporativo oco | estimular, produzir, aplicar, utilizar |

---

## 2. Falsos Paralelismos e Imitação de Insight

Estruturas sintáticas que tentam criar profundidade artificial:

- ❌ **Negative Parallelisms:**
  - *"It's not just X, it's Y"* $\rightarrow$ Substitua por afirmação direta: *"O modelo altera tanto X quanto Y"*.
  - *"Não se trata apenas de agilidade, mas sim de uma revolução na coordenação"* $\rightarrow$ *"A coordenação apresentou ganho de 30% no tempo de convergência"*.
  - *"No X. No Y. Just Z."* $\rightarrow$ Eliminar estilo publicitário.

- ❌ **Fórmula "Apesar dos Desafios...":**
  - *"Apesar dos desafios inerentes à latência, a arquitetura posiciona-se como um marco promissor..."*
  - $\rightarrow$ Apresentar os dados objetivos de latência e os limites reais da arquitetura.

---

## 3. Aberturas Limpa-Garganta (*Throat-Clearing*)

Fórmulas de abertura que atrasam a entrega do conteúdo:

- ❌ *"In today's rapidly evolving technological landscape..."*
- ❌ *"No cenário contemporâneo de rápida evolução..."*
- ❌ *"Vale ressaltar que os agentes desempenham um papel crucial..."*
- ❌ *"É mister destacar a importância de..."*
- ❌ *"Como é de conhecimento geral na literatura..."*
- **Regra:** Remova as fórmulas de abertura inteiras e inicie a sentença pelo sujeito concreto e verbo principal.

---

## 4. Particípios Pendurados e Fechamentos Ocos

Fechamentos genéricos no final de parágrafos:

- ❌ *"...underscoring the importance of future empirical investigations."*
- ❌ *"...destacando assim a relevância fundamental de uma coordenação eficiente."*
- ❌ *"...evidenciando a necessidade premente de novos estudos."*
- **Regra:** Substitua a fórmula genérica pela hipótese ou implicação teórica concreta que o leitor deve reter.

---

## 5. Monotonia Estrutural e *Burstiness*

- **Sintoma:** Todos os parágrafos com 4 a 5 linhas, e todas as sentenças com 15 a 20 palavras.
- **Correção:** Varie propositalmente o ritmo:
  - Sentença curta de impacto (8–12 palavras): *"A hierarquia rígida impõe custos imediatos."*
  - Sentença articulada de desenvolvimento (20–30 palavras): *"Quando cada mensagem entre agentes exige autorização síncrona do orquestrador central, o tempo total de resposta cresce linearmente com o tamanho do time, anulando os ganhos de especialização."*
