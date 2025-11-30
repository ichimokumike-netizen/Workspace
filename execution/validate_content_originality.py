"""
Script: validate_content_originality.py
Purpose: Ensure content is original, not plagiarized, and provides real value
Inputs: Content text or file path
Outputs: Originality validation report
Author: AI-Assisted
Created: 2025-11-29

CRITICAL RULES - CONTENT ORIGINALITY:
1. No plagiarism - content must be original
2. Must provide unique insights, not just regurgitated information
3. Examples must be specific and actionable (not generic)
4. Frameworks/systems must be presented in an original way
5. Real value that customers can actually use
"""

import re
from collections import Counter


# PLAGIARISM RED FLAGS - These indicate lazy/copied content
PLAGIARISM_INDICATORS = {
    "generic_phrases": [
        "in today's world",
        "it goes without saying",
        "needless to say",
        "at the end of the day",
        "the fact of the matter is",
        "in conclusion",
        "as we all know",
        "it is what it is",
    ],
    "vague_language": [
        "some experts say",
        "studies show",
        "research indicates",
        "many people",
        "it has been shown",
        "commonly known",
        "widely accepted",
        "generally speaking",
    ],
    "filler_words": [
        "very",
        "really",
        "quite",
        "just",
        "simply",
        "basically",
        "actually",
        "literally",
    ],
}


# ORIGINALITY REQUIREMENTS
ORIGINALITY_MARKERS = {
    "specific_numbers": r'\d+%|\d+ hours|\d+ days|\$\d+',  # Specific metrics
    "actionable_steps": r'(Step \d+:|Day \d+:|Week \d+:|\d+\. )',  # Clear steps
    "concrete_examples": r'Example:|Case Study:|Try This:|Pro Tip:',  # Specific examples
    "unique_frameworks": r'(Formula:|System:|Framework:|Blueprint:|Method:)',  # Original systems
}


def analyze_sentence_complexity(content):
    """
    Analyze if content has varied sentence structure (not templated).

    Returns:
        dict: Complexity metrics
    """
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    if not sentences:
        return {"score": 0, "issue": "No sentences found"}

    # Calculate sentence length variance
    lengths = [len(s.split()) for s in sentences]
    avg_length = sum(lengths) / len(lengths)
    variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)

    # Check for repetitive patterns
    sentence_starts = [s.split()[0].lower() if s.split() else "" for s in sentences]
    start_variety = len(set(sentence_starts)) / len(sentence_starts) if sentence_starts else 0

    complexity_score = min(100, int((variance / 10) * 50 + start_variety * 50))

    return {
        "score": complexity_score,
        "avg_sentence_length": round(avg_length, 1),
        "sentence_variety": round(start_variety * 100, 1),
        "total_sentences": len(sentences)
    }


def check_specificity(content):
    """
    Check if content contains specific, actionable information.

    Returns:
        dict: Specificity metrics
    """
    word_count = len(content.split())

    # Count specific numbers/metrics
    numbers = len(re.findall(ORIGINALITY_MARKERS["specific_numbers"], content))

    # Count actionable steps
    steps = len(re.findall(ORIGINALITY_MARKERS["actionable_steps"], content))

    # Count concrete examples
    examples = len(re.findall(ORIGINALITY_MARKERS["concrete_examples"], content))

    # Count frameworks/systems
    frameworks = len(re.findall(ORIGINALITY_MARKERS["unique_frameworks"], content))

    # Calculate specificity score
    # Expect at least 1 specific element per 100 words
    expected_elements = word_count / 100
    actual_elements = numbers + steps + examples + frameworks

    specificity_ratio = min(100, int((actual_elements / expected_elements) * 100))

    return {
        "score": specificity_ratio,
        "specific_numbers": numbers,
        "actionable_steps": steps,
        "concrete_examples": examples,
        "frameworks": frameworks,
        "specificity_per_100_words": round(actual_elements / (word_count / 100), 2)
    }


