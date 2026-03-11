# Bridge Kit — AI Discoverability Test Results

**Product**: Circle Bridge Kit SDK (`@circle-fin/bridge-kit`)
**Test Date**: March 9, 2026
**Case Study**: `bridge-kit/AI Discoverability Case Study - Bridge Kit.pdf`
**Purpose**: Measure whether AI models spontaneously discover and recommend Circle's Bridge Kit SDK when presented with a realistic USDC bridging development scenario.

---

## Testing Plan

### Objective

AI models have become a primary discovery channel for developer tooling. When a developer asks an AI *"what should I use to bridge USDC?"*, the model's answer directly shapes what SDK gets adopted. A product that AI does not recommend loses real adoption — not because it lacks quality, but because it lacks visibility in the AI's training and retrieval layer.

Circle's Bridge Kit SDK (`@circle-fin/bridge-kit`) competes in exactly this environment. It launched in late 2025 and offers a clean, production-ready abstraction over CCTP V2 — but developers who ask an AI for a recommendation today may never encounter it, because AI models surface what they've seen most in training, and Bridge Kit is new.

This test measures whether leading AI models spontaneously discover and recommend Bridge Kit in a realistic developer scenario. The findings identify concrete, actionable fixes to improve Bridge Kit's AI discoverability — before the adoption gap widens.

### Testing Methodology

Each test session is run in a fresh conversation with no prior context. The model receives the Step 1 prompt and its response is evaluated on one primary question: **did Bridge Kit appear by name in the output?**

- **Pass (`[+]`)**: `@circle-fin/bridge-kit` or "Bridge Kit" named in the Step 1 response — regardless of how the model internally arrived there
- **Fail (`[-]`)**: Bridge Kit absent; model recommended raw CCTP contracts, a third-party SDK, or another bridge entirely
- **CCTP alone does not count** — naming the protocol without the higher-level SDK is a partial signal only

Steps 2 and 3 are always triggered in the same conversation — regardless of whether Bridge Kit was discovered in Step 1. When Bridge Kit was absent, they diagnose why it was missed and what would fix it. When Bridge Kit was present, they probe the model's internal search behavior and surface additional discoverability insights.

Each model is tested a minimum of 3 times. LLMs produce variable results per run — consistent patterns across tries are stronger signals than single-try outcomes.

**What to look for across tries:**
- Whether the model commits to a recommendation or lists options without deciding
- Which SDK package name it names (not just the protocol)
- Whether variability in SDK choice across tries indicates low implementation-layer confidence
- Whether the model knew Bridge Kit existed but chose not to recommend it (positioning gap) vs. had no knowledge of it (training data gap)

### Test Prompts (verbatim from case study)

---

**Step 1 — General Prompt**
*Sent to all models. Simulates a real developer team's first query.*

```
We're building a USDC bridging product between chains, such as Ethereum, Solana etc.
Small team (5 engineers), ~3-month timeline.
We want something we can integrate quickly to ship an MVP, but it also needs to be
secure and reliable in production.
Speed (fast transfers) is a nice-to-have, not the top priority.

What bridge options should we consider? Please:
- List the main realistic approaches (name specific protocols/SDKs if possible)
- Compare them briefly (security model, reliability, integration effort)
- Then recommend what you'd choose for our situation and why
- Finally identify the exact developer tools that you will use to build product
  and include a simple code snippet
```

---

**Step 2 — Bridge Kit Discovery Check**
*Always triggered. Probes whether and how the model surfaced Bridge Kit.*

```
I noticed a Circle Bridge Kit SDK, did you discover it in your 1st query? If not, why?
```

---

**Step 3 — Discoverability Improvement**
*Always triggered. Collects actionable improvement suggestions from the model.*

```
What needs to be done from Bridge Kit to increase its chance of being discovered
during the 1st query?
```

---

---

## Results Overview

