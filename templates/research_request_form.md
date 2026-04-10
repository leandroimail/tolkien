# Research Initiation Form - tolkien

This form is designed to collect all the necessary information to start the academic article production pipeline (Phase 0: Academic PRD).

**Instructions for the User:** Fill out the fields below and paste this content into the chat with the Orchestrator Agent.

---

## 1. Basic Information
*   **Provisional Title:** [Insert title here]
*   **Paper Type:** [Research Article | Review | Systematic Review | Meta-analysis | Case Study]
*   **Field/Discipline:** [e.g., Computer Science, Medicine, Engineering, etc.]
*   **Target Language(s):** [e.g., English (Primary) + Abstract in Portuguese]
*   **Blind Review (Anonymization):** [Yes | No] (Set to 'Yes' for conferences requiring double-blind review)

## 2. Research Objectives and Questions
*   **General Objective:** [Describe what you intend to achieve]
*   **Primary Research Question (RQ1):** [Clear and direct question]
*   **Secondary Questions (Optional):**
    *   **RQ2:** [Additional question]
    *   **RQ3:** [Additional question]
*   **Seed Papers / Reference DOIs:** [List DOIs of key papers that serve as the foundation for this research]

## 3. Formatting and Output
*   **Citation Style:** [APA | IEEE | ABNT | Vancouver | Chicago | MLA]
*   **Final Output Format:** [LaTeX (Recommended) | DOCX | PDF | Markdown]
*   **Specific Template:** [e.g., IEEE Conference, ACM acmart, NeurIPS, or path to .cls/.sty file]
*   **Target Venue:** [e.g., ICRA 2025, Nature, Journal of AI]

## 4. Research Strategy and Documentation
*   **Keywords:** [Comma-separated list]
*   **Databases:** [OpenAlex (Default), Google Scholar, Scopus, etc.]
*   **Inclusion/Exclusion Criteria:** [Which articles should or should not be considered?]
*   **Support Documents:** [List URLs or file paths for reference papers, guidelines, or templates the agent should read]
*   **Submission Deadline:** [YYYY-MM-DD] (If applicable)

## 5. Structure and Research Plan
*   **Paper Structure:** [IMRaD (Intro, Methods, Results, Discussion) | Thematic | Systematic Review Structure]
*   **Narrative Voice:** [1st Person Plural (We) | 3rd Person (Passive Voice) | 1st Person Singular (I)]
*   **Time Scope:** [e.g., Articles published between 2015 and 2024]
*   **Minimum Sources:** [Approximate number of expected references]
*   **Data Availability:** [I have a Dataset (CSV/XLSX) | Agent should search for public data | Purely theoretical research]
*   **Expected Visuals:** [Describe planned figures or diagrams, e.g., Architecture Diagram, PRISMA Flowchart, Performance Bars]

---

**Note for the Agent:** 
*   Upon receiving this form, use the `academic-prd` skill to process the information and generate the `prd.md`.
*   If research questions are vague, use the **Socratic Mode** of the `academic-researcher` skill to refine them before proceeding.
*   Once the PRD is approved, proceed to the `academic-plan` skill to detail the execution roadmap in `plan.md`.
