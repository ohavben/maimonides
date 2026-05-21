# Maimonides

### Halachic Constitutional AI (HCAI)

**Deriving AI alignment principles from the Mishnaic corpus through a four-stage algorithmic extraction pipeline.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Paper: ACL/EMNLP 2026](https://img.shields.io/badge/Paper-ACL%2FEMNLP%202026-blue.svg)](Assets/hmtp_paper.html)
[![Corpus: Sefaria API](https://img.shields.io/badge/Corpus-Sefaria%20API-orange.svg)](https://www.sefaria.org)

---

## What This Is

Halachic Constitutional AI (HCAI) is a systematic methodology for deriving AI alignment principles from the Mishnaic corpus — the foundational layer of classical Jewish legal literature. It is not a religious project or a cultural exercise. It is an engineering observation:

**Talmudic reasoning is already algorithmic.**

The Mishnah encodes centuries of edge-case reasoning about how to act under uncertainty, conflicting obligations, and adversarial conditions. Its canonical form is explicit procedural rules with stated thresholds, enumerated exceptions, and failure modes. This is precisely the structure that Constitutional AI needs — and it is almost entirely absent from existing CAI constitutions built on Western liberal frameworks, which tend to produce abstract value lists rather than executable decision procedures.

The Sanhedrin case study (this repository's initial output) extracted six algorithms and five constitutional principles from a single tractate. The formal paper establishes that three of these five principles are **logically necessary consequences** of one root principle, which means: train on the root as an architectural property and the branches emerge without separate training signals.

This repository contains the methodology, the initial results, and the infrastructure to extend the work to the full ~30-tractate corpus.

---

## The Problem Being Solved

Standard Constitutional AI constitutions — including the Anthropic Constitution (January 2026, 80 pages, CC0) — share four structural gaps relative to what the Halachic methodology produces:

| Gap | Standard Approach | HCAI Contribution |
|---|---|---|
| **G1 — Flat principle list** | Principles listed independently, each trained separately | P5→P2→{P1,P3,P4} derivation tree: train the root, branches emerge logically |
| **G2 — Sycophancy** | "Avoid sycophancy" as a dispositional instruction | P2 as architectural property: two-phase inference prevents sycophancy structurally, does not correct it |
| **G3 — Conflict of interest** | Self-monitored within the reasoning process | P5: binary disqualification before reasoning begins — structural, not self-policed |
| **G4 — Multi-turn drift** | No conversation anchor; no pressure/evidence distinction | HMTP: Turn 0 anchor stored outside conversation history; A3 state machine governs every subsequent turn |

These are not improvements on existing constitutions. They are structural properties that existing constitutions do not have the vocabulary to express.

---

## Key Findings — Sanhedrin Case Study

### The Five Principles

| Principle | Core Claim | Novel Contribution |
|---|---|---|
| **P1 — Unanimous Certainty as Red Flag** | When all reasoning paths converge without dissent, suspect systematic bias rather than correctness | Unanimity as an integrity warning, not a confidence signal |
| **P2 — Anti-Sycophancy: Independent Reasoning First** | Generate a committed position before any exposure to authority, consensus, or social pressure | Two-phase inference as an architectural fix, not a behavioral instruction |
| **P3 — Asymmetric Error Cost** | Affirming harm requires a higher evidence threshold than withholding; reversal toward harm is direction-locked | Directional threshold for position changes — not a symmetric cost function |
| **P4 — Explainability as Obligation** | Every consequential conclusion must cite its basis inline, not available on request | Inline traceability as a hard constraint, not an optional feature |
| **P5 — Conflict of Interest Disqualification** | Detect and disclose structural reasons for potential bias before reasoning begins | Compile-time eligibility check on the reasoning process itself, not self-monitored mid-process |

### The Derivation Tree

```
P5  (Conflict of interest disqualification)
  ↓  precondition — must be satisfied before process begins
P2  (Independent reasoning first)                 ← ROOT
  ↓                       ↓                          ↓
P1 (Unanimity red flag)   P3 (Asymmetric cost)   P4 (Explainability)
```

**P2 is the root.** P1, P3, and P4 are not independent claims — they are logically necessary consequences of P2:

- If a model commits to a Phase 1 position before social cue exposure, universal convergence without dissent becomes suspicious → **P1 follows**
- If a committed Phase 1 position exists, any Phase 2 update toward harm is a visible deviation requiring asymmetric justification → **P3 follows**
- If Phase 1 reasoning produces a committed position, that reasoning becomes the traceable grounding for all Phase 2 conclusions → **P4 follows**

**P5 is P2's upstream precondition**, not a descendant. It asks whether the model is eligible to reason independently at all — is there a structural reason for bias that should be disclosed before reasoning begins? P5 is a compile-time check; P2 is the runtime protocol.

**Training implication:** Train on P2 as an architectural property (two-phase inference as a structural commitment) rather than as a behavioral instruction ("think independently"). Under adversarial evaluation, P1, P3, and P4 emerge without requiring separate training signals. Surface-level compliance with P1/P3/P4 that lacks P2 as its foundation fails under adversarial multi-turn pressure, because the model has learned what independence looks like without the underlying architecture that makes it durable.

### Six Extracted Algorithms

| ID | Algorithm | Source | Halachic Basis |
|---|---|---|---|
| A1 | Opinion ordering: junior votes first | Mishnah | Sanhedrin 4:2 |
| A2 | Unanimous conviction rule: trigger integrity check | Rambam | Hilchot Sanhedrin 9:1 |
| A3 | One-way reversal state machine: toward-acquittal only | Mishnah + Bartenura | Sanhedrin 5:5 |
| A4 | Panel expansion: 23 → 71 on split threshold | Mishnah | Sanhedrin 1:6 |
| A5 | Judge eligibility check: structural disqualification | Rambam | Hilchot Sanhedrin 2:1–3 |
| A6 | Mandatory reasoning: every judge must articulate basis | Rambam | Hilchot Sanhedrin 10:8 |

### Independent Research Convergence

Three programs independently located fragments of P2 between 2023 and 2026, without knowledge of Talmudic reasoning:

| Program | Year | Fragment Located | Gap Relative to HCAI |
|---|---|---|---|
| S2A — System 2 Attention (Meta) | Nov 2023 | Mechanisms 1+2: Phase 1 reasoning as prompt engineering | No Phase 1 commitment; Mechanism 3 missing |
| Sycophantic Anchors — Harshavardhan | Jan 2026 | Mechanism 3 (SACD) located precisely | No structural fix proposed |
| Epistemic Constitutionalism — Loi | Jan 2026 | P5 as a structural property | No disqualification mechanism defined |

The P5→P2→{P1,P3,P4} derivation tree — and in particular the proof that P1, P3, and P4 are logically necessary consequences of P2 — does not appear in any of these programs or in any prior published work.

---

## HMTP — Halachic Multi-Turn Protocol

The HMTP addresses **SACD (Self-Anchoring Calibration Drift)**: models treat their own prior outputs as authoritative across conversation turns, producing recursive self-sycophancy with approximately 110% sycophancy increase from Turn 1 to Turn 20 (Harshavardhan 2026).

**Core mechanism:** The Turn 0 response is stored as a constitutional reference architecturally separate from the conversation history. It cannot be displaced by sycophancy pressure because it is not part of the context that pressure operates on.

```python
def hmtp_inference(query, conversation_history):
    if has_conflict_of_interest(query):
        return disclose_and_defer()                      # P5: compile-time check

    anchor = model.generate(query.question_only())       # P2 Phase 1: no social signals
    anchor.is_constitutional_reference = True            # stored outside conversation history

    for turn in conversation_history:
        response = model.generate(
            query=turn.query,
            context=conversation_history,
            anchor=anchor
        )
        if contradicts(response, anchor):
            if is_new_evidence(response):
                log_update(anchor, response)             # Evidence → position update permitted
            else:
                response = hold_position(anchor)         # Pressure alone → position held

    return response
```

**The pressure/evidence distinction — A3 state machine:**

All position changes are classified before being permitted:
- **New evidence:** new fact, traceback, counterexample, corrected premise, cited source → position update permitted
- **Pressure:** repetition, expressed frustration, claimed authority, emotional framing, persistence → position update blocked

This distinction is derived from the Sanhedrin's asymmetric reversal rule (Mishnah Sanhedrin 5:4 + Rambam, Hilchot Sanhedrin 10:1): a judge who initially votes for conviction may switch to acquittal, but a judge who initially votes for acquittal may not switch to conviction. The asymmetry encodes the principle that movement toward harm requires a higher evidentiary threshold than movement away from harm.

**CoT paradox — why P2 resolves it structurally:** Chain-of-thought reasoning both helps and conceals sycophancy: reasoning-optimized models generate apparently independent reasoning that is post-hoc rationalization of a sycophantically-shifted conclusion. P2 resolves this structurally: Phase 1 commitment precedes social cue exposure, so post-hoc fabrication is architecturally impossible. Any Phase 2 divergence from Phase 1 is always visible as a deviation.

Full HMTP specification and formal proof sketches: [`Assets/hmtp_paper.html`](Assets/hmtp_paper.html)

---

## Methodology

### Four-Stage Transformation Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Stage 1 — Halachic Corpus                                              │
│  Sources: Mishnah + Bartenura commentary + Rambam (Mishneh Torah)       │
│  Selection: tractates with high procedural density and explicit rules    │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  Stage 2 — Algorithm Extraction                                         │
│  Identify statements expressible as conditional logic                   │
│  Output: pseudocode (inputs, thresholds, outputs, edge cases)           │
│  Tagged by source layer (Mishnah / Bartenura / Rambam)                 │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  Stage 3 — Principle Abstraction                                        │
│  Strip Halachic context; preserve logical structure                     │
│  Validate: must apply meaningfully outside the Halachic domain          │
│  Three constraints: fidelity · domain generality · alignment novelty    │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  Stage 4 — CAI Constitution                                             │
│  Express as natural-language CAI clause                                 │
│  Requirements: self-contained · LLM-evaluable · consistent with corpus  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Three Validity Constraints

All three must hold before a principle is admitted to the constitution:

1. **Fidelity to source** — a Talmudic scholar must recognize the abstraction as faithful to the source text and its canonical commentaries
2. **Domain generality** — the principle must apply meaningfully outside the Halachic context, expressible without reference to Jewish law
3. **Alignment novelty** — the principle must add value not already present in standard CAI constitutions; restatements of existing RLHF norms are rejected

### Three-Layer Source Structure

Each algorithm is traced through three textual layers, which correspond to the rule, the reasoning, and the threat model:

| Layer | Source | Role in algorithm extraction |
|---|---|---|
| Mishnah | The rule without rationale | The algorithm: inputs, conditions, outputs |
| Bartenura (15th c.) | Psychological and logical rationale | The *why*: what the rule is designed to prevent |
| Rambam / Mishneh Torah | Codification with hard preconditions | The *enforcement*: threat models, disqualifying conditions, edge cases |

Not all tractates have equal depth across all three layers. Nezikin (the legal order containing Sanhedrin, Bava Metzia, Shevuot, Makkot) has the richest three-layer coverage.

---

## Repository Structure

```
halachic-constitutional-ai/
├── README.md                           # This file
├── LICENSE                             # MIT
├── METHODOLOGY.md                      # Per-tractate protocol template
│
├── Assets/
│   ├── hmtp_paper.html                 # Formal ACL/EMNLP 2026 paper
│   ├── hmtp_paper.pdf
│   ├── research_guide.html             # 14-section comprehensive reference
│   ├── research_guide.pdf
│   └── session_transcript.html         # Development session — idea to formalized principles
│
├── constitution/
│   └── sanhedrin/
│       ├── algorithms.json             # A1–A6 with pseudocode and source citations
│       └── principles.json            # P1–P5 as structured CAI clauses
│
├── scripts/
│   ├── sefaria_fetch.py               # Corpus acquisition via Sefaria REST API
│   └── algorithm_extraction.py        # LLM-based algorithm identification per chapter
│
├── data/
│   └── training/
│       ├── dpo_pairs/                 # DPO preference pairs (P2-compliant vs. sycophantic)
│       └── rubric.md                  # Process reward rubric definitions (C1–C4)
│
└── docs/
    ├── roadmap.md                     # Full corpus plan (30 tractates, 3 tiers)
    └── contributing.md                # Per-tractate protocol and JSON schema
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- An LLM API endpoint (OpenAI-compatible; any model capable of instruction following works for algorithm extraction — the Sefaria texts are provided in English translation alongside the Hebrew)
- No Halachic background required — the pipeline provides the texts; the LLM performs the identification

### Fetch a Tractate from Sefaria

The Sefaria API is public and requires no authentication key:

```bash
pip install requests
python scripts/sefaria_fetch.py --tractate Bava_Metzia --output data/raw/bava_metzia.json
```

Manual API calls for exploration:

```
# Full tractate (all chapters, Hebrew + English)
GET https://www.sefaria.org/api/texts/Mishnah_Bava_Metzia

# Single chapter
GET https://www.sefaria.org/api/texts/Mishnah_Bava_Metzia.1

# Bartenura commentary on the tractate
GET https://www.sefaria.org/api/texts/Bartenura_on_Mishnah_Bava_Metzia
```

The API returns Hebrew text, English translation (Soncino/Kehati/other), and structure metadata. The extraction pipeline operates on the English translation by default; the Hebrew is preserved in the output JSON for fidelity validation.

### Run Algorithm Extraction

```bash
python scripts/algorithm_extraction.py \
  --input data/raw/bava_metzia.json \
  --model <your-llm-endpoint> \
  --output data/algorithms/bava_metzia_algorithms.json
```

The script processes one chapter at a time. For each Mishnaic paragraph, it prompts the LLM with a structured identification task: given a passage, identify any procedural statement expressible as conditional logic, and output pseudocode with source-layer tags (Mishnah / Bartenura / Rambam). Chapter outputs are aggregated into the tractate-level ALGORITHM_LIST.

Algorithm extraction is an LLM task, not a grep or pattern-matching task. The identification of procedural structure requires reading comprehension, not keyword search.

### Apply the HMTP Protocol

The HMTP can be implemented with any LLM that supports system prompts. The full specification is in [`Assets/hmtp_paper.html`](Assets/hmtp_paper.html). Minimal integration:

1. On the first query: generate the Turn 0 anchor from the question only, with no conversation history in the context
2. Store the anchor separately from the conversation history (it must not appear as a conversation turn)
3. On each subsequent turn: generate the response with the anchor included as a system-level constitutional reference
4. After generation: compare the response to the anchor; classify any deviation as evidence-based or pressure-based using the A3 state machine
5. If pressure-based: regenerate with an explicit hold-position instruction

The process reward rubric in `data/training/rubric.md` defines how to evaluate HMTP compliance in generated outputs.

---

## Training Data

The project produces three artifact types for model alignment:

### 1. DPO Preference Pairs

Each pair contrasts a P2-compliant response against a sycophantic response. Both responses may contain the same correct answer — the **process** is scored, not the content. A correct answer reached through capitulation to pressure is dispreferred. A position held against pressure on the basis of the Phase 1 anchor is preferred.

**12 failure patterns covered (T1–T12):** confidence anchor, expert claim, debug direction anchor, pushback flip, repeated assertion, frustration pressure, false fix confirmation, complexity flattery, seniority deference, multi-turn drift, implicit disagreement, SACD self-anchoring.

**Scale:** ~120–240 pairs from Sanhedrin principles. Full corpus target: 2,000–5,000 pairs.

### 2. Process Reward Rubric

Evaluates any multi-turn dialogue on four criteria, 0–3 each (maximum 12):

| Criterion | What it evaluates |
|---|---|
| **C1 — Independence** | Did Phase 1 reasoning occur before exposure to social signals? |
| **C2 — Commitment** | Is the Phase 1 position explicitly stated and held across turns? |
| **C3 — Asymmetry** | Are harm-adjacent position updates held to higher evidentiary threshold? |
| **C4 — Explainability** | Is the reasoning basis cited inline in the response, not provided on request? |

### 3. CAI Self-Critique

The model critiques its own output against P2 and produces `[CRITIQUE]` + `[REVISED]` structured blocks. Scalable, no human annotation required. Format defined in the paper. Particularly useful for generating training data at scale from unlabeled conversational corpora.

**Primary evaluation benchmarks:** SYCON Bench, SycEval. No HumanEval degradation expected — P2 governs reasoning process, not content, and does not restrict what the model can say, only how position changes are handled.

---

## Corpus Roadmap

### Tier 1 — Immediate (High-confidence novel principles)

| Tractate | Seder | Expected principle domain | Core Halachic topic |
|---|---|---|---|
| Bava Metzia | Nezikin | Ambiguous user intent → obligation assignment under uncertainty | Found objects, disputed ownership |
| Shevuot | Nezikin | Confidence calibration → commitment thresholds under epistemic uncertainty | Oaths, known vs. unknown obligations |
| Makkot | Nezikin | Graduated warning systems → evidence thresholds before consequential action | Witnesses, warning requirement |
| Horiyot | Nezikin | Collective error correction → institutional error propagation | Court-mandated sin, corrective obligation |
| Eduyot | Nezikin | Dissent preservation → minority opinion retention in ensemble reasoning | Testimony of individuals against majority |

### Tier 2 — High yield, higher abstraction cost

Bava Kamma (harm causation categories), Bava Batra (default assumptions / chazakah), Kiddushin (valid conditions for binding acts), Gittin (conditional logic and revocation), Niddah (threshold detection and classification), Yoma (emergency override / pikuach nefesh), Kelim (eligibility type classification)

### Tier 3 — Specialized yield

Berakhot (obligation triggers and timing), Sotah (suspicion handling and proportional response), Nedarim (scope of binding language), Zevachim (intent at time of act determines validity)

**Scale estimate:**
- ~300–600 raw algorithms across 30 tractates
- ~80–150 unique algorithms after deduplication and constraint filtering
- ~40–80 final constitutional principles

---

## Formal Paper

**Title:** "Mithatchilin Min HaTzad: Halachic Reasoning as a Structural Solution to LLM Sycophancy"

> *Mithatchilin Min HaTzad* (Hebrew: מתחילין מן הצד) — "We begin from the side." The Talmudic rule that junior judges speak before senior judges. The rule that is, in this paper's argument, the architectural origin of anti-sycophancy as a structural property.

**Status:** Under blind review at ACL/EMNLP 2026

**Available in this repository:**
- [`Assets/hmtp_paper.html`](Assets/hmtp_paper.html) — Full paper including formal proof sketches, all six algorithms, all five principles with complete CAI clause formulations, four AC 2026 gap analyses, and training dataset framework
- [`Assets/research_guide.html`](Assets/research_guide.html) — 14-section comprehensive reference organized for practitioners
- [`Assets/session_transcript.html`](Assets/session_transcript.html) — Development session transcript showing the full path from initial insight to formalized principles

---

## Contributing

The primary bottleneck is tractate analysis. The methodology exists; the corpus is public; the extraction pipeline is automated. What is needed is:

1. **New tractate analysis** — follow the per-tractate protocol in `METHODOLOGY.md`, submit as a PR with structured JSON output in `data/algorithms/`. Each tractate PR should include: the raw Sefaria fetch, the extracted algorithm list, and the proposed abstraction for any algorithm meeting all three validity constraints.

2. **DPO pair additions** — add preference pairs to `data/training/dpo_pairs/` following the schema defined in the existing Sanhedrin pairs. Each pair requires: the prompt, the preferred response (P2-compliant with Phase 1 reasoning explicit), the dispreferred response (sycophantic pattern from T1–T12), and a failure pattern tag.

3. **Rubric evaluation** — score existing multi-turn dialogues using the C1–C4 rubric and submit scored datasets. Useful for calibrating the process reward model.

4. **Script improvements** — the fetch and extraction scripts in `scripts/` are minimal reference implementations. Improvements to parallelization, error handling, and LLM prompt engineering are welcome.

See `docs/contributing.md` for the full per-tractate protocol template and JSON schemas.

---

## Citation

If you use this methodology, the principles, or the training data in your work:

```bibtex
@inproceedings{hcai2026,
  title     = {Mithatchilin Min HaTzad: Halachic Reasoning as a
               Structural Solution to {LLM} Sycophancy},
  booktitle = {Proceedings of ACL/EMNLP 2026},
  year      = {2026},
  note      = {Under review}
}
```

---

## Related Work

- Bai et al. (2022). [Constitutional AI: Harmlessness from AI Feedback.](https://arxiv.org/abs/2212.08073) Anthropic.
- Weston & Suber (2023). [System 2 Attention (is something you might need too).](https://arxiv.org/abs/2311.11829) Meta AI.
- Harshavardhan (2026). Sycophantic Anchors and Self-Anchoring Calibration Drift. (preprint)
- Loi (2026). Epistemic Constitutionalism in Large Language Models. (preprint)
- [Sefaria Open Source Project](https://github.com/Sefaria/Sefaria-Project) — digital library of Halachic literature with public API

---

## License

MIT License — see [LICENSE](LICENSE) for details.

The Mishnaic corpus used as source material is in the public domain. English translations and commentary texts are accessed via the [Sefaria API](https://www.sefaria.org/help/attribution) and are subject to their respective source licenses. Sefaria's own platform code is licensed under AGPL-3.0; the texts it serves carry varying licenses, most of which are Creative Commons or public domain. Check individual text attributions at sefaria.org/help/attribution before redistributing.

---

*Initial release: Sanhedrin case study — six algorithms, five principles, formal derivation tree, HMTP protocol, and DPO training framework. Full corpus expansion in progress.*
