"""
Script: generate_content_with_ai.py
Purpose: Generate complete PDF content using Claude API (fast, single-shot generation)
Inputs: Topic name, target pages, product tier
Outputs: Complete markdown content ready for PDF conversion
Author: AI-Assisted
Created: 2025-11-29
"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


def generate_full_content_with_ai(topic, target_pages=25, tier="tier1"):
    """
    Use Claude API to generate complete PDF content in one call.
    This is MUCH faster than manually writing each page.

    Args:
        topic: The topic to write about
        target_pages: Target number of pages
        tier: Product tier (tier1, tier2, tier3)

    Returns:
        Complete markdown content
    """
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")

    client = Anthropic(api_key=api_key)

    print(f"[*] Generating {target_pages}-page guide on: {topic}")
    print(f"[*] Using Claude API for single-shot generation...")

    # Tier-specific instructions
    tier_specs = {
        "tier1": {
            "pages": "10-20",
            "depth": "Quick, actionable advice. Each page should be scannable with clear takeaways.",
            "style": "Direct and practical. Use bullets, numbered lists, examples.",
            "examples": "2-3 specific examples per major section"
        },
        "tier2": {
            "pages": "30-60",
            "depth": "Comprehensive coverage with step-by-step guidance.",
            "style": "Tutorial-style with detailed explanations and walkthroughs.",
            "examples": "5+ detailed case studies and real-world applications"
        },
        "tier3": {
            "pages": "60+",
            "depth": "Ultimate resource with everything needed to master the topic.",
            "style": "Reference guide + tutorial + templates/worksheets.",
            "examples": "10+ case studies, templates, checklists, and resources"
        }
    }

    spec = tier_specs.get(tier, tier_specs["tier1"])

    # The prompt that generates the entire PDF
    prompt = f"""You are an expert content creator specializing in practical, high-value PDF guides.

Create a complete {target_pages}-page PDF guide on: "{topic}"

**Quality Requirements:**
- {spec['depth']}
- {spec['style']}
- Include {spec['examples']}
- Every section must be ACTIONABLE (not just theory)
- Use real examples, not generic placeholders
- Format in Markdown with clear headers

**Structure Guidelines:**
- Start with compelling intro explaining value
- 5-7 chapters with clear themes
- Each chapter: 3-5 pages of content
- Use ## for chapters, ### for sections
- Liberal use of **bold** for key points
- Bullet lists for scannability
- Include "Try This:" or "Example:" boxes
- End with clear next steps

**Content Standards:**
- No fluff or filler content
- Specific, tactical advice (not vague)
- Each page should teach something new
- Include mistakes to avoid
- Add pro tips and shortcuts
- Use conversational but professional tone

**Target Length:** Approximately {target_pages} pages when formatted (aim for ~400-500 words per page)

Generate the COMPLETE guide now in Markdown format. Start with the title and go all the way to the conclusion.
"""

    try:
        # Single API call to generate entire guide
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=16000,  # Enough for 25-page guide
            temperature=1.0,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        content = response.content[0].text

        print(f"[+] Generated {len(content)} characters of content")
        print(f"[+] Estimated pages: ~{len(content) // 2000}")

        return content

    except Exception as e:
        print(f"[X] API Error: {str(e)}")
        raise


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_content_with_ai.py <topic> [target_pages] [tier]")
        print("\nExample:")
        print("  python generate_content_with_ai.py 'how to use chatgpt effectively' 25 tier1")
        print("\nTiers:")
        print("  tier1 = Quick Guide (10-20 pages, 2hr production)")
        print("  tier2 = Comprehensive (30-60 pages, 4-6hr production)")
        print("  tier3 = Ultimate Pack (60+ pages, 10-18hr production)")
        sys.exit(1)

    topic = sys.argv[1]
    target_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    tier = sys.argv[3] if len(sys.argv) > 3 else "tier1"

    print("="*80)
    print(">>> AI-POWERED CONTENT GENERATION")
    print("="*80)

    # Generate content with AI
    content = generate_full_content_with_ai(topic, target_pages, tier)

    # Save to file
    topic_slug = topic.lower().replace(' ', '-')
    output_file = f'.tmp/content_{topic_slug}.md'

    os.makedirs('.tmp', exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n[+] Content saved to: {output_file}")
    print(f"[+] Ready to convert to PDF with: python execution/generate_pdf_simple.py {output_file}")

    return output_file


if __name__ == "__main__":
    main()
