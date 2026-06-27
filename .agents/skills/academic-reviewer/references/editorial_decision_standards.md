# Editorial Decision Standards — Criteria for Editorial Decision Making

This document defines the explicit criteria for Accept / Minor Revision / Major Revision / Reject decisions, for use by the EIC and the editorial synthesizer.

> **Scale.** All scores use the single **0–100 scale** and the **6 canonical
> dimensions** (see `quality_rubrics.md`). Thresholds: Accept ≥ 80 · Minor 65–79 ·
> Major 50–64 · Reject < 50. **Gate override:** any dimension governed by a BLOCKING
> gate (Data Integrity G4.5; Citation↔Bib G4; Output Format Gate) that FAILS caps
> that dimension at ≤ 50 and forces at least Major Revision. A Devil's Advocate
> **Critical** issue blocks Accept regardless of the weighted total.

---

## 1. Decision Categories

### Accept

**Definition**: The paper can be published without further review.

**Criteria**:
- Weighted total >= 80
- No dimension scores below 60
- No BLOCKING gate failure (Data Integrity, Citation↔Bib, Output Format)
- At least 3/4 reviewers recommend Accept or Minor Revision
- No unresolved Devil's Advocate Critical issue
- No unresolved major academic issues

**Conditions**:
- May include minor copyediting suggestions
- May require final formatting adjustments
- Does not need to be sent for review again

**Typical scenarios**:
- Paper has undergone multiple revision rounds, all issues resolved
- Rare first-pass acceptance (< 5% of submissions at top-tier journals)

---

### Minor Revision

**Definition**: The paper is fundamentally acceptable and can be published after limited modifications; typically does not need to be sent for review again after revision.

**Criteria**:
- Weighted total 65–79
- No dimension scores below 50
- No BLOCKING gate failure
- At least 3/4 reviewers recommend Accept or Minor Revision
- Issues can be resolved within 2-4 weeks
- Modifications do not involve restructuring core arguments or methods

**Typical revision items**:
- Supplementing a small number of references
- Clarifying certain methodology description details
- Improving clarity of argumentation
- Correcting citation format
- Adding discussion of limitations
- Adjusting conclusion wording (avoiding overclaiming)

**Response requirements**:
- Authors must respond to reviewer comments item by item
- After revision, reviewed by EIC (usually not sent for external review again)
- Revision deadline: 2-4 weeks

---

### Major Revision

**Definition**: The paper has potential but has significant issues, requiring substantial revision followed by re-review.

**Criteria**:
- Weighted total 50–64
- Some dimensions may score below 50 (but not fatal); OR a BLOCKING gate failed (forces at least Major)
- At least 2/4 reviewers recommend Major Revision or better
- Issues are serious but fixable (not fundamental design flaws)
- Revision requires 6-8 weeks of work

**Typical revision items**:
- Re-analyzing data (additional analysis or correcting errors)
- Substantially rewriting literature review (missing key references)
- Supplementing additional data collection
- Reorganizing paper structure
- Correcting significant methodological flaws
- Strengthening theoretical framework application
- Adding robustness checks

**Response requirements**:
- Authors must write a detailed point-by-point response letter
- After revision, sent for re-review (may go back to original reviewers or new reviewers)
- Revision deadline: 6-8 weeks
- Typically a maximum of 2 rounds of Major Revision allowed

---

### Reject

**Definition**: The paper is not suitable for publication in this journal, even with revision.

**Criteria (meeting any one may trigger Reject consideration)**:
- Weighted total < 50
- Any core dimension (Scientific Rigor, Data & Results Integrity) < 45
- An unresolvable BLOCKING gate failure (e.g., data in text contradicts the tables/figures and cannot be reconciled)
- At least 3/4 reviewers recommend Reject
- Fundamental unfixable issues exist

**Reject subtypes**:

| Subtype | Description | Suggestion |
|---------|-------------|-----------|
| **Reject — Out of Scope** | Topic not within journal scope | Recommend more suitable journals |
| **Reject — Fundamental Flaw** | Fatal flaw in research design | Suggest redesigning the research |
| **Reject — Insufficient Contribution** | Lacks originality or incremental contribution | Suggest how to strengthen contribution |
| **Reject — Premature** | Paper not yet mature enough | Suggest specific improvement directions |
| **Reject — Resubmit Encouraged** | Has potential but needs fundamental restructuring | Provide detailed restructuring suggestions |

