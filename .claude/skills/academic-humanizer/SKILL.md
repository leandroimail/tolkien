---
name: academic-humanizer
description: >
  Register adjustment, humanization, and naturalization of academic writing.
  Removes typical AI markers, throat-clearing, and structural monotony while
  maintaining academic rigor and factual integrity. Supports EN and PT-BR.
  Trigger: /academic-humanizer, "humanize", "adjust register",
  "naturalize writing", "humanize text", "remove AI feel".
allowed-tools: [Read, Write, Edit, Bash]
metadata:
  version: "2.0"
  role: "stylist"
  depends_on: "academic-writer"
---

# Academic Humanizer v2

Humanização e naturalização de prosa científica gerada ou assistida por IA. Remove a artificialidade, o vocabulário hiper-inflado e a monotonia rítmica do texto gerado por modelos de linguagem, garantindo a autoridade da voz científica, a precisão conceitual e a integridade factual.

---

## 1. As Duas Passadas Obrigatórias de Humanização

O humanizador opera em **dois momentos distintos** do ciclo de vida do manuscrito:

### Passada 1: Local (por Seção)
- **Quando ocorre:** Imediatamente após o `academic-writer` redigir qualquer `draft/{section}.md`.
- **Foco:**
  - Remoção de conectivos inflados e fórmulas limpa-garganta (*Além disso, Ademais, Outrossim, Vale ressaltar que*).
  - Variação do comprimento de frases (*burstiness*: alternar frases curtas de 8–12 palavras com frases analíticas de 20–30 palavras).
  - Eliminação de falsos paralelismos (*"Não apenas X, mas Y"*).
  - Preservação intacta de todas as citações e chaves `\cite{}`.

### Passada 2: Global (Manuscrito Completo)
- **Quando ocorre:** Na Fase 6 do pipeline, após todas as seções terem sido redigidas e validadas nos gates factuais (G4 e G4.5).
- **Foco:**
  - Consistência terminológica transversal (o mesmo conceito não deve mudar de nome entre seções).
  - Erradicação de redundâncias cruzadas (eliminar parágrafos que repetem alegações da Introdução na Discussão sem avançar no insight).
  - Calibração de tom com o `resources/style-guide.md` e verificação estrita do `resources/anti-style-guide.md` (banir tom de mestrado e didatismo condescendente).
  - Teste da leitura em voz alta (o texto soa como um pesquisador experiente ou como um press release corporativo?).

---

## 2. Linhas Vermelhas (Guardrails Absolutos)

1. **NUNCA ALTERAR CONTEÚDO FACTUAL:** Jamais modifique números, porcentagens, tamanhos de amostra ou achados estatísticos ao tentar melhorar o estilo.
2. **NUNCA INVENTAR OU REMOVER CITAÇÕES:** Todas as chaves `\cite{}` e referências autor-data devem permanecer estritamente intactas.
3. **HUMANIZAR NÃO É INFORMALIZAR:** O texto acadêmico deve permanecer formal, rigoroso e técnico. Proibido usar gírias, contrações coloquiais ou analogias popularescas.
4. **CONSISTÊNCIA TERMINOLÓGICA > VARIEDADE VAZIA:** Em textos científicos, mudar o termo técnico a cada frase ("sinônimo-ciclismo") confunde o leitor. Use o termo técnico correto com consistência.
5. **NÃO É EVASÃO DE DETECTORES:** O objetivo é produzir boa prosa científica, clara e substantiva, e não tentar enganar ferramentas estatísticas de detecção.

---

## 3. Protocolo de Reescrita Parágrafo por Parágrafo

Para cada trecho reescrito, o humanizador deve manter no log de alterações:
```
**Original:** [trecho com vício de IA]
**Revisado:** [texto naturalizado]
**Justificativa:** Removido 'vale ressaltar que', variado o ritmo de sentenças (10, 24 e 14 palavras) e eliminada fórmula de falso contraste.
```

---

## 4. Referências da Skill

- `references/ai-patterns.md` — Catálogo de 26 padrões empíricos de IA (Kobak 2025 + WikiProject AI Cleanup) para EN e PT-BR.
- `references/language-specific.md` — Diretrizes de registro acadêmico para Português Brasileiro (ABNT/Gestão) e Inglês Internacional.
- `references/rewriting-principles.md` — Princípios de reescrita sem perda de conteúdo e preservação de coesão.
- `references/fi-specific.md` — Diretrizes específicas para língua finlandesa (carregadas sob demanda).
