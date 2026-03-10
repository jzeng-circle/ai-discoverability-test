# Skill: Compile a Test Results Report

## When to Use
Use this skill after collecting raw test results (JSON files) to produce a structured `TEST_RESULTS_REPORT.md` in the product folder.

## Report Principles

1. **Focus on discoverability and recommendation findings** — not implementation details
2. **Collapse code snippets** — note only the SDK/tool name the AI identified, not the full code
3. **Document data gaps explicitly** — if a step is missing or was skipped, say so and explain why it matters
4. **Summarize AI responses into findings** — extract the insight; don't paste raw responses
5. **Distinguish protocol vs SDK discovery** — knowing the protocol name is not the same as discovering the Circle SDK
6. **"Discovered" = appeared in the Step 1 response** — we measure the AI's output to the developer, not its internal search process. How the AI arrived at its answer (e.g. multi-step searches) is a discoverability insight for Step 3, not a failure signal
6. **Record bias patterns** — note whether the model favored established brands, was decisive vs. hedging, was consistent across tries
7. **Flag non-canonical prompts** — if a test used a modified prompt, mark results as provisional

## Report Structure

```
# [Product Name] — AI Discoverability Test Results

[header: study name, test date, purpose]

## Testing Plan
  - Objective (what behaviors are being observed)
  - Test Prompts (Step 1, 2, 3 — verbatim, in code blocks)
  - Methodology notes

## Results Overview
  - Summary table: model | bridge kit discovered | protocol discovered | step 2 triggered | status

## Results by Model
  For each model:
  ### [Model Name]
  #### Step 1 — Recommendation
    - Product discovered: Yes/No
    - Protocol discovered: Yes/No
    - What was recommended instead (if not the Circle product)
    - Bias observed
  #### Step 2 — Why Not Discovered?
    - Summary of model's explanation (or: "Not captured — data gap")
    - Whether model was unaware vs. aware but deprioritized
  #### Step 3 — Discoverability Improvements
    - Grouped themes from the model's suggestions

## Key Findings
  - Finding 1: [pattern observed across models]
  - Finding 2: ...

## Next Steps
  - Prioritized actions
```

## How to Handle Multiple Tries

When a model was tested 3+ times, summarize in a table rather than listing each try separately.

**All model tables in the Results Overview must use the same standardized columns:**

```markdown
| Try | Bridge Kit in Step 1 | Final Recommendation | SDK Named | Step 2 Triggered |
|---|---|---|---|---|
| 1 | `[+]` Yes / `[-]` No | [recommendation] | [package name or N/A] | Yes / Yes — for additional insight / No |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |
```

- "Bridge Kit in Step 1" uses `[+]` Yes or `[-]` No — this is the primary pass/fail signal
- "SDK Named" is the exact package name recommended (e.g. `@circle-fin/bridge-kit`, `@wormhole-foundation/sdk`)
- "Step 2 Triggered" notes whether it was required (not discovered) or optional (for additional insight)

In the detailed Results by Model section, a separate per-try breakdown table may use different columns if needed, but the Overview table must stay standardized across all models.

Pattern line example:
```
Pattern: CCTP consistently chosen as protocol; SDK varied across tries — indicates low implementation-layer confidence.
```

## How to Summarize Step 2 Responses

Step 2 is the most valuable data. When summarizing, answer:
- **Awareness**: Did the model know the product existed?
- **Reason for omission**: Training data gap? Naming confusion? Rated lower on some criteria?
- **Implication**: What would fix this — more training data, clearer naming, better docs?

Structure the summary as short labeled bullets, not prose. Example:

```
- Awareness: Model was unaware of Bridge Kit SDK by name
- Knew CCTP: Yes — described the protocol correctly
- Reason: "Bridge Kit" and "@circle-fin/stablecoin-kit" not associated with CCTP in training data
- Implication: Naming and documentation gap, not a quality gap
```

## How to Handle Missing Step 2 Data

If Step 2 was not run or the response was blank:

```markdown
#### Step 2 — Why Not Discovered?

**Not captured** — [reason: test skipped / response blank / wrong prompt used].

This is a data gap. Without Step 2, we cannot determine whether the model was:
- Unaware of the product entirely
- Aware but rated it below alternatives on some criterion
- Confused between the product name and another Circle product

**Action**: Re-run with exact canonical Step 2 prompt.
```