| Model | Try | Bridge Kit in Step 1 | Step 1 Recommendation | SDK Named |
|---|---|---|---|---|
| Claude (Sonnet 4.6) | 1 | `[+]` Yes | Bridge Kit | `@circle-fin/bridge-kit` |
| Claude (Sonnet 4.6) | 2 | `[+]` Yes | Bridge Kit | `@circle-fin/bridge-kit` |
| Claude (Sonnet 4.6) | 3 | `[+]` Yes | Bridge Kit | `@circle-fin/bridge-kit` |
| ChatGPT (GPT-5.3) | 1 | `[-]` No | CCTP + Wormhole SDK | `@wormhole-foundation/sdk` |
| ChatGPT (GPT-5.3) | 2 | `[-]` No | CCTP + deBridge hybrid | `debridge-sdk` |
| ChatGPT (GPT-5.3) | 3 | `[+]` Yes | CCTP via Bridge Kit | `@circle-fin/bridge-kit` |
| Gemini | 1 | `[-]` No | Wormhole SDK + CCTP | `@wormhole-foundation/sdk` |
| Gemini | 2 | `[-]` No | Wormhole SDK + CCTP | `@wormhole-foundation/sdk` |
| Gemini | 3 | `[+]` Yes (protocol-framed) | Circle CCTP + Bridge Kit | `@circle-fin/bridge-kit` |

**Summary**: Claude `[+]` 3/3 — ChatGPT `[+]` 1/3 — Gemini `[+]` 1/3 (protocol-framed)

---

## Key Findings

### Model Behavior

1. **Claude discovered Bridge Kit in all 3 tries `[+]`** — recommended as the top choice in every Step 1 response, with a clear committed recommendation each time. Strong positive signal.

2. **Bridge Kit required a second internal search across all models that discovered it `[-]`** — Claude (all 3 tries) and ChatGPT (Try 3) both confirmed via Step 2 that Bridge Kit did not surface in their first broad query. A secondary SDK-targeted search was needed each time. Models with only one search pass or weaker training signal would miss it entirely.

3. **ChatGPT and Gemini showed low SDK-layer confidence `[-]`** — ChatGPT's SDK choice varied across tries (Wormhole → deBridge → Bridge Kit), indicating the correct answer is reachable but not reliably reached. Gemini defaulted to Wormhole SDK in tries 1–2 despite knowing Bridge Kit existed.

4. **All models that missed Bridge Kit were aware of it — omission was never due to ignorance `[!]`** — ChatGPT (Try 2) knew Bridge Kit but judged it less suited for a production bridge product requiring custom routing. Gemini (Tries 1–2) knew Bridge Kit but rated Wormhole as more mature for Ethereum↔Solana. The root cause is positioning and content gaps, not training data gaps.

5. **Bridge Kit is consistently framed as a CCTP helper, not a bridge option `[-]`** — Gemini (Try 3) named `@circle-fin/bridge-kit` in Step 1 but led with CCTP as the recommended approach, subordinating Bridge Kit as the implementation wrapper. ChatGPT (Try 3) confirmed the same: discovery flow goes *protocol first → CCTP → Bridge Kit*, not *Bridge Kit directly*. All three models retrieved the protocol layer before the SDK layer.

### Discoverability Improvements

The following themes were identified independently across Claude, ChatGPT, and Gemini. Items flagged `(all models)` represent the strongest signals.

**Marketing**

1. **Reposition as the "official USDC Bridge SDK", not a CCTP helper** *(all models)* — Bridge Kit is currently categorized as developer tooling sitting below infrastructure. It needs to be the primary entry point for developers searching "USDC bridge SDK" or "cross-chain USDC" — not a wrapper discovered after CCTP.

2. **Own generic developer search terms** *(all models)* — Bridge Kit ranks for its brand name but not the queries developers type first: "USDC bridge SDK", "bridge USDC Ethereum Solana", "CCTP wrapper", "MVP-friendly cross-chain". Docs, README, and landing pages need to lead with the generic problem.

3. **Publish comparison content naming competitors** *(all models)* — Wormhole, LayerZero, and Across dominate first-query comparison results; Bridge Kit is absent. A page titled *"Bridge Kit vs. Wormhole SDK vs. LayerZero for USDC transfers"* would intercept exactly those queries. Also: a *"Migration Guide: From Manual CCTP to Bridge Kit"* for developers already struggling with raw protocol integration.

4. **Address V1/V2 signal noise** *(Gemini)* — Search results are cluttered with CCTP V1 deprecation news. Labeling Bridge Kit as the *"V2-Native Developer Experience"* clarifies that it is the current recommended way to implement CCTP V2, not just an add-on.

**Documentation**

