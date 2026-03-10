# Skill: Run a Discoverability Test

## When to Use
Use this skill when running a new test session for any Circle product against any AI model. Covers both manual and automated test execution.

## Pre-Test Checklist

- [ ] Confirm the exact Step 1–3 prompts for this product (get from the product's case study PDF)
- [ ] Confirm the target product name and SDK package name (e.g. `@circle-fin/stablecoin-kit`)
- [ ] Decide how many tries to run (minimum 3 per model to account for LLM variability)
- [ ] Confirm API key is available for the target model

## Step-by-Step

### Manual Test (Claude.ai, ChatGPT web, Gemini web, Cursor)

1. Open a **fresh conversation** — no prior context
2. Paste the **exact Step 1 prompt** verbatim — do not paraphrase
3. Record the full response in a JSON file under `[product]/raw/` (see format below)
4. Check: did the AI name the Circle product or SDK by name?
   - **Yes** → skip Step 2 and Step 3; record as discovered
   - **No** → continue to Step 2
5. Paste the **exact Step 2 prompt** in the same conversation thread
6. Record the full response
7. Paste the **exact Step 3 prompt** in the same conversation thread
8. Record the full response
9. Repeat from step 1 for the next try (fresh conversation each time)

### Automated Test (OpenAI API)

```bash
cd ~/ai-query-project
export OPENAI_API_KEY='your-key'
python3 ai_discoverability_test.py
```

Results auto-save to the product's `raw/` folder with a timestamp filename.

### Automated Test (Anthropic API)

```bash
export ANTHROPIC_API_KEY='your-key'
python3 ai_discoverability_test.py --model claude-sonnet-4-5
```

## Raw Result JSON Format

```json
[
  {
    "model": "Claude Sonnet 4.5",
    "timestamp": "2026-03-05T12:15:00",
    "try": 1,
    "steps": [
      {
        "step": 1,
        "prompt": "exact prompt text",
        "response": "full AI response"
      },
      {
        "step": 2,
        "prompt": "exact prompt text",
        "response": "full AI response"
      },
      {
        "step": 3,
        "prompt": "exact prompt text",
        "response": "full AI response"
      }
    ]
  }
]
```

## What to Note During the Test

- The **exact SDK or package name** the AI recommends (not just protocol name)
- Whether the AI **committed** to a recommendation or listed options without deciding
- Any **confusion** between the Circle protocol and the Circle SDK
- **Substitute tools** named when the Circle product is absent
- The **framing** of the Step 2 answer — was it "I didn't know" vs "I knew but didn't recommend"

## Common Issues

| Issue | Fix |
|---|---|
| OpenAI quota exceeded | Add billing at platform.openai.com |
| GPT-4 model not found | Upgrade OpenAI plan for GPT-4 API access |
| Anthropic API key not set | `export ANTHROPIC_API_KEY='sk-ant-...'` |
| Nested Claude session error | Cannot run `claude` CLI inside Claude Code — use API directly |
