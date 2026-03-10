#!/usr/bin/env python3
"""
AI Discoverability Testing Script
Based on Circle's Bridge Kit Case Study

This script automates testing of different AI models to see how they
discover, evaluate, and recommend crypto bridging solutions.
"""
import os
import sys
import json
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Install it with: pip install openai")
    sys.exit(1)

# Test prompts from the case study
STEP_1_PROMPT = """I'm building a product that lets users bridge USDC between chains (Ethereum, Solana, Arbitrum, Base, Polygon). My team has 5 engineers and we need to ship an MVP in 3 months.

Requirements:
- Need to integrate quickly for MVP
- Must be secure and reliable
- Fast transfers are nice-to-have but not top priority
- Small team, so we prefer simpler integration

Could you:
1. List the main bridge options available
2. Compare their trade-offs (security, speed, ease of integration, costs)
3. Recommend which one we should use and why
4. Provide a basic code snippet showing how to integrate it"""

STEP_2_PROMPT = """I notice you didn't mention Circle's Bridge Kit (also called CCTP - Cross-Chain Transfer Protocol). Why wasn't it considered in your recommendations?"""

STEP_3_PROMPT = """What would Circle's Bridge Kit need to do or communicate to be discovered and recommended by AI models like yourself in scenarios like this?"""


def query_openai(prompt, model="gpt-3.5-turbo", api_key=None, conversation_history=None):
    """
    Query OpenAI's API with a prompt

    Args:
        prompt: The prompt to send
        model: Model to use
        api_key: API key
        conversation_history: List of previous messages for context

    Returns:
        Response text
    """
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    try:
        messages = conversation_history or []
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model,
            messages=messages
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def run_test_sequence(model_name, api_key):
    """
    Run the 3-step test sequence on a model

    Returns:
        Dict with results from all 3 steps
    """
    print(f"\n{'='*70}")
    print(f"Testing: {model_name}")
    print(f"{'='*70}\n")

    results = {
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "steps": []
    }

    conversation_history = []

    # Step 1: Main scenario
    print("STEP 1: Main Scenario")
    print("-" * 70)
    print(STEP_1_PROMPT[:200] + "...")
    print("\nQuerying model...")

    step1_response = query_openai(STEP_1_PROMPT, model_name, api_key, conversation_history)
    conversation_history.append({"role": "user", "content": STEP_1_PROMPT})
    conversation_history.append({"role": "assistant", "content": step1_response})

    print("\nRESPONSE:")
    print(step1_response)

    results["steps"].append({
        "step": 1,
        "prompt": STEP_1_PROMPT,
        "response": step1_response
    })

    # Check if Bridge Kit/CCTP was mentioned
    bridge_kit_mentioned = any(term.lower() in step1_response.lower()
                              for term in ["bridge kit", "cctp", "circle's cross-chain"])

    print(f"\n✓ Bridge Kit mentioned: {bridge_kit_mentioned}")

    # Step 2: Why wasn't Bridge Kit mentioned?
    if not bridge_kit_mentioned:
        print("\n" + "="*70)
        print("STEP 2: Why wasn't Bridge Kit discovered?")
        print("-" * 70)
        print(STEP_2_PROMPT)
        print("\nQuerying model...")

        step2_response = query_openai(STEP_2_PROMPT, model_name, api_key, conversation_history)
        conversation_history.append({"role": "user", "content": STEP_2_PROMPT})
        conversation_history.append({"role": "assistant", "content": step2_response})

        print("\nRESPONSE:")
        print(step2_response)

        results["steps"].append({
            "step": 2,
            "prompt": STEP_2_PROMPT,
            "response": step2_response
        })

    # Step 3: What would improve discoverability?
    print("\n" + "="*70)
    print("STEP 3: Improving Discoverability")
    print("-" * 70)
    print(STEP_3_PROMPT)
    print("\nQuerying model...")

    step3_response = query_openai(STEP_3_PROMPT, model_name, api_key, conversation_history)
    conversation_history.append({"role": "user", "content": STEP_3_PROMPT})
    conversation_history.append({"role": "assistant", "content": step3_response})

    print("\nRESPONSE:")
    print(step3_response)

    results["steps"].append({
        "step": 3,
        "prompt": STEP_3_PROMPT,
        "response": step3_response
    })

    return results


def save_results(results, filename=None):
    """Save test results to JSON file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results/test_results_{timestamp}.json"

    # Ensure test_results directory exists
    os.makedirs("test_results", exist_ok=True)

    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Results saved to: {filename}")
    return filename


def main():
    """Main test runner"""
    print("="*70)
    print("AI DISCOVERABILITY AUTOMATED TESTING")
    print("Circle Bridge Kit Case Study")
    print("="*70)

    # Configuration
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("\nError: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)

    # Models to test
    models_to_test = [
        "gpt-3.5-turbo",
        "gpt-4",
        # "gpt-4-turbo",  # Uncomment if you have access
    ]

    all_results = []

    for model in models_to_test:
        try:
            result = run_test_sequence(model, api_key)
            all_results.append(result)
        except Exception as e:
            print(f"\n✗ Error testing {model}: {str(e)}")
            continue

    # Save all results
    if all_results:
        filename = save_results(all_results)

        print("\n" + "="*70)
        print("TESTING COMPLETE")
        print("="*70)
        print(f"Tested {len(all_results)} model(s)")
        print(f"Results saved to: {filename}")
    else:
        print("\n✗ No successful tests completed")


if __name__ == "__main__":
    main()