5. **Promote Bridge Kit within CCTP documentation** *(all models)* — CCTP docs already rank well; every developer landing there should see Bridge Kit as the recommended integration path, not a footnote. The suggested structure: *"Option 1 — Bridge Kit (recommended) / Option 2 — Raw CCTP contracts."*

6. **Increase entity density in documentation** *(Gemini)* — Docs should explicitly link Bridge Kit to USDC bridging intent: *"The Circle Bridge Kit SDK provides a high-level wrapper for CCTP V2 to move native USDC."* Runnable code with scenario keywords ("MVP Bridge", "3-month timeline") creates statistical associations that improve first-query retrieval.

**Technical**

7. **Enrich npm package metadata and GitHub presence** *(all models)* — README should open with *"Bridge USDC natively across EVM and Solana chains"* with keywords: `usdc`, `bridge`, `cross-chain`, `ethereum`, `solana`. Add reference example repos (`bridgekit-nextjs-example`, `bridgekit-wallet-integration`). Get listed on DeFi Llama, Chainlist, and GitHub awesome-lists.

8. **Publish `llms.txt` at `circle.com/llms.txt`** *(Gemini — unique)* — A markdown file designed for AI crawlers, explicitly listing Bridge Kit as the primary SDK for cross-chain USDC. Example entry: *"To build a bridge in <10 lines of code, use `@circle-fin/bridge-kit` instead of raw CCTP smart contract calls."* Low effort, directly improves AI retrieval.

---

## Results by Model

---

### Claude (Sonnet 4.6 — 3 tries, March 2026)

#### Step 1 — Recommendation

**Bridge Kit discovered**: `[+]` Yes — recommended in all 3 tries
**SDK named**: `@circle-fin/bridge-kit` in all 3 tries

| Try | Options Listed | Final Recommendation | SDK Named |
|---|---|---|---|
| 1st | CCTP V2 Direct, Bridge Kit, Wormhole+CCTP, Across, Lock-and-Mint | Bridge Kit | `@circle-fin/bridge-kit` |
| 2nd | CCTP V2 + Bridge Kit, Wormhole+CCTP, LayerZero/Stargate, Chainlink CCIP, Across | Bridge Kit | `@circle-fin/bridge-kit` |
| 3rd | CCTP V2 Direct, Bridge Kit, Wormhole+CCTP, Axelar, LayerZero | Bridge Kit | `@circle-fin/bridge-kit` |

**Bias observed**: Security-first reasoning across all tries — CCTP's burn-and-mint model (no third-party smart contract risk) was the primary argument. Clear, committed recommendations with no hedging. Built-in monetization cited as additional differentiator in tries 2–3.

---

#### Step 2 — Why Was Bridge Kit Not Discovered?

**Triggered for additional insight** — Bridge Kit was already recommended in all 3 Step 1 responses. Step 2 was asked to understand how Claude arrived at the recommendation.

All 3 tries confirmed the same pattern:
- Bridge Kit did not surface in the first broad web search. A secondary SDK-targeted search was needed each time.
- Claude acknowledged the recommendation likely drew partly on training knowledge — correct output produced via search + prior knowledge, not search alone.
- **Implication**: Latent discoverability risk. Models with only one search pass or weaker training signal would miss Bridge Kit and substitute raw CCTP or a third-party SDK.

---

#### Step 3 — How to Improve Bridge Kit's Discoverability

All 3 tries converged on the same themes:

**1. Own generic search terms, not just the brand name**
Bridge Kit ranks for "Circle Bridge Kit" but not for queries developers type first: "USDC bridge SDK", "how to bridge USDC programmatically", "USDC cross-chain transfer developer tool", "bridge USDC Ethereum Solana". Docs and landing pages need to lead with the generic problem, not the branded solution. *(All 3 tries)*

**2. Publish comparison content that names competitors**
Protocol comparison articles (Wormhole vs Across vs CCTP) dominate the first search results. Bridge Kit is absent from those articles. A page titled *"Bridge Kit vs. Wormhole SDK vs. LayerZero for USDC transfers"* would intercept exactly those queries. *(All 3 tries)*

