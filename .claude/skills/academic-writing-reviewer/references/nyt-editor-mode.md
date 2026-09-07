# Protocolo do Modo Editor do NYT (nyt-editor-mode.md)

> Inspirado na prática editorial do *New York Times* descrita por Paul Goldsmith-Pinkham (*A Causal Affair*).
> **Princípio Central:** O revisor audita e comenta; **nunca reescreve o texto diretamente**. A autoria permanece integralmente do pesquisador humano.

---

## 1. Estrutura Canônica de um Comentário Editorial

Todo apontamento qualitativo deve conter obrigatoriamente 4 elementos:

```markdown
### [CÓDIGO_ISSUE] [SEVERIDADE] Seção:Linha
- **Trecho Citado:** "[Trecho exato de até 25 palavras]"
- **Diagnóstico:** [Explicação clara do problema conceitual, retórico ou estilístico]
- **Efeito no Leitor / Revisor:** [Como a banca ou um orientador sênior lê essa frase — ex.: "soa como insegurança", "parece terceirizado", "deixa o leitor perdido sem saber o porquê"]
- **Direção de Correção:** [Instrução estratégica de reescrita sem entregar a frase pronta — ex.: "Explicite o mecanismo causal entre a escolha da hierarquia e a redução de tokens antes de apresentar os percentuais"]
```

---

## 2. Exemplo Prático de Aplicação

### ❌ Exemplo Errado (Reescrita direta não solicitada):
> *"O trecho 'vale ressaltar que a latência aumentou' ficou ruim. Sugiro trocar por: 'A latência computacional elevou-se em 15%'."*

### ✅ Exemplo Correto (Padrão Editor NYT):
> **[JAR-01] [WARNING] 01-introduction.md:L42**
> - **Trecho Citado:** *"A orquestração descentralizada introduz gargalos severos de latência durante as rodadas de consenso."*
> - **Diagnóstico:** Termo técnico de computação (*latência*) empregado sem glosa funcional em artigo direcionado a periódico de Gestão / Engenharia de Produção.
> - **Efeito no Leitor / Revisor:** Professores e avaliadores de áreas de administração e engenharia organizacional podem interromper a leitura por opacidade conceitual (problema apontado na reunião pelos orientadores).
> - **Direção de Correção:** Insira uma oração explicativa entre parênteses ou vírgulas definindo latência em termos de atraso temporal de comunicação entre agentes antes de discutir as rodadas de consenso.

---

## 3. As 4 Lentes Críticas do Editor

Ao analisar o manuscrito, o revisor deve alternar entre 4 perspectivas:
1. **A Lente do Orientador Sênior:** *"Isso parece um pesquisador maduro ou um aluno de mestrado justificando timidamente o que leu?"*
2. **A Lente do Par Interdisciplinar:** *"Um pesquisador de teoria das organizações consegue entender este gráfico sem precisar de um diploma de ciência da computação?"*
3. **A Lente da Condução Narrativa:** *"O autor está me guiando através de uma tese clara ou está apenas despejando dados de simulação esperando que eu tire as conclusões?"*
4. **A Lente da Integridade de Autoria:** *"Onde está a voz do autor nesta discussão? Há reflexão humana substantiva ou o texto parece ter sido gerado em lote por uma máquina?"*
