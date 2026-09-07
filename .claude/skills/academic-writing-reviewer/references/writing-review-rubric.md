# Rubrica de Avaliação da Prosa Acadêmica (writing-review-rubric.md)

> Escala: 0 a 100 pontos · Alimenta a Dimensão 5 (Writing & Style) do veredito do `academic-reviewer`.

A pontuação da auditoria combina o **Backstop Determinístico** (scripts de marcadores de IA, repetição, tensões e glosa) com a **Avaliação Qualitativa por Comentários no Modo Editor do NYT**.

---

## 1. As 7 Dimensões da Prosa Acadêmica (Pesos)

| Categoria | Código Base | Peso | Foco de Avaliação |
|---|---|---|---|
| **1. Marcadores e Vícios de IA** | `AIM` | 20% | Ausência de vocabulário hiper-inflado (Kobak et al.), falsos paralelismos retóricos e aberturas clichês. |
| **2. Repetição e Redundância** | `REP` | 15% | Ausência de parágrafos espelhados entre Introdução e Discussão; fluidez e diversidade lexical em sentenças vizinhas. |
| **3. Narrativa e Coerência (CEI)** | `UNM` | 20% | Estrutura *Claim $\rightarrow$ Evidence $\rightarrow$ Interpretation* em parágrafos de dados. Prosa que conduz o leitor em vez de apenas despejar números. |
| **4. Motivação e Reflexão (6 Gatilhos)** | `UNM` | 15% | Cumprimento do dever de justificativa nos 6 pontos de inflexão teórica/arquitetural. Ausência de constatações "ralas". |
| **5. Escopo e Nível de Análise** | `SCP` | 10% | Estrita aderência ao nível de análise (ex.: time de agentes vs. organização inteira) delimitado na `Scope Card`. |
| **6. Jargão e Calibração de Audiência** | `JAR` | 10% | Glosa funcional de termos computacionais no primeiro uso para bancas e periódicos de Gestão / Engenharia de Produção. |
| **7. Tom e Voz Autoral** | `VOI` | 10% | Postura de pesquisador sênior; erradicação do "tom de mestrado" e de insegurança acadêmica (*hedging soup*). |

---

## 2. Tabela de Conversão e Status Advisory

| Faixa de Score | Status Advisory | Significado para a Dimensão 5 (6-D Review) |
|---|---|---|
| **85 – 100** | `PASS_FOR_DIM5` | Prosa fluida, madura e transparente. Aprovado sem restrições de estilo. |
| **70 – 84** | `PASS_WITH_MINOR_ISSUES` | Escrita sólida, mas com oportunidades pontuais de variação rítmica ou glosa. Permite recomendação de *Minor Revision*. |
| **< 70** (ou $\ge 1$ CRITICAL) | `MAJOR_REVISION_RECOMMENDED` | Prosa com problemas graves de repetição, contradição, jargão opaco ou marcas densas de geração automática. Limita a nota da Dimensão 5 a $\le 60$. |

---

## 3. Protocolo de Pré-Compromisso Anti-Sycophancy

O revisor deve seguir 3 regras mecânicas para evitar conivência ou elogios vazios:
1. **Nota Exige Trecho Citado:** Nenhuma pontuação deduzida ou concedida é válida sem a citação literal do trecho (`draft/{section}.md:L{linha}`) que justifica o apontamento.
2. **Proibido Elogio de Fechamento:** É vedado encerrar o relatório com parágrafos genéricos de congratulação (*"No geral, o artigo está muito bem escrito e promissor..."*). O relatório deve encerrar diretamente no plano de ação corretiva.
3. **Lente "So What?":** Toda apresentação de dados que não responder *"Qual a implicação teórica deste número?"* deve ser penalizada na Categoria 3.