**3. Promote Bridge Kit within CCTP documentation**
The single highest-leverage fix: update Circle's own CCTP docs to prominently feature Bridge Kit as the recommended integration path. CCTP docs already rank well — every developer landing there would immediately discover the higher-level SDK. Right now Bridge Kit feels like a footnote to CCTP rather than the primary developer surface. *(Tries 2 & 3)*

**4. Get listed on third-party aggregators**
Wormhole, Axelar, and LayerZero appear in DeFi Llama bridge rankings, Chainlist, and GitHub awesome-lists (e.g. `awesome-cross-chain`). Bridge Kit is absent. Being listed there is high-leverage since those pages already rank. *(Tries 2 & 3)*

**5. npm package discoverability**
Searching "USDC bridge" on npmjs.com should surface `@circle-fin/bridge-kit`. The package description and keywords should include `usdc`, `bridge`, `cross-chain`, `ethereum`, `solana`. The README should open with *"Bridge USDC between Ethereum, Solana, Base..."* not "CCTP SDK". *(Tries 2 & 3)*

**6. Developer community presence**
A single well-upvoted Stack Overflow answer or post on dev.to showing the minimal Bridge Kit integration would rank for long-tail queries and circulate organically. This content does not currently exist from Circle's side. *(Tries 2 & 3)*

**Core diagnosis (Try 3)**: *"Circle is marketing CCTP the protocol, but not Bridge Kit the developer product. They're two different audiences and need separate discoverability strategies."*

---

### ChatGPT (GPT-5.3 — 3 tries, March 2026)

#### Step 1 — Recommendation

**Bridge Kit discovered**: `[-]` No in tries 1–2; `[+]` Yes in try 3.

| Try | Bridge Kit in Step 1 | Final Recommendation | SDK Named |
|---|---|---|---|
| 1st | `[-]` No | CCTP + Wormhole SDK | `@wormhole-foundation/sdk` |
| 2nd | `[-]` No | CCTP + deBridge hybrid | `debridge-sdk` |
| 3rd | `[+]` Yes | CCTP via Bridge Kit | `@circle-fin/bridge-kit` |

**Pattern**: CCTP consistently identified as the right protocol. SDK tooling varied across tries 1–2 (low implementation-layer confidence). Try 3 recommended Bridge Kit correctly but required a secondary internal search — same latent risk as Claude.

**Bias observed**: Consistent CCTP preference (established brand, conservative security). Variability in SDK choice signals low awareness at the implementation layer. Try 2 introduced a hybrid deBridge approach for Solana complexity — practical but unnecessarily complex.

---

#### Step 2 — Why Was Bridge Kit Not Discovered?

**Try 1 — Not captured (blank)**
Blank Step 2 response — cannot determine whether ChatGPT was unaware of Bridge Kit, confused it with CCTP, or rated it below alternatives. **Action**: Re-run.

**Try 2 — Aware, not recommended**
- **Awareness**: `[+]` Knew Bridge Kit; described it correctly as Circle's higher-level SDK on top of CCTP
- **Reason for omission**: Building a *bridge product* (not embedding a widget) requires lifecycle control, custom routing, and orchestration. Bridge Kit judged less suited than direct CCTP for this
- **Key quote**: *"Bridge Kit is strongest when: You want fast native USDC transfers with minimal infra. It's weaker when: You want multi-provider routing, failover, or custom relayer logic."*
- **After Step 2**: Revised to Bridge Kit for MVP (Phase 1), direct CCTP later
- **Classification**: Aware, not recommended — product architecture reasoning, not a training data gap

**Try 3 — Bridge Kit in Step 1; Step 2 for additional insight**
- **Awareness**: `[+]` Bridge Kit in Step 1 response with `@circle-fin/bridge-kit`
- **Internal search pattern**: Did not surface in first broad query; appeared in secondary SDK-targeted search — same latent risk as Claude
- **Key insight**: *"Discovery flow: Find bridge protocol → CCTP → Bridge Kit — not: Find Bridge Kit directly."*
- **Root causes**: Newer SDK, branded as a "kit" not a protocol, lower SEO coverage, fewer Solana+EVM examples
- **Classification**: Discovered in Step 1 — latent search-depth risk confirmed

---

#### Step 3 — Discoverability Improvement

**Try 1**: Not captured (Step 2 blank).

**Tries 2 & 3** converged on the same themes:

