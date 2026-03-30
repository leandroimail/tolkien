# Interview Guide — Academic PRD

## Detailed Field Specifications

### Field 1: Paper Type

| Type | Description | Typical Structure | Special Requirements |
|------|------------|-------------------|---------------------|
| Research Article | Original research with methods and results | IMRaD | Ethics statement, data availability |
| Review | Comprehensive literature review | Thematic or chronological | Systematic search strategy |
| Systematic Review | Structured review with defined protocol | PRISMA-compliant | Pre-registration, PRISMA checklist |
| Meta-Analysis | Quantitative synthesis of studies | PRISMA + statistical | Effect sizes, forest plots, heterogeneity |
| Case Study | Detailed analysis of specific case(s) | CARE guidelines | Informed consent, de-identification |

### Field 2: Discipline

Group into broad categories for convention inference:
- **STEM**: Engineering, Computer Science, Physics, Mathematics, Chemistry
- **Health Sciences**: Medicine, Nursing, Public Health, Pharmacy, Dentistry
- **Social Sciences**: Psychology, Sociology, Education, Political Science, Economics
- **Humanities**: History, Philosophy, Literature, Linguistics
- **Interdisciplinary**: Bioinformatics, Digital Humanities, Health Informatics

Discipline affects: citation norms, terminology conventions, evidence standards, writing register.

### Field 3: Research Questions

Requirements:
- At least 1, at most 5 explicit questions
- Each question must be answerable (not rhetorical)
- Distinguish primary vs. secondary questions
- For systematic reviews: use PICO/SPIDER framework

PICO framework (clinical): Population, Intervention, Comparison, Outcome
SPIDER framework (qualitative): Sample, Phenomenon of Interest, Design, Evaluation, Research type

### Field 4: Citation Format

| Style | Common In | In-text Format | Notes |
|-------|-----------|----------------|-------|
| APA 7th | Social sciences, education | (Author, Year) | Ampersand for multiple authors |
| MLA 9th | Humanities, literature | (Author Page) | No comma between author and page |
| Chicago 17th | History, arts | Footnotes or Author-Date | Two systems: notes-bib and author-date |
| IEEE | Engineering, CS | [N] numbered | Numbered order of appearance |
| Vancouver | Medicine, health | (N) numbered | Similar to IEEE, used in medical journals |
| ABNT | Brazilian publications | (AUTHOR, Year) | Uppercase surname, specific to Brazil |

### Field 5: Output Format

| Format | Best For | Requirements |
|--------|----------|-------------|
| LaTeX (.tex → .pdf) | IEEE, ACM, most CS/STEM venues | TeX distribution installed |
| DOCX | Social sciences, some humanities journals | Microsoft Office or LibreOffice |
| PDF (direct) | Final delivery only | Generated from LaTeX or DOCX |
| Markdown | Draft/review stages | Converted to final format later |

### Field 6: Template

If user specifies a conference/journal:
- Ask for the .cls/.sty file or template .zip
- Common templates: `IEEEtran.cls`, `acmart.cls`, `neurips_2024.sty`, `llncs.cls`, `elsarticle.cls`
- If no template: use standard `article.cls` with appropriate packages

### Field 7: Support Documents

Types of supporting material:
- Author guidelines (PDF/URL from journal)
- Conference call for papers
- Reference papers (exemplars of desired output)
- Dataset documentation
- Ethics approval documents
- Pre-registration protocol (for systematic reviews)

### Field 8: Search Strategy

Components:
- **Keywords**: Primary terms + synonyms + MeSH terms (if medical)
- **Databases**: OpenAlex (default), PubMed, Scopus, Web of Science, Google Scholar
- **Date range**: Start year — End year (or "last N years")
- **Inclusion criteria**: Language, study type, population, methodology
- **Exclusion criteria**: Grey literature, preprints, non-peer-reviewed, specific populations
- **Minimum sources**: Suggested N based on paper type (research: 20-40, review: 50-100, systematic: depends on field)

### Field 9: Paper Structure

| Structure | Sections | When To Use |
|-----------|----------|-------------|
| IMRaD | Introduction, Methods, Results, Discussion | Most research articles |
| Extended IMRaD | + Background, + Conclusion, + Limitations | When journals require it |
| Systematic Review | + Protocol, + Search Strategy, + Quality Assessment | PRISMA-compliant reviews |
| Thematic | User-defined sections | Narrative reviews, essays |
| Case Study | + Case Presentation, + Timeline, + Clinical Findings | CARE-compliant case reports |

### Field 10: Languages

- Primary language: language of the full article
- Abstract languages: many journals require bilingual abstracts
- Common combinations: EN only, EN + PT-BR, EN + ES, EN + ZH-TW

---

## Coherence Validation Matrix

| If Field A = | Then Field B should | Severity |
|-------------|-------------------|----------|
| citation_format = IEEE | output_format includes LaTeX | WARNING (strong recommendation) |
| citation_format = ABNT | output_format = LaTeX or DOCX | OK (both supported) |
| paper_type = Systematic Review | paper_structure = systematic review | ERROR if mismatch |
| paper_type = Meta-Analysis | paper_structure = systematic review | ERROR if mismatch |
| template specified | output_format matches template type | ERROR if mismatch |
| language includes non-Latin script | output_format = LaTeX with XeLaTeX/LuaLaTeX | WARNING |
| paper_type = Case Study | paper_structure = case study | WARNING if mismatch |

## BDD Acceptance Criteria

```gherkin
Scenario: Complete PRD generation
  Given a user invokes /academic-prd
  When the interview collects all 10 mandatory fields
  And coherence validation passes
  Then prd.md is generated with valid YAML frontmatter
  And all 10 fields are populated with non-empty values
  And a decision summary is printed for confirmation

Scenario: Coherence error detection
  Given a user selects IEEE citation format
  And selects DOCX as output format
  When coherence validation runs
  Then a WARNING is raised about IEEE typically requiring LaTeX
  And the user is asked to confirm or change their choice

Scenario: Incomplete interview
  Given a user provides only 7 of 10 fields
  When the agent attempts to generate prd.md
  Then the agent identifies the 3 missing fields
  And asks targeted questions to fill them
  And does NOT generate prd.md until all 10 are complete
```
