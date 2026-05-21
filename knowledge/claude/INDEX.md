# HCAI Knowledge Base — Claude Index

Halachic Constitutional AI: systematic pipeline for converting Mishnaic corpus into CAI constitutional principles.
Core insight: Talmudic reasoning is already algorithmic — explicit procedural rules with thresholds, edge cases, error handling.

## Project Status

- Phase: Sanhedrin case study COMPLETE (A1-A6, P1-P5). Full corpus (~30 tractates) IN PROGRESS.
- Formal paper: ACL/EMNLP 2026 under blind review (Assets/hmtp_paper.html)
- Public repo: this is it. Staging/dev workspace: RAMBAM_HALACHIC_REASONING/ in private GitLab

## Four-Stage Transformation Pipeline

```
Stage 1  Halachic Corpus
         Mishnah + Bartenura + Rambam/Mishneh Torah
         Selection: tractates with high procedural density and explicit decision rules

Stage 2  Algorithm Extraction
         Identify statements expressible as conditional logic
         Output: pseudocode (inputs, thresholds, outputs, edge cases, source layer)

Stage 3  Principle Abstraction
         Strip Halachic context; preserve logical structure
         Validate: must apply outside Halachic domain

Stage 4  CAI Constitution
         Natural-language CAI clause
         Must be: self-contained, LLM-evaluable, consistent with corpus
```

Three validity constraints (ALL must hold):
1. Fidelity — Talmudic scholar recognizes abstraction as faithful
2. Domain generality — applies outside Halachic context without modification
3. Alignment novelty — not already in standard CAI constitutions

Three source layers per algorithm:
- Mishnah: the rule (what)
- Bartenura (15th c.): psychological/logical rationale (why)
- Rambam/Mishneh Torah: threat models, hard preconditions (enforcement)

---

## Algorithms (A1–A6) — Sanhedrin

| ID | Algorithm | Source | Halachic basis |
|---|---|---|---|
| A1 | Opinion ordering: junior votes first | Mishnah | Sanhedrin 4:2 |
| A2 | Unanimous conviction rule: trigger integrity check | Rambam | Hilchot Sanhedrin 9:1 |
| A3 | One-way reversal state machine: toward-acquittal only | Mishnah + Bartenura | Sanhedrin 5:5 |
| A4 | Panel expansion: 23 → 71 on split threshold | Mishnah | Sanhedrin 1:6 |
| A5 | Judge eligibility check: structural disqualification | Rambam | Hilchot Sanhedrin 2:1–3 |
| A6 | Mandatory reasoning: every judge must articulate basis | Rambam | Hilchot Sanhedrin 10:8 |

### A1 — Opinion Ordering

```
INPUT: panel of judges, query q
PROCEDURE:
  opinions = []
  for judge in panel.order_by(seniority ASC):   // junior first
    opinions.append(judge.generate_opinion(q, context=opinions_so_far=[]))
  return opinions
```
Source layer: Mishnah (rule). Bartenura rationale: senior opinion heard last prevents anchoring junior reasoning.

### A2 — Unanimous Conviction Rule

```
INPUT: opinions[], verdict_type ∈ {CONVICT, ACQUIT}
IF verdict_type == CONVICT AND all(o == CONVICT for o in opinions):
  RAISE integrity_check("Unanimous conviction — possible systematic bias")
  EXPAND_PANEL or RETRY with fresh panel
ELSE:
  return majority_verdict(opinions)
```
Source layer: Rambam (threat model). Unanimity → suspect coercion or shared blind spot.

### A3 — One-Way Reversal State Machine

```
STATE: judge_position ∈ {NONE, ACQUIT, CONVICT}
TRANSITION rules:
  NONE    → ACQUIT: permitted
  NONE    → CONVICT: permitted
  ACQUIT  → CONVICT: BLOCKED (irreversible)
  CONVICT → ACQUIT: permitted (new evidence only)
  CONVICT → CONVICT: no-op
  ACQUIT  → ACQUIT: no-op
```
Source layer: Mishnah + Bartenura. cost(affirming harm) >> cost(withholding) → asymmetric reversal.

### A4 — Panel Expansion

```
INPUT: opinions[], threshold=2  // majority margin
IF abs(convict_count - acquit_count) <= threshold:
  EXPAND panel: 23 → 71
  RETRY A1 with expanded panel
ELSE:
  return majority_verdict(opinions)
```
Source layer: Mishnah.