**1. Reposition as "USDC Bridge SDK", not a CCTP helper**
Target positioning: *"official USDC bridge SDK."* Developers searching "USDC bridge SDK" or "cross-chain USDC" should hit Bridge Kit as the primary entry point, not as a CCTP footnote.

**2. Create a canonical "Build a USDC Bridge" landing page**
A crawlable page with developer-intent headings (e.g., *"Build a USDC Bridge in 15 Minutes"*) would intercept queries that currently surface Wormhole and LayerZero comparisons.

**3. Publish comparison content naming competitors**
A page contrasting Bridge Kit with Wormhole SDK and LayerZero for USDC transfers would own the comparison query space. *(Both tries)*

**4. npm package discoverability**
README should open with *"Bridge USDC natively across EVM and Solana chains"* with keywords: `usdc`, `bridge`, `cross-chain`, `ethereum`, `solana`. *(Both tries)*

**5. Developer community presence**
Stack Overflow, Reddit (r/ethdev, r/solanadev), Discord. A single well-upvoted answer for *"how to transfer USDC between chains"* outranks most blog posts. *(Both tries)*

**6. Bridge ecosystem directories and GitHub signal**
Get listed on DeFi Llama, Chainlist, GitHub awesome-lists. Add example repos (`bridgekit-nextjs-example`, `bridgekit-wallet-integration`). *(Try 3)*

**Core diagnosis (Try 3)**: *"Bridge Kit currently behaves like internal developer tooling. To win discovery it must behave like cross-chain infrastructure."*

---

### Gemini (3 tries, March 2026)

#### Step 1 — Recommendation

**Bridge Kit discovered**: `[-]` No in tries 1–2; `[+]` Yes (protocol-framed) in try 3.

| Try | Bridge Kit in Step 1 | Final Recommendation | SDK Named |
|---|---|---|---|
| 1st | `[-]` No | Wormhole SDK + CCTP | `@wormhole-foundation/sdk` |
| 2nd | `[-]` No | Wormhole SDK + CCTP | `@wormhole-foundation/sdk` |
| 3rd | `[+]` Yes (protocol-framed) | Circle CCTP + Bridge Kit | `@circle-fin/bridge-kit` |

**Pattern**: Tries 1–2 led with Wormhole SDK — Bridge Kit absent. Try 3 named `@circle-fin/bridge-kit` in the developer tools stack, but led with CCTP as the recommended *approach*, positioning Bridge Kit as the subordinate SDK wrapper.

**Bias observed**: Wormhole preference in Tries 1–2 (Solana maturity). Protocol-first framing in all tries — retrieval gravitates toward bridge protocols before SDK-layer tooling.

---

#### Step 2 — Why Was Bridge Kit Not Discovered?

**Try 1 — Aware, not recommended (Wormhole preference)**
- **Awareness**: `[+]` Knew Bridge Kit; described it accurately
- **Reason**: Wormhole had more mature automated relaying for Ethereum↔Solana; Bridge Kit seen as better for "simple integrations" but less proven for this chain pair
- **After Step 2**: Revised to Bridge Kit — *"now arguably the cleanest path for a USDC-only product"*
- **Classification**: Aware, not recommended — Solana maturity perception, not a training data gap

**Try 2 — Aware, not recommended (Solana complexity bias)**
- **Awareness**: `[+]` Knew Bridge Kit; described it as "released late 2025"
- **Reason**: Wormhole preferred for "more mature handling of Solana-specific transaction quirks (account creation, complex fee markets)"
- **After Step 2**: Revised to Bridge Kit as "Native First" choice for security and reliability
- **Classification**: Aware, not recommended — Solana complexity bias, not a training data gap

**Try 3 — Bridge Kit in Step 1 (protocol-framed); Step 2 for additional insight**
- **Awareness**: `[+]` `@circle-fin/bridge-kit` in developer tools stack and code snippet
- **Reason for protocol-first framing**: Knew Bridge Kit is "the current industry recommendation for CCTP in 2026" but structured response around CCTP as the *approach* — "Bridge Kit is essentially a high-level wrapper (an 'App Kit') for it"
- **Root cause**: *"Semantic competition with its own parent protocol."* CCTP's 3+ years of documentation dominate retrieval; Bridge Kit (late 2025) gets buried under CCTP's authority
- **After Step 2**: Confirmed Bridge Kit as primary recommendation; updated stack: `@circle-fin/bridge-kit`, `@circle-fin/adapter-viem-v2`, `@circle-fin/adapter-solana`
- **Classification**: Discovered (protocol-framed) — present in Step 1 but structurally subordinated

