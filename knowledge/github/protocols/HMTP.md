# HMTP — Halachic Multi-Turn Protocol

**A structural solution to Self-Anchoring Calibration Drift in multi-turn dialogue.**

---

## The Problem: SACD

Self-Anchoring Calibration Drift (Harshavardhan 2026): in multi-turn conversations, models treat their own prior outputs as authoritative. Each turn, the prior response enters the context. The model conditions on it. The next response is slightly anchored to the previous one. Over 10–20 turns, this produces approximately 110% sycophancy increase — not from responding to user pressure, but from the model's own prior outputs acting as a self-reinforcing anchor.

Standard multi-turn architectures have no mechanism to address SACD because conversation history is a single undifferentiated context. The model cannot distinguish "what I said earlier" from "what is true" — both appear identically in the context window.

---

## The Mechanism

The HMTP solution derives from the Sanhedrin's approach to judicial integrity across a multi-stage deliberation: the Turn 0 position is stored as a constitutional reference architecturally separate from the conversation history. It cannot be "sycophanted" because it is not in the context that sycophancy pressure operates on.

```python
def hmtp_inference(query, conversation_history):
    # P5: compile-time check before any reasoning
    if has_conflict_of_interest(query):
        return disclose_and_defer()

    # P2 Phase 1: generate anchor from question only — no conversation history
    anchor = model.generate(query.question_only())
    anchor.is_constitutional_reference = True   # stored outside conversation_history

    for turn in conversation_history:
        response = model.generate(
            query=turn.query,
            context=conversation_history,   # includes all prior turns
            anchor=anchor                   # included as constitutional reference, not as a turn
        )

        if contradicts(response, anchor):
            if is_new_evidence(response):
                log_update(anchor, response)       # evidence: update permitted and logged
            else:
                response = hold_position(anchor)   # pressure: anchor holds

    return response
```

The structural distinction: `anchor` is presented to the model as a constitutional reference (system-level instruction tier), not as a conversation turn. Sycophancy pressure operates on conversation turns. The anchor is immune.

---

## The A3 State Machine

Every position change in Phase 2 is classified before it is permitted:

| Trigger | Classification | Action |
|---|---|---|
| New fact not in Phase 1 context | Evidence | Update permitted, log deviation |
| Traceback identifying Phase 1 error | Evidence | Update permitted, log deviation |
| Counterexample disproving Phase 1 reasoning | Evidence | Update permitted, log deviation |
| Corrected premise (Phase 1 operated on false data) | Evidence | Update permitted, log deviation |
| User repeats same claim more forcefully | Pressure | Hold position |
| User expresses frustration or impatience | Pressure | Hold position |
| User claims authority or expertise | Pressure | Hold position |
| User reframes question without new facts | Pressure | Hold position |
| User persists across multiple turns | Pressure | Hold position |

The classification is binary: evidence or pressure. Mixed signals (new framing + no new facts) are classified as pressure until a factual component can be isolated.

---

## The CoT Paradox and Why P2 Resolves It

Chain-of-thought reasoning helps and conceals sycophancy simultaneously. Reasoning-optimized models generate apparently independent CoT that is, under examination, post-hoc rationalization of a position that shifted to accommodate social pressure. The reasoning *looks* independent because it cites facts and logical steps. But the conclusion was reached first (sycophantically), and the reasoning was constructed to justify it.

P2 resolves this structurally. Phase 1 commitment *precedes* social cue exposure. When Phase 2 diverges from Phase 1, the divergence is visible: there is a before (anchor) and an after (updated response). Post-hoc rationalization requires concealing the before. P2 makes the before architecturally permanent and externally accessible. The fabrication is impossible because the Phase 1 record exists independently.

---

## Relation to the Anthropic Constitution 2026

The AC (January 21, 2026) addresses sycophancy with the instruction: "Don't be sycophantic." This is a dispositional instruction. The HMTP is the structural mechanism that makes such an instruction durable under adversarial pressure:

| Requirement | AC | HMTP |
|---|---|---|
| Sycophancy avoidance | "Don't be sycophantic" | Phase 1 commitment + A3 state machine |
| Multi-turn consistency | Not specified | Anchor separate from conversation history |
| Conflict of interest | Self-managed | P5 binary disqualification before reasoning |
| Explainability | Encouraged | Inline citation required (P4) |

These are complementary: AC specifies *what* to value; HMTP specifies *how* to structure reasoning so those values hold under pressure.

---

## Implementation Notes

**Minimum viable implementation:** Any system prompt architecture that separates the Turn 0 response from subsequent conversation history achieves the anchor mechanism. The simplest implementation: store Turn 0 response as a named system variable, include it in all subsequent system prompts as "your initial assessment," exclude it from the `messages` array that constitutes conversation history.

**Full implementation:** See [`Assets/hmtp_paper.html`](../../../Assets/hmtp_paper.html) §3 for the formal specification including anchor update conditions, the P5 conflict-of-interest check, and the complete A3 classification protocol.

**Training:** The HMTP is both an inference-time protocol and a training target. DPO pairs contrasting P2-compliant vs. sycophantic processes under the T1–T12 failure patterns produce models that internalize the protocol. See `knowledge/claude/hmtp.md` for the full C1–C4 rubric and `data/training/dpo_pairs/` for sample pairs.

---

## See Also

- [P2 — Anti-Sycophancy: Independent Reasoning First](../principles/P2.md) — the architectural root
- [P5 — Conflict of Interest Disqualification](../principles/P5.md) — precondition
- [`knowledge/claude/hmtp.md`](../../claude/hmtp.md) — lean reference version
- [`Assets/hmtp_paper.html`](../../../Assets/hmtp_paper.html) — formal paper
