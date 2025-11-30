"""
Script: generate_benefit_driven_title.py
Purpose: Generate benefit-driven titles that instantly communicate value
Inputs: Topic, optional context
Outputs: Compelling, benefit-focused title
Author: AI-Assisted
Created: 2025-11-29

TITLE RULES (MUST FOLLOW):
1. Lead with the benefit (what the reader gets/achieves)
2. Be specific and concrete (not vague)
3. Use action-oriented language
4. Communicate value instantly
5. Make it scannable and compelling
"""

import re


# TITLE FORMULA TEMPLATES - All benefit-driven
TITLE_FORMULAS = {
    "achievement": "{Outcome}: {Method}",
    "transformation": "{Start State} to {End State}: {Timeframe}",
    "solution": "{Problem Solved}: {How}",
    "guide": "{Benefit}: Complete {Resource Type}",
    "mastery": "{Skill/Topic} Mastery: {Key Benefit}",
    "actionable": "How to {Achieve Benefit} {Timeframe/Constraint}",
}


# BENEFIT KEYWORDS - Use these to lead titles
BENEFIT_KEYWORDS = [
    "master", "achieve", "build", "create", "earn", "save", "gain",
    "grow", "increase", "improve", "optimize", "maximize", "scale",
    "launch", "start", "accelerate", "transform", "unlock", "discover"
]


def validate_title_is_benefit_driven(title):
    """
    Validate that a title follows benefit-driven rules.

    Returns:
        dict: {
            "valid": bool,
            "score": int (0-100),
            "issues": list of problems,
            "suggestions": list of improvements
        }
    """
    issues = []
    suggestions = []
    score = 100

    title_lower = title.lower()

    # Rule 1: Must start with benefit/action (not just topic name)
    starts_with_benefit = any(keyword in title_lower[:30] for keyword in BENEFIT_KEYWORDS)
    if not starts_with_benefit:
        issues.append("Title doesn't lead with benefit or action")
        suggestions.append(f"Start with action verb: {', '.join(BENEFIT_KEYWORDS[:5])}")
        score -= 30

    # Rule 2: Should be specific (avoid vague words)
    vague_words = ["things", "stuff", "ways", "tips", "tricks", "secrets"]
    has_vague = any(word in title_lower for word in vague_words)
    if has_vague:
        issues.append("Title contains vague words")
        suggestions.append("Replace vague words with specific outcomes")
        score -= 20

    # Rule 3: Should communicate timeframe or scope
    has_scope = any(word in title_lower for word in ["complete", "ultimate", "essential", "quick", "comprehensive", "2025", "step-by-step"])
    if not has_scope:
        issues.append("No scope indicator (timeframe/completeness)")
        suggestions.append("Add scope: 'Complete Guide', '2025', 'Quick Start', etc.")
        score -= 15

    # Rule 4: Length check (ideal: 40-70 characters for readability)
    if len(title) < 30:
        issues.append("Title too short (lacks detail)")
        score -= 10
    elif len(title) > 90:
        issues.append("Title too long (hard to scan)")
        score -= 10

    # Rule 5: Should include colon for clarity (benefit: method)
    if ":" not in title:
        issues.append("No colon separator (benefit: method)")
        suggestions.append("Use format: 'Benefit: Method' for clarity")
        score -= 15

    # Rule 6: Avoid starting with generic words
    generic_starts = ["the", "a", "an", "some", "tips", "guide to"]
    starts_generic = any(title_lower.startswith(word) for word in generic_starts)
    if starts_generic:
        issues.append("Starts with generic word")
        suggestions.append("Start with benefit/outcome instead")
        score -= 20

    return {
        "valid": score >= 70,
        "score": max(0, score),
        "issues": issues,
        "suggestions": suggestions
    }


def generate_benefit_title(topic, year=2025, context=None):
    """
    Generate a benefit-driven title for any topic.

    Args:
        topic: The subject matter (e.g., "passive income ideas")
        year: Year to include (default: 2025)
        context: Optional context (tier, audience, etc.)

    Returns:
        dict: {
            "title": The generated title,
            "subtitle": Supporting subtitle,
            "validation": Validation results
        }
    """

    # Extract key components from topic
    topic_clean = topic.lower().replace("how to ", "").replace("guide", "").strip()

    # Determine benefit/outcome based on topic
    benefit_map = {
        "passive income": "Start Earning While You Sleep",
        "chatgpt": "Get 10x Better Results from ChatGPT",
        "ai tools": "Work Smarter with AI-Powered Automation",
        "side hustle": "From Idea to First Dollar in 30 Days",
        "social media": "10x Your Following",
        "time management": "Get More Done in Less Time",
        "email marketing": "Build a List That Prints Money",
        "freelancing": "Build a 6-Figure Freelance Business",
        "content creation": "Create Content That Converts",
        "personal finance": "Master Your Money in 30 Days",
    }

    # Find best matching benefit
    benefit = None
    for keyword, mapped_benefit in benefit_map.items():
        if keyword in topic_clean:
            benefit = mapped_benefit
            break

    # Fallback if no match
    if not benefit:
        # Generate from topic
        words = topic_clean.split()
        action = "Master" if "master" not in topic_clean else "Transform Your"
        benefit = f"{action} {' '.join(words[:3]).title()}"

    # Capitalize first word of topic for title
    topic_title = ' '.join(word.capitalize() for word in topic_clean.split())

    # Generate title using benefit-first formula
    title = f"{topic_title.title()} {year}: Complete Action Guide"
    subtitle = benefit

    # If benefit doesn't contain the word from benefit_keywords, prepend one
    if not any(kw in benefit.lower() for kw in BENEFIT_KEYWORDS):
        # Add action verb
        if "your" in benefit.lower():
            benefit = f"Transform {benefit}"
        else:
            benefit = f"Achieve {benefit}"

    # Validate
    validation = validate_title_is_benefit_driven(title)

    return {
        "title": title,
        "subtitle": subtitle,
        "validation": validation
    }


def print_validation_report(validation):
    """Print validation report in readable format"""
    print(f"\n{'='*80}")
    print(f">>> TITLE VALIDATION REPORT")
    print(f"{'='*80}")
    print(f"Score: {validation['score']}/100")
    print(f"Status: {'PASS' if validation['valid'] else 'FAIL'}")

    if validation['issues']:
        print(f"\nIssues Found:")
        for issue in validation['issues']:
            print(f"  - {issue}")

    if validation['suggestions']:
        print(f"\nSuggestions:")
        for suggestion in validation['suggestions']:
            print(f"  - {suggestion}")

    print(f"{'='*80}\n")


def main():
    """Test title generation"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generate_benefit_driven_title.py <topic>")
        print("\nExample:")
        print("  python generate_benefit_driven_title.py 'passive income ideas'")
        sys.exit(1)

    topic = sys.argv[1]

    print(f"\n{'='*80}")
    print(f">>> BENEFIT-DRIVEN TITLE GENERATOR")
    print(f"{'='*80}")
    print(f"Topic: {topic}\n")

    result = generate_benefit_title(topic)

    print(f"Generated Title: {result['title']}")
    print(f"Subtitle: {result['subtitle']}")

    print_validation_report(result['validation'])

    if not result['validation']['valid']:
        print("[WARNING] Title does not meet benefit-driven standards")
        print("[ACTION] Review suggestions above and regenerate")
    else:
        print("[SUCCESS] Title meets all benefit-driven criteria!")


if __name__ == "__main__":
    main()