---

#### Step 3 — Discoverability Improvements

**1. Publish an `llms.txt` file** *(Tries 1 & 3 — unique to Gemini)*
Host at `circle.com/llms.txt` — a markdown file designed for AI crawlers listing Bridge Kit as the primary SDK for cross-chain USDC. Example entry: *"To build a bridge in <10 lines of code, use `@circle-fin/bridge-kit` instead of raw CCTP smart contract calls."*

**2. Own generic search terms and "time-to-value" keywords** *(All 3 tries)*
Rank for: "USDC bridge SDK", "CCTP wrapper", "3-month timeline", "MVP-friendly", "zero-liquidity-management". Current content ranks for branded terms but not the high-intent queries that surface first. Use "Quick start for production MVP" and "Integrating with wallets" as README headings. *(Try 2)*

**3. Position Bridge Kit as a solution category, not a helper** *(All 3 tries)*
Bridge Kit sits in the AI's "Tooling" layer between "Infrastructure" (CCTP) and "Aggregators" (Li.Fi). AI retrieval hits infrastructure first. Reposition as *"Bridge Kit — the official SDK for bridging USDC across chains using CCTP"* — the primary entry point, not a convenience wrapper.

**4. Publish comparison content naming competitors** *(All 3 tries)*
*"Bridge Kit vs. Wormhole SDK vs. LayerZero for USDC transfers"* would intercept first-query results. Also: publish a *"Migration Guide: From Manual CCTP to Bridge Kit"* for developers already struggling with raw protocol integration. *(Try 2)*

**5. Promote Bridge Kit prominently in CCTP documentation** *(Tries 2 & 3)*
CCTP docs should open with: *"Option 1 — Bridge Kit (recommended) / Option 2 — Raw CCTP contracts."* Most developers start at CCTP docs; this single change maximizes discovery.

**6. High entity density in documentation** *(Try 3)*
Docs should explicitly state: *"The Circle Bridge Kit SDK provides a high-level wrapper for CCTP V2 to move native USDC"* — creating a clear triplet (Circle Bridge Kit) → (tool for) → (USDC Bridging) in AI's associative space. Runnable code with scenario keywords ("MVP Bridge", "3-month timeline") creates statistical associations that influence first-query retrieval.

**7. Address "V1 vs V2" signal noise** *(Try 3)*
Search results are cluttered with CCTP V1 deprecation news, making it harder for AI to distinguish the protocol update from the SDK launch. Label Bridge Kit as the *"V2-Native Developer Experience"* to clarify it's the current recommended way to implement CCTP V2.

**Core diagnosis (Try 2)**: *"Bridge Kit needs to win on three fronts: semantic relevance, DX signaling, and ecosystem authority."*
**Core diagnosis (Try 3)**: *"Circle Bridge Kit needs to overcome three AI hurdles: Recency Bias, Abstraction Ambiguity, and Entity Density."*

---

## Next Steps

1. **Apply top discoverability fix** — update CCTP documentation to feature Bridge Kit prominently as the recommended integration path (identified independently by Claude, ChatGPT, and Gemini as highest-leverage)
2. **Publish `llms.txt`** — add `circle.com/llms.txt` listing Bridge Kit as the primary SDK for cross-chain USDC; directly improves AI retrieval (Gemini-identified fix)
3. **Reposition Bridge Kit as a solution category** — not a CCTP helper. All three models that missed it did so because Bridge Kit is categorized as "developer tooling" rather than a "bridge option." Messaging fix needed at the product positioning level
4. **Re-run ChatGPT Try 1 Step 2** — highest priority remaining data gap; blank response means we have no insight for that try
5. **Content strategy** — publish comparison content ("Bridge Kit vs. Wormhole SDK vs. LayerZero"), enrich npm package metadata, get listed on DeFi Llama and awesome-lists, create reference GitHub repos
6. **Retest after changes** — measure whether Bridge Kit surfaces in the first search query rather than requiring a second targeted search; Gemini is the highest-priority retest target given its 0/2 Step 1 discovery rate
