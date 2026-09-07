# Grill: Redesign das skills de escrita (writer, writing-reviewer, humanizer)
Date: 2026-09-04

## Intent
Refazer as skills e agentes de escrita do tolkien (academic-writer, revisor da escrita, academic-humanizer) com base na biblioteca `escrita_academica/` e no relatório `relatorio_criticas_escrita_ia.md` (críticas da reunião), para eliminar os padrões de escrita por IA apontados pelos orientadores. Foco primeiro em `.agents/`, depois replicar para `.claude/`.

## Constraints
- Nada de novo gate bloqueante de escrita: checks determinísticos são advisory e alimentam a Dimensão 5 do academic-reviewer; o veredito Accept já exige writing alto.
- Foco inicial em `.agents/`; replicação `.claude/` é etapa posterior.
- A proposta de melhoria deve ser revisada por outro agente (modelo deepseek v4 pro) antes do plano final.
- O plano deve descrever: o que o usuário pediu, ideia e motivação, e os artefatos (diretórios/arquivos específicos).

## Key decisions
- Decision: Criar skill nova `academic-writing-reviewer` (auditoria read-only focada na prosa). Reason: o revisor de escrita é papel próprio (worker/critic), separado do academic-reviewer 6-D. Alternative considered: aprofundar só a Dimensão 5 — rejeitado porque o relatório concentra críticas de escrita e uma skill dedicada dá granularidade e scripts próprios; ela ainda alimenta a Dimensão 5.
- Decision: Refazer 3 skills + atualizar agentes de orquestração (writing-agent.md, review-agent.md) com o loop escrever → revisor de escrita → humanizar. Reason: skills isoladas sem orquestração não mudam o pipeline real. Alternative considered: só as skills — rejeitado.
- Decision: EN + PT-BR como listas fortes de marcadores; FI em referência separada sob demanda. Reason: reunião/relatório são PT-BR; material empírico (Kobak, Wikipédia) é EN. Alternative considered: PT-BR only — rejeitado por perder a base empírica EN.
- Decision: Checks de escrita advisory (backstop determinístico), sem novo gate bloqueante. Reason: fluxo atual de gates G4/G4.5 já decide; burocracia extra por seção atrapalha. Alternative considered: gate G5 bloqueante — rejeitado pelo usuário.

## Surfaced assumptions
- Os scripts determinísticos existentes (deai_check.py etc.) devem ser reaproveitados e estendidos, não reescritos do zero.
- A calibração de voz do autor (style guide curado) é parte da solução do problema "IA absorveu o tom imaturo do autor" — vira artefato opcional `resources/style-guide.md`.
- A humanização passa a rodar por seção e no final (lição do Paper-OS), não só no fim.

## Open questions
- Nenhuma bloqueante para o plano.

## Out of scope
- Alterar gates G4/G4.5/formato.
- Replicar para `.claude/` nesta etapa.
- Mudar academic-prd, academic-plan, academic-researcher e demais skills.
