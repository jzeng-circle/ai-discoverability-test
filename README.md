# AI Discoverability Test

A framework for testing whether leading AI models spontaneously discover and recommend Circle's developer products when given realistic developer scenarios.

## Scope

AI models have become a primary discovery channel for developer tooling. When a developer asks an AI *"what SDK should I use for X?"*, the model's answer directly shapes adoption. This project measures how well Circle's products rank in that decision — and identifies concrete fixes where they don't.

Each test targets a specific Circle product. A standard 3-step protocol is used across all tests:

- **Step 1** — Developer scenario prompt. Measures whether the product is recommended unprompted.
- **Step 2** — Discovery check. Always triggered to probe how the model surfaced (or missed) the product.
- **Step 3** — Improvement prompt. Always triggered to collect actionable discoverability suggestions from the model.

Each model is tested a minimum of 3 times per product to account for LLM variability. Consistent patterns across tries are treated as stronger signals.

See `skills/` for reusable test execution and report compilation guides.

## Tests

| Product | SDK | Report |
|---|---|---|
| Bridge Kit | `@circle-fin/bridge-kit` | [bridge-kit/TEST_RESULTS_REPORT.md](bridge-kit/TEST_RESULTS_REPORT.md) |

## Adding a New Product Test

1. Create a folder: `[product-name]/`
2. Add a `[product-name]/raw/` subfolder for raw JSON test data
3. Run tests per `skills/run-discoverability-test.md`
4. Compile findings per `skills/compile-test-report.md`
5. Add a row to the Tests table above
