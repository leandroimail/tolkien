# tolkien Documentation Center

> **Language / Idioma:** English | [Versão em Português (docs/pt-BR/)](pt-BR/README.md)

Welcome to the official documentation for the **Academic Article Production Multi-Agent System (tolkien)**. This documentation hub follows the Diataxis framework and technical documentation best practices, separating technical references, guided tutorials, architectural overviews, and formal system specifications.

---

## 🗺️ Documentation Navigation Map

### 1. Technical Documentation & Architecture
For developers, researchers, and AI agent engineers who need to understand internal structures, components, data flows, and invariants:
- 📘 **Technical Architecture Deep-Dive**: [English Version](technical/architecture.md) | [Versão em Português](pt-BR/tecnica/arquitetura.md)
- 📐 **System Architecture Overview**: [English Version](ARCHITECTURE.md) | [Versão em Português](pt-BR/ARCHITECTURE.md)
- 📖 **Definitions & Concepts Glossary**: [English Version](DEFINITIONS.md) | [Versão em Português](pt-BR/DEFINITIONS.md)

### 2. Tutorials & Execution Guides
For new users and researchers who want to learn how to operate the system in practice:
- 🚀 **Tutorial: Producing an Article from Scratch**: [English Version](tutorials/producing-article-from-scratch.md) | [Versão em Português](pt-BR/tutoriais/produzindo-artigo-do-zero.md)
- ⚡ **Quickstart Guide**: [English Version](QUICKSTART.md) | [Versão em Português](pt-BR/QUICKSTART.md)
- 🎓 **General Tutorial & Operating Philosophy**: [English Version](TUTORIAL.md) | [Versão em Português](pt-BR/TUTORIAL.md)

### 3. Formal Specifications & Requirements (PRD)
For history, methodological foundations of Academic SDD, and engineering requirements:
- 📋 **System PRD v2.0**: [English Version](PRD-academic-multiagent-system.md) | [Versão em Português](pt-BR/PRD-academic-multiagent-system.md)

---

## 🏛️ The 7 Quality Gates

Every manuscript produced in tolkien must clear the following non-negotiable checkpoints:

| Gate | Phase | Validator | Approval Criterion |
|---|:---:|---|---|
| **Gate G1** | 0 | Human | Formal review and approval of `prd.md`. |
| **Gate G2** | 1 | Human | Approval of execution plan and milestones in `plan.md`. |
| **Gate G3** | 3 | Human | Approval of section architecture, word counts, and *Scope Cards*. |
| **Gate G4** | 5 | Deterministic (`citation_gate.py`) | Zero orphan in-text citations and zero missing `.bib` entries. |
| **Gate G4.5** | 5.5 | Deterministic (`data_congruence_gate.py`) | 100% mathematical congruence between prose numbers and tables/figures. |
| **Gate G5** | 7 | 6-D Panel (`review-agent`) | Composite score $\ge 65/100$, 0 critical issues from Devil's Advocate. |
| **Output Format Gate** | 8 | Deterministic (`validate_formats.py`) | Clean compilation and structural integrity (Markdown / LaTeX / DOCX). |
