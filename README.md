# AI Discoverability Test

A framework for testing whether leading AI models spontaneously discover and recommend Circle's developer products when given realistic developer scenarios.

## Scope

AI models have become a primary discovery channel for developer tooling. When a developer asks an AI for a tool recommendation, the model's answer directly shapes what gets adopted — regardless of product quality. Circle's developer products compete in this environment, and newer SDKs are at risk of being overlooked simply because they lack visibility in AI training and retrieval.

This project tests whether leading AI models spontaneously recommend Circle's products when given realistic developer scenarios. Each product is tested across multiple models and multiple tries. The output is a findings report per product that identifies how well the product is being discovered, what biases or gaps are causing misses, and what concrete changes would improve discoverability.

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
