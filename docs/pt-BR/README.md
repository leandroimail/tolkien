# Central de Documentação do tolkien

> **Idioma / Language:** Português | [English Version (docs/)](../README.md)

Bem-vindo à documentação oficial do **Academic Article Production Multi-Agent System (tolkien)**. Esta central está organizada segundo o framework Diataxis e as melhores práticas de documentação técnica, separando referências técnicas, tutoriais guiados, arquitetura e especificações de sistema.

---

## 🗺️ Mapa de Navegação da Documentação

### 1. Documentação Técnica e Arquitetura
Para desenvolvedores, pesquisadores e engenheiros de agentes que precisam compreender a estrutura interna, componentes, fluxos de dados e invariantes:
- 📘 **Documentação Técnica de Arquitetura**: [Versão em Português](tecnica/arquitetura.md) | [English Version](../technical/architecture.md)
- 📐 **Visão Geral de Arquitetura de Sistema**: [Versão em Português](ARCHITECTURE.md) | [English Version](../ARCHITECTURE.md)
- 📖 **Dicionário de Conceitos e Definições**: [Versão em Português](DEFINITIONS.md) | [English Version](../DEFINITIONS.md)

### 2. Tutoriais e Guias de Execução
Para novos usuários e pesquisadores que desejam aprender a utilizar o sistema na prática:
- 🚀 **Tutorial: Produzindo um Artigo do Zero**: [Versão em Português](tutoriais/produzindo-artigo-do-zero.md) | [English Version](../tutorials/producing-article-from-scratch.md)
- ⚡ **Guia Rápido (Quickstart)**: [Versão em Português](QUICKSTART.md) | [English Version](../QUICKSTART.md)
- 🎓 **Tutorial Geral e Filosofia Operacional**: [Versão em Português](TUTORIAL.md) | [English Version](../TUTORIAL.md)

### 3. Especificações Formais e Requisitos (PRD)
Para histórico, fundamentos metodológicos do Academic SDD e requisitos de engenharia:
- 📋 **PRD Técnico v2.0**: [Versão em Português](PRD-academic-multiagent-system.md) | [English Version](../PRD-academic-multiagent-system.md)

---

## 🏛️ Os 7 Gates de Qualidade

Todo artigo produzido no tolkien deve atender aos seguintes checkpoints não-negociáveis:

| Gate | Fase | Validador | Critério de Aprovação |
|---|:---:|---|---|
| **Gate G1** | 0 | Humano | Assinatura e aprovação formal do `prd.md`. |
| **Gate G2** | 1 | Humano | Aprovação do plano de execução e tarefas em `plan.md`. |
| **Gate G3** | 3 | Humano | Aprovação da arquitetura de seções e das *Scope Cards*. |
| **Gate G4** | 5 | Determinístico (`citation_gate.py`) | Zero citações órfãs no texto e zero entradas faltantes no `.bib`. |
| **Gate G4.5** | 5 | Determinístico (`data_congruence_gate.py`) | 100% de congruência entre números da prosa e tabelas/figuras. |
| **Gate G5** | 7 | Painel 6-D (`review-agent`) | Nota $\ge 7.0/10$, 0 erros críticos do Advogado do Diabo. |
| **Output Format Gate** | 8 | Determinístico (`validate_formats.py`) | Compilação e integridade sem erros de sintaxe (Markdown/LaTeX/DOCX). |