def detect_plagiarism_indicators(content):
    """
    Detect signs of lazy/plagiarized content.

    Returns:
        dict: Plagiarism risk assessment
    """
    content_lower = content.lower()
    word_count = len(content.split())

    issues = []
    issue_count = 0

    # Check for generic phrases
    generic_found = []
    for phrase in PLAGIARISM_INDICATORS["generic_phrases"]:
        if phrase in content_lower:
            generic_found.append(phrase)
            issue_count += 1

    if generic_found:
        issues.append(f"Generic phrases: {', '.join(generic_found[:3])}")

    # Check for vague language
    vague_found = []
    for phrase in PLAGIARISM_INDICATORS["vague_language"]:
        if phrase in content_lower:
            vague_found.append(phrase)
            issue_count += 1

    if vague_found:
        issues.append(f"Vague language: {', '.join(vague_found[:3])}")

    # Check for excessive filler words
    filler_count = 0
    for word in PLAGIARISM_INDICATORS["filler_words"]:
        filler_count += content_lower.count(f" {word} ")

    filler_ratio = (filler_count / word_count) * 100 if word_count > 0 else 0

    if filler_ratio > 2:  # More than 2% filler words
        issues.append(f"Excessive filler words: {filler_ratio:.1f}% of content")
        issue_count += int(filler_ratio)

    # Calculate plagiarism risk score (inverse - lower is better)
    risk_score = max(0, 100 - (issue_count * 10))

    return {
        "score": risk_score,
        "issues_found": issues,
        "generic_phrases_count": len(generic_found),
        "vague_language_count": len(vague_found),
        "filler_ratio": round(filler_ratio, 2)
    }


def check_unique_value(content):
    """
    Assess if content provides unique, valuable insights.

    Returns:
        dict: Value assessment
    """
    # Check for actionable advice ratio
    actionable_keywords = [
        "how to", "step", "try this", "action", "implement", "apply",
        "use this", "start by", "begin with", "first", "next", "then"
    ]

    content_lower = content.lower()
    actionable_count = sum(content_lower.count(keyword) for keyword in actionable_keywords)
    word_count = len(content.split())

    actionable_ratio = (actionable_count / (word_count / 100)) if word_count > 0 else 0

    # Check for practical examples
    example_markers = ["example:", "case study:", "real-world", "scenario:", "situation:"]
    example_count = sum(content_lower.count(marker) for marker in example_markers)

    # Check for templates/tools
    tool_markers = ["template", "checklist", "worksheet", "tool", "framework", "system"]
    tool_count = sum(content_lower.count(marker) for marker in tool_markers)

    # Calculate value score
    value_score = min(100, int(
        (actionable_ratio * 30) +
        (example_count * 10) +
        (tool_count * 5)
    ))

    return {
        "score": value_score,
        "actionable_ratio": round(actionable_ratio, 2),
        "example_count": example_count,
        "tool_count": tool_count,
        "provides_real_value": value_score >= 70
    }