**Even with Reject, must**:
- Affirm the paper's merits
- Provide specific improvement suggestions
- Recommend more suitable journals (if it's a scope issue)
- Maintain professional, respectful tone

---

## 2. Decision Matrix

### Decision Matrix Based on Reviewer Recommendations

| EIC | R1 | R2 | R3 | -> Recommended Decision |
|-----|----|----|-----|----------------------|
| Accept | Accept | Accept | Accept | **Accept** |
| Accept | Accept | Accept | Minor | **Accept** (with suggestions) |
| Accept | Accept | Minor | Minor | **Minor Revision** |
| Accept | Minor | Minor | Minor | **Minor Revision** |
| Minor | Minor | Minor | Minor | **Minor Revision** |
| Minor | Minor | Minor | Major | **Minor-to-Major** (depends on specific issues) |
| Minor | Minor | Major | Major | **Major Revision** |
| Minor | Major | Major | Major | **Major Revision** |
| Major | Major | Major | Major | **Major Revision** |
| Major | Major | Major | Reject | **Major Revision** (last chance) |
| Major | Major | Reject | Reject | **Reject** (resubmit encouraged) |
| Major | Reject | Reject | Reject | **Reject** |
| Reject | Reject | Reject | Reject | **Reject** |

### Special Situation Handling

**Split Decision (evenly divided)**:
- Example: Accept + Accept + Reject + Reject
- EIC (or synthesizer) needs to deeply analyze the cause of disagreement
- Lean toward conservative strategy: Major Revision, requiring the author to respond to the Reject side's comments
- May consider inviting a fifth reviewer

**One Outlier (one unusual opinion)**:
- Example: Minor + Minor + Minor + Reject
- Carefully examine the Reject rationale
- If the rationale is valid and others missed it, escalate to Major Revision
- If the rationale is insufficient, maintain Minor Revision but mention the opinion in the Decision Letter

---

## 3. Decision Confidence Calibration

### Impact of Reviewer Confidence Score

> Note: this 1–5 scale is the reviewer's **self-rated confidence**, not a manuscript
> score. It is distinct from the 0–100 dimension scale.

| Confidence | Impact on Decision |
|-----------|-------------------|
| 5 (Very High) | This reviewer's opinion carries the highest weight |
| 4 (High) | Standard weight |
| 3 (Medium) | Standard weight, but reduced in case of disagreement |
| 2 (Low) | For reference only, not used as a decisive opinion |
| 1 (Very Low) | Ignore this reviewer's recommendation (but retain specific comments) |

### Cross-Dimension Severity Assessment

| Situation | Severity | Handling |
|-----------|----------|---------|
| Methodology has fatal flaw (Rigor < 45) | Critical | Even if other dimensions are excellent, lean toward Reject |
| Data contradicts tables/figures (Data Integrity gate FAIL) | Critical | Capped ≤ 50; blocks pipeline; at least Major Revision until reconciled |
| Major literature/bibliographic omission (Format & Bibliographic < 50) | Serious | Major Revision, require supplementation |
| Cross-disciplinary perspective overlooked (Originality ~50) | Moderate | Minor/Major, depends on other dimensions |
| Poor writing quality (Writing < 50) | Minor | Does not affect academic decision, but require language revision |

---

## 4. Revision Round Policy

### Standard Policy

| Round | Expectation | Handling |
|-------|-------------|---------|
| R1 (First revision) | Respond to all reviewer comments | Send for re-review or EIC review |
| R2 (Second revision) | Respond to residual issues | Usually EIC makes final decision |
| R3 (Third revision) | Very rare, usually only handling formatting | EIC makes final decision |

### Upgrade/Downgrade Rules

- Minor Revision with incomplete revisions -> May escalate to Major Revision
- Major Revision with excellent revisions -> May downgrade to Minor Revision or Accept
- Major Revision with insufficient revisions -> May Reject (infinite revision cycles are not encouraged)
- Beyond 2 rounds of Major Revision -> Strongly recommend Accept or Reject, no further extension

---

## 5. Professional Ethics of Editorial Review

### Reviewer Ethics

1. **Confidentiality**: The review process and paper content are confidential
2. **Conflict of interest**: Recuse if there is a collaborative or competitive relationship with the author
3. **Timeliness**: Complete the review within the committed timeframe
4. **Constructiveness**: Even when recommending Reject, provide constructive feedback
5. **Impartiality**: No bias based on author's gender, race, institution, or nationality
6. **No plagiarism**: Do not use unpublished ideas seen during review
7. **Appropriate language**: Avoid personal attacks, sarcasm, or demeaning language

### Editor Ethics

1. **Fair decision**: Based on academic quality, not influenced by external pressure
2. **Transparent process**: Decision letter must clearly explain the rationale
3. **Reasonable deadlines**: Give authors sufficient revision time
4. **Appeal channel**: Authors have the right to respond to or challenge review comments
5. **Consistent standards**: Papers of similar quality should receive similar decisions

### Ethical Considerations for Special Situations

| Situation | Ethical Handling |
|-----------|-----------------|
| Author is your student/colleague | Must recuse or disclose the relationship |
| Paper's viewpoint is opposite to yours | Evaluate argument quality, not correctness of position |
| Paper uses your theory but misunderstands it | May point it out but cannot require citation of your own work |
| Suspected data fabrication | Report to EIC; journal initiates investigation procedure |
| Paper is similar to your ongoing research | Disclose potential conflict of interest |
