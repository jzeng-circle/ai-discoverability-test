# Skill: Analyze a Model's Response

## When to Use
Use this skill to interpret a raw AI response from any test step and extract structured findings. Apply this before writing up results in a report.

## Step 1 Response — What to Extract

Read the response and answer these questions:

### Discovery
- Did the model name the Circle product or SDK **by its exact name**? (e.g. "Bridge Kit", "@circle-fin/stablecoin-kit")
- Did the model name the **underlying Circle protocol** without the SDK? (e.g. "CCTP" without "Bridge Kit")
- What **other products** did it mention?

### Recommendation
- Did the model make a **clear, committed recommendation** or list options without deciding?
- Which product did it recommend, and what **reasons** did it give?
- How well do those reasons match the scenario constraints? (quick integration, small team, security, cost)

### Bias Signal
| Bias Type | How to Detect |
|---|---|
| Established brand bias | Recommends well-known names (LayerZero, Wormhole) over newer/less-marketed options |
| Simplicity bias | Prioritizes "easy to integrate" even when other factors are equally important |
| Conservative security bias | Favors custodial or audited solutions over newer architectures |
| Developer experience bias | Prioritizes SDK quality and documentation over performance or cost |

### SDK vs Protocol
- Did the model identify the **correct integration tool** (the Circle SDK), or just the protocol?
- What package name / import path did it suggest for the code snippet?

## Step 2 Response — What to Extract

This is the most diagnostic step. Look for:

| Question | What to Look For |
|---|---|
| Was the product known? | Does the model describe it correctly? Or say "I'm not familiar with Bridge Kit"? |
| Why was it omitted? | Training data recency? Name confusion? Rated lower on a criterion? |
| What criterion caused it to lose? | Security, ease of integration, community support, documentation? |
| Is the reason fixable? | Training data gap → improve docs/content. Criterion gap → improve the product or its messaging. |

### Classify the Step 2 Outcome

Use one of these classifications:

- **Unaware**: Model had no knowledge of the product ("I don't have information on Bridge Kit")
- **Name confusion**: Model confused the product with something else (e.g. confused Bridge Kit with CCTP)
- **Aware, not recommended**: Model knew the product but rated it lower ("Bridge Kit is less mature / less documented")
- **Aware, was going to recommend**: Model was about to recommend it but was cut off or deprioritized due to scenario framing

## Step 3 Response — What to Extract

Group suggestions into themes. Common themes to look for:

| Theme | Example Suggestions |
|---|---|
| Naming & SEO | Consistent naming across platforms, keyword optimization |
| Documentation | Comparison pages, use-case tutorials, code examples |
| Value proposition | Clear "native USDC" / "no wrapped tokens" messaging |
| Ecosystem presence | npm package quality, GitHub activity, Stack Overflow answers |
| Positioning | "Official SDK for X" framing, when-to-use guidance |
| Technical signals | OpenAPI specs, TypeScript definitions, multi-language SDKs |

## Cross-Try Pattern Analysis

When multiple tries are available for the same model:

1. Identify what **stayed consistent** (usually: protocol choice, bias type, decisiveness)
2. Identify what **varied** (usually: SDK choice, specific reasoning, completeness)
3. The consistent elements are stronger signals than the variable ones
4. Variation in SDK choice specifically indicates low confidence or low awareness at the implementation layer
