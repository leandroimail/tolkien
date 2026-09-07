# Perguntas Antes da Prosa e os 6 Gatilhos de Motivação (questions-before-prose.md)

> Regra fundamental do `academic-writer`: **pensar antes de redigir**.
> A IA nunca deve começar a despejar parágrafos sem antes responder estruturalmente ao objetivo da seção e verificar a incidência dos gatilhos de motivação causal.

---

## 1. Protocolo Pré-Prosa (STORM Check)

Antes de gerar o rascunho de qualquer seção, o agente deve responder internamente às 4 perguntas de ancoragem:

1. **Qual é a alegação central (Claim) desta seção?**  
   *Se o leitor só puder lembrar de uma frase desta seção, qual é ela?*
2. **Quais dados ou fontes concretas sustentam essa alegação?**  
   *Quais números de tabelas ou autores do `.bib` fornecem o chão empírico?*
3. **Qual é o nível de análise exato desta seção?**  
   *Estamos falando do agente individual, do time de agentes ou da empresa como um todo? (Não misturar!)*
4. **O que está expressamente fora do escopo desta seção?**  
   *Quais tentações de digressão devem ser podadas antecipadamente?*

---

## 2. Os 6 Gatilhos de Motivação Obrigatória

A crítica mais severa dos orientadores foi: *"o texto não entra para explicar bem... não descreve a motivação... a discussão ficou muito rala"*.

Para resolver isso sem gerar prolixidade em fatos óbvios, o **dever de motivação profunda ("o porquê")** é acionado estritamente quando o texto atinge um destes 6 pontos de inflexão:

### Gatilho 1: Escolha de Design Arquitetural
- **Quando ocorre:** Quando o texto apresenta uma decisão de projeto (ex.: orquestração centralizada vs. coreografia distribuída; comunicação síncrona vs. assíncrona; divisão estática vs. dinâmica de papéis).
- **Exigência de Prosa:** É proibido apenas dizer *"optou-se pelo modelo hierárquico porque é tradicional"*. Deve-se justificar o trade-off de coordenação, o consumo de tokens e o impacto na latência.

### Gatilho 2: Resultado Contraintuitivo
- **Quando ocorre:** Quando uma configuração simples supera uma complexa, ou quando uma hipótese esperada é refutada pelos dados experimentais.
- **Exigência de Prosa:** É proibido apenas constatar o número. Deve-se formular imediatamente uma hipótese explicativa baseada nos mecanismos internos da ferramenta (*"Esse resultado contraintuitivo decorre de..."*).

### Gatilho 3: Trade-off Técnico/Econômico
- **Quando ocorre:** Decisões que elevam a qualidade da resposta às custas de maior tempo de resposta (latência) ou custo financeiro de inferência.
- **Exigência de Prosa:** Justificar explicitamente por que o aumento no custo ou na latência foi considerado aceitável no desenho do experimento.

### Gatilho 4: Divergência da Literatura Prévia
- **Quando ocorre:** Quando os achados contradizem ou qualificam estudos anteriores citados no referencial teórico.
- **Exigência de Prosa:** Apontar os fatores de contexto, arquitetura, modelo de linguagem base ou tamanho do time de agentes que explicam a divergência.

### Gatilho 5: Invocação de Limite de Escopo
- **Quando ocorre:** Quando o texto estabelece uma fronteira de pesquisa (*"não analisamos a interação com humanos em tempo real"*).
- **Exigência de Prosa:** Explicar a razão metodológica ou conceitual do recorte (evitar que a limitação soe como preguiça metodológica ou falha de execução).

### Gatilho 6: Empréstimo Conceitual / Transposição Teórica
- **Quando ocorre:** Ao aplicar teorias concebidas para organizações humanas (ex.: Mintzberg, Weber, Contingência Estrutural) a sistemas de agentes de IA.
- **Exigência de Prosa:** Explicar explicitamente os limites da metáfora: em que pontos a transposição é fiel e em que pontos a natureza algorítmica e a memória estocástica dos LLMs quebram a premissa da teoria original.
