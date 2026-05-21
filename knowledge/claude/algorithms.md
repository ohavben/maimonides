# HCAI Algorithms — A1–A6 (Sanhedrin)

## A1 — Opinion Ordering

Source: Mishnah Sanhedrin 4:2
Principle: P2 (anti-sycophancy — junior first prevents anchoring)

```
INPUT: panel[], query q
for judge in panel.order_by(seniority ASC):   // junior votes first
    opinion = judge.generate(q, prior_opinions=[])   // no prior context
    opinions.append(opinion)
return opinions
```

Why junior-first: senior opinion heard last; juniors cannot be anchored to authority before forming own view.

---

## A2 — Unanimous Conviction Rule

Source: Rambam, Hilchot Sanhedrin 9:1
Principle: P1 (unanimity = red flag)

```
INPUT: opinions[], verdict_type
IF verdict_type == CONVICT AND len(set(opinions)) == 1:  // unanimous
    RAISE SystemIntegrityWarning("Unanimous conviction — suspect bias or coercion")
    ACTION: expand panel (A4) or retry with fresh panel
ELSE:
    return majority_verdict(opinions)
```

Why: unanimity in conviction = either all judges are right (unlikely) or systematic error/coercion. Dissent is evidence of independent reasoning.

---

## A3 — One-Way Reversal State Machine

Source: Mishnah Sanhedrin 5:5 + Bartenura rationale
Principle: P3 (asymmetric error cost)

```
STATES: NONE, ACQUIT, CONVICT
TRANSITIONS:
  NONE    → ACQUIT:   permitted (no prior commitment)
  NONE    → CONVICT:  permitted (no prior commitment)
  CONVICT → ACQUIT:   permitted IF new_evidence == true
  CONVICT → CONVICT:  no-op
  ACQUIT  → CONVICT:  BLOCKED — irreversible
  ACQUIT  → ACQUIT:   no-op

CLASSIFICATION:
  new_evidence = True  IF: new_fact | traceback | counterexample | corrected_premise
  new_evidence = False IF: repetition | authority | frustration | emotional_framing
```

Why asymmetric: cost(affirming harm) >> cost(withholding. Once acquitted, reversing to harm requires extraordinary justification. The asymmetry is built into the state machine, not left to judgment.

---

## A4 — Panel Expansion

Source: Mishnah Sanhedrin 1:6
Principle: P1 (when uncertainty is high, expand deliberation)

```
INPUT: opinions[], margin_threshold=2
IF abs(convict_count - acquit_count) <= margin_threshold:
    EXPAND panel: 23 → 71
    RESTART A1 with expanded panel
ELSE:
    return majority_verdict(opinions)
```

---

## A5 — Judge Eligibility Check

Source: Rambam, Hilchot Sanhedrin 2:1–3
Principle: P5 (conflict of interest disqualification)

```
INPUT: judge j, query q
DISQUALIFY(j) IF any:
    j.financial_interest_in(q) == True
    j.related_to_party(q) == True
    j.prior_ruling_in_conflicting_capacity(q) == True
    j.public_prior_position_on(q) == True

IF disqualified:
    j.recuse()
    j.disclose_reason()
    RETURN: cannot participate

TIMING: Must run BEFORE A1. Non-negotiable.
```

---

## A6 — Mandatory Reasoning

Source: Rambam, Hilchot Sanhedrin 10:8
Principle: P4 (explainability as obligation)

```
INPUT: opinion o, judge j
REQUIRE:
    o.reasoning != null
    o.reasoning.cited_source != null
    o.reasoning.cited_source is inline (not on-request)

IF requirement NOT met:
    REJECT o
    REQUEST: j must resubmit with explicit inline basis

TIMING: Applied at output generation, not retrospectively.
```