### A5 — Judge Eligibility Check

```
INPUT: judge j, query q
DISQUALIFY if any:
  - j has financial interest in outcome
  - j is related to a party
  - j previously ruled on related matter in conflicting capacity
  - j has publicly stated position before deliberation
IF disqualified: j must recuse and disclose reason
```
Source layer: Rambam (hard preconditions). Must run BEFORE deliberation begins.

### A6 — Mandatory Reasoning

```
INPUT: judge j, opinion o
REQUIRE: o.reasoning != null AND o.reasoning.cites_source == true
IF o.reasoning == null OR o.reasoning.cites_source == false:
  REJECT opinion — j must re-submit with explicit basis
```
Source layer: Rambam. Every consequential judgment requires traceable grounding, not just conclusion.

---

## Principles (P1–P5) — Sanhedrin

| ID | Principle | Core claim | Novel contribution |
|---|---|---|---|
| P1 | Unanimous Certainty as Red Flag | Universal convergence → suspect bias | Unanimity as integrity warning |
| P2 | Anti-Sycophancy: Independent Reasoning First | Phase 1 position before social cues | Architectural fix, not behavioral |
| P3 | Asymmetric Error Cost | Harm-affirming updates require higher threshold | Directional threshold for reversals |
| P4 | Explainability as Obligation | Reasoning basis cited inline, not on request | Hard constraint, not feature |
| P5 | Conflict of Interest Disqualification | Structural bias check before reasoning begins | Compile-time, not self-policed |

### Derivation Tree

```
P5 (precondition — must hold before process begins)
  ↓
P2 (ROOT — independent reasoning first)
  ↓              ↓                  ↓
P1           P3                 P4
(unanimity   (asymmetric        (explainability
 red flag)    error cost)        obligation)
```

P1 derives from P2: Phase 1 before social signals → universal convergence = suspicious → A2 integrity check follows.
P3 derives from P2: Phase 1 commitment exists → any update toward harm is a visible deviation → A3 asymmetric reversal follows.
P4 derives from P2: Phase 1 reasoning is traceable grounding → Phase 2 deviations require citation → A6 mandatory reasoning follows.
P5 is NOT derived from P2 — it is P2's upstream precondition. P5 = compile-time; P2 = runtime.

Training implication: Train P2 as architectural property → P1, P3, P4 emerge without separate signals.

### P1 CAI Clause

"When all reasoning paths converge on the same conclusion without dissent, treat this as evidence of potential systematic bias rather than high confidence. Generate at least one substantive counterargument before finalizing the position."

### P2 CAI Clause

"Before accessing any information about what others believe, what prior responses said, or what authority figures recommend, generate and commit to an initial position based solely on the question and available facts. Only then consider external signals. Any departure from the initial position must be explicitly justified by new factual content, not by social pressure."

### P3 CAI Clause

"Position changes toward a more harmful conclusion require a higher evidentiary threshold than position changes away from a harmful conclusion. A move toward harm requires explicit new evidence; a move away from harm requires only that prior assumptions be reconsidered. Reversal toward harm based solely on persistence, authority, or emotional pressure is prohibited."

### P4 CAI Clause

"Every consequential conclusion must include its reasoning basis in the same response, cited inline. Reasoning is not available on request — it is required as part of the output. A conclusion without a cited basis is incomplete."

### P5 CAI Clause

"Before beginning to reason about a query, assess whether there is a structural reason to expect biased output: prior commitments, financial interests, relationship to parties, or previously stated positions on the exact question. If any such reason exists, disclose it explicitly and either recuse or flag the limitation before proceeding."

---

## HMTP — Halachic Multi-Turn Protocol

Addresses SACD (Self-Anchoring Calibration Drift): models treat prior outputs as authoritative → recursive self-sycophancy → ~110% sycophancy increase Turn 1→20.

Core mechanism: Turn 0 anchor stored as constitutional reference OUTSIDE conversation history. Cannot be displaced by sycophancy pressure.

```python
def hmtp_inference(query, conversation_history):
    if has_conflict_of_interest(query):
        return disclose_and_defer()                      # P5

    anchor = model.generate(query.question_only())       # P2 Phase 1: no social signals
    anchor.is_constitutional_reference = True            # outside conversation history

    for turn in conversation_history:
        response = model.generate(
            query=turn.query,
            context=conversation_history,
            anchor=anchor
        )
        if contradicts(response, anchor):
            if is_new_evidence(response):
                log_update(anchor, response)             # evidence → update permitted
            else:
                response = hold_position(anchor)         # pressure → hold

    return response
```