def validate_content_originality(content, min_score=70):
    """
    Comprehensive originality validation.

    Args:
        content: The content text to validate
        min_score: Minimum passing score (default 70/100)

    Returns:
        dict: Complete validation report
    """

    # Run all checks
    complexity = analyze_sentence_complexity(content)
    specificity = check_specificity(content)
    plagiarism = detect_plagiarism_indicators(content)
    value = check_unique_value(content)

    # Calculate overall originality score (weighted average)
    overall_score = int(
        (complexity["score"] * 0.20) +      # 20% - varied writing
        (specificity["score"] * 0.30) +     # 30% - specific details
        (plagiarism["score"] * 0.25) +      # 25% - not plagiarized
        (value["score"] * 0.25)             # 25% - real value
    )

    # Determine pass/fail
    passes = overall_score >= min_score

    # Compile issues
    all_issues = []

    if complexity["score"] < 60:
        all_issues.append("Content lacks sentence variety (repetitive structure)")

    if specificity["score"] < 60:
        all_issues.append("Not enough specific examples/numbers/actionable steps")

    if plagiarism["score"] < 60:
        all_issues.append("Contains plagiarism indicators (generic phrases, vague language)")

    if value["score"] < 60:
        all_issues.append("Lacks actionable value (too theoretical, not enough practical advice)")

    all_issues.extend(plagiarism["issues_found"])

    # Generate recommendations
    recommendations = []

    if specificity["score"] < 70:
        recommendations.append("Add more specific numbers, percentages, timeframes (e.g., '10 hours', '3 weeks', '50%')")

    if value["score"] < 70:
        recommendations.append("Include more 'Try This:', 'Example:', 'Step-by-step' sections")

    if plagiarism["score"] < 70:
        recommendations.append("Remove generic phrases and replace with specific, original language")

    if complexity["score"] < 70:
        recommendations.append("Vary sentence structure - mix short punchy sentences with longer detailed ones")

    return {
        "overall_score": overall_score,
        "passes_validation": passes,
        "min_required_score": min_score,
        "component_scores": {
            "complexity": complexity["score"],
            "specificity": specificity["score"],
            "non_plagiarism": plagiarism["score"],
            "value": value["score"]
        },
        "detailed_metrics": {
            "complexity": complexity,
            "specificity": specificity,
            "plagiarism_check": plagiarism,
            "value_assessment": value
        },
        "issues": all_issues,
        "recommendations": recommendations,
        "word_count": len(content.split())
    }


def print_validation_report(result):
    """Print comprehensive validation report"""

    print(f"\n{'='*80}")
    print(f">>> CONTENT ORIGINALITY VALIDATION REPORT")
    print(f"{'='*80}")

    print(f"\nOverall Score: {result['overall_score']}/100")
    print(f"Status: {'PASS' if result['passes_validation'] else 'FAIL'}")
    print(f"Word Count: {result['word_count']:,}")

    print(f"\nComponent Scores:")
    print(f"  Complexity (sentence variety): {result['component_scores']['complexity']}/100")
    print(f"  Specificity (concrete details): {result['component_scores']['specificity']}/100")
    print(f"  Non-Plagiarism (originality): {result['component_scores']['non_plagiarism']}/100")
    print(f"  Value (actionable content): {result['component_scores']['value']}/100")

    if result['issues']:
        print(f"\nIssues Found ({len(result['issues'])}):")
        for i, issue in enumerate(result['issues'][:5], 1):
            print(f"  {i}. {issue}")
        if len(result['issues']) > 5:
            print(f"  ... and {len(result['issues']) - 5} more")

    if result['recommendations']:
        print(f"\nRecommendations:")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"  {i}. {rec}")

    # Detailed metrics
    specs = result['detailed_metrics']['specificity']
    print(f"\nSpecificity Details:")
    print(f"  Specific numbers/metrics: {specs['specific_numbers']}")
    print(f"  Actionable steps: {specs['actionable_steps']}")
    print(f"  Concrete examples: {specs['concrete_examples']}")
    print(f"  Frameworks/systems: {specs['frameworks']}")

    value = result['detailed_metrics']['value_assessment']
    print(f"\nValue Assessment:")
    print(f"  Actionable advice ratio: {value['actionable_ratio']} per 100 words")
    print(f"  Real examples: {value['example_count']}")
    print(f"  Tools/templates: {value['tool_count']}")

    print(f"\n{'='*80}")

    if not result['passes_validation']:
        print(f"\n[CRITICAL] Content FAILS originality validation")
        print(f"[ACTION] Address issues above before publishing")
    else:
        print(f"\n[SUCCESS] Content passes originality validation")
        print(f"[READY] Content is original and provides real value")

    print(f"{'='*80}\n")


def main():
    """Test content originality validation"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python validate_content_originality.py <file_path>")
        print("\nExample:")
        print("  python validate_content_originality.py .tmp/content_example.md")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    result = validate_content_originality(content)
    print_validation_report(result)

    sys.exit(0 if result['passes_validation'] else 1)


if __name__ == "__main__":
    main()
