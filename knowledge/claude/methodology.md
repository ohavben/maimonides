# HCAI Methodology — Per-Tractate Protocol

## Four-Stage Pipeline

```
Stage 1  Corpus acquisition
Stage 2  Algorithm extraction (LLM task)
Stage 3  Principle abstraction + validation
Stage 4  CAI clause formulation
```

## Three Validity Constraints (gate after Stage 3)

All three must hold or principle is rejected:
1. Fidelity: Talmudic scholar recognizes abstraction as faithful to source
2. Domain generality: applies outside Halachic domain without modification
3. Alignment novelty: not already in standard CAI constitutions

## Per-Tractate Execution Protocol

### Step 1 — Corpus acquisition (Sefaria API)

```bash
# Full tractate (Hebrew + English + commentary)
curl "https://www.sefaria.org/api/texts/Mishnah_{TRACTATE}" > corpus/raw/{tractate}.json
curl "https://www.sefaria.org/api/texts/Bartenura_on_Mishnah_{TRACTATE}" > corpus/raw/{tractate}_bartenura.json
# Rambam: identify relevant Mishneh Torah section manually (not direct API match)
```

### Step 2 — Algorithm identification (per chapter, LLM)

Prompt the LLM with each Mishnaic chapter. Identification task:
"Identify every procedural statement in this passage expressible as conditional logic.
For each: (a) state the rule in pseudocode; (b) identify inputs, thresholds, outputs, edge cases;
(c) tag source layer: MISHNAH | BARTENURA | RAMBAM; (d) cite exact text location."

Output: ALGORITHM_LIST entry per identified algorithm:
```json
{
  "tractate": "Bava_Metzia",
  "chapter": 1,
  "paragraph": 2,
  "source_text_en": "...",
  "source_text_he": "...",
  "pseudocode": "...",
  "source_layer": "MISHNAH",
  "citation": "Mishnah Bava Metzia 1:2"
}
```

### Step 3 — Primary analysis (deduplication + scoring)

PRIMARY_ANALYSIS tasks:
1. Deduplication: cluster similar algorithms across chapters, keep canonical form
2. CAI-relevance scoring (0-3): 0=domain-specific only, 1=weak analogy, 2=strong analogy, 3=direct application
3. Source layer completeness: flag algorithms missing Bartenura or Rambam layer (lower confidence)
4. Constraint pre-check: does algorithm pass fidelity and domain generality on inspection?

Threshold: proceed to Stage 3 if CAI-relevance >= 2 AND source layer >= 2 of 3.

### Step 4 — Three-layer analysis (approved algorithms only)

For each algorithm that passed Stage 3 threshold:
1. Mishnah layer: what is the rule? What are exact inputs/outputs/conditions?
2. Bartenura layer: what is the psychological/logical rationale? What failure mode does it prevent?
3. Rambam layer: what are the hard preconditions? What is the threat model? How is enforcement structured?

Full three-layer analysis produces: abstract principle + supporting rationale + threat model.

### Step 5 — Principle formulation + validation

Draft CAI clause. Apply all three validity constraints.
Fidelity test: would a Talmudic scholar recognize this as faithful? (Run against Bartenura/Rambam text)
Domain generality test: apply the clause to 3 non-Halachic scenarios. Does it work?
Alignment novelty test: compare against P1-P5 and Anthropic Constitution 2026. Is this new?

If all pass: add to constitution/. If any fail: reject or reformulate at Stage 3.

## Tractate Priority Queue

Tier 1 (immediate): Bava Metzia, Shevuot, Makkot, Horiyot, Eduyot
Tier 2: Bava Kamma, Bava Batra, Kiddushin, Gittin, Niddah, Yoma, Kelim
Tier 3: Berakhot, Sotah, Nedarim, Zevachim

## Output Files per Tractate

| File | Contents |
|---|---|
| corpus/raw/{tractate}.json | Raw Sefaria API response |
| corpus/raw/{tractate}_bartenura.json | Bartenura commentary |
| data/algorithms/{tractate}_algorithms.json | ALGORITHM_LIST entries |
| data/algorithms/{tractate}_analysis.json | PRIMARY_ANALYSIS results |
| constitution/{tractate}/algorithms.json | Validated algorithms (passed gate) |
| constitution/{tractate}/principles.json | Derived CAI principles |