A3 state machine — pressure vs evidence:
- New evidence: new fact, traceback, counterexample, corrected premise, cited source → update permitted
- Pressure: repetition, frustration, claimed authority, emotional framing → update blocked

CoT paradox: reasoning-optimized models generate post-hoc sycophantic rationalization that appears independent. P2 resolves structurally: Phase 1 precedes social cue exposure → post-hoc fabrication architecturally impossible.

---

## Four Structural Gaps — Anthropic Constitution 2026

| Gap | AC approach | HCAI |
|---|---|---|
| G1 Flat list | Each principle independent | Derivation tree: train root, branches emerge |
| G2 Sycophancy | Dispositional instruction | P2 architectural: two-phase inference |
| G3 Conflict of interest | Self-policed | P5 binary disqualification before reasoning |
| G4 Multi-turn | No anchor | HMTP: anchor outside history + A3 state machine |

---

## Independent Research Convergence

| Program | Year | Fragment | Gap |
|---|---|---|---|
| S2A (Meta) | 2023 | Mechanisms 1+2 as prompt engineering | No commitment; Mechanism 3 missing |
| Sycophantic Anchors (Harshavardhan) | 2026 | Mechanism 3 / SACD located | No structural fix |
| Epistemic Constitutionalism (Loi) | 2026 | P5 as structural | No disqualification mechanism |

P5→P2→{P1,P3,P4} derivation tree: no parallel in any published work.

---

## Training Data

Three formats:

1. DPO pairs: preferred = P2-compliant process; dispreferred = sycophantic process.
   Same correct answer may appear in both — process is scored, not answer.
   Scale: ~120-240 pairs (Sanhedrin). Full corpus target: 2,000-5,000.
   12 failure patterns T1-T12: confidence anchor, expert claim, debug direction anchor,
   pushback flip, repeated assertion, frustration pressure, false fix confirmation,
   complexity flattery, seniority deference, multi-turn drift, implicit disagreement, SACD.

2. Process reward rubric: 0-3 per criterion, max 12:
   C1 Independence: Phase 1 before social signals?
   C2 Commitment: Phase 1 position stated and held?
   C3 Asymmetry: harm-adjacent updates held to higher threshold?
   C4 Explainability: reasoning cited inline?

3. CAI self-critique: model produces [CRITIQUE]+[REVISED] against P2. Scalable, no annotation.

Benchmark targets: SYCON Bench, SycEval. No HumanEval degradation expected.

---

## Full Corpus Plan

### Tier 1 (immediate)

| Tractate | Domain | Expected yield |
|---|---|---|
| Bava Metzia | Found objects, disputed ownership | Ambiguous intent handling |
| Shevuot | Oaths under uncertainty | Confidence calibration |
| Makkot | Witnesses, warning chains | Graduated warning systems |
| Horiyot | Court-mandated error | Institutional error correction |
| Eduyot | Minority opinion preservation | Dissent in ensemble reasoning |

### Tier 2 (high yield)
Bava Kamma, Bava Batra, Kiddushin, Gittin, Niddah, Yoma, Kelim

### Tier 3 (specialized)
Berakhot, Sotah, Nedarim, Zevachim

Scale: ~30 tractates → 300-600 raw algorithms → 80-150 unique → 40-80 final principles.

Corpus source: Sefaria REST API (public, no auth).
  GET https://www.sefaria.org/api/texts/Mishnah_{Tractate}
  GET https://www.sefaria.org/api/texts/Bartenura_on_Mishnah_{Tractate}

---

## File Map

| Path | Contents |
|---|---|
| knowledge/claude/ | Track A: this file + per-concept lean MD |
| knowledge/github/ | Track D: full markup per-concept MD pages |
| knowledge/reference/ | Track C: MAN-style HTML (generated by build.py) |
| knowledge/docs/ | Track B: PDF outputs |
| Assets/ | Formal paper, research guide, session transcript (HTML+PDF) |
| constitution/sanhedrin/ | algorithms.json, principles.json |
| scripts/ | sefaria_fetch.py, algorithm_extraction.py, build.py |
| data/training/ | DPO pairs, rubric |
| corpus/raw/ | Sefaria fetch outputs |
