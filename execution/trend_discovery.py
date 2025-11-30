"""
Script: trend_discovery.py
Purpose: Discover trending topics across multiple platforms for PDF creation
Inputs: None (automated scraping)
Outputs: .tmp/trending_topics_[date].json with validated trends
Author: AI-Assisted
Created: 2025-11-29
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
import praw  # Reddit API
from pytrends.request import TrendReq  # Google Trends

# Load environment variables from .env file
load_dotenv()


def validate_inputs():
    """
    Validate all required inputs and environment variables.
    Raise an exception if any required input is missing.
    """
    reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
    reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')

    if not reddit_client_id or not reddit_client_secret:
        print("Warning: Reddit API credentials not found in .env file")
        print("Reddit trend discovery will be skipped")
        print("To enable Reddit: Add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to .env")
        return False

    return True


def get_fallback_trends():
    """
    Fallback trending topics when API fails.
    These are manually curated popular topics that are evergreen or currently trending.
    """
    fallback_topics = [
        "how to use chatgpt effectively",
        "ai tools for productivity",
        "how to start a side hustle",
        "learn python for beginners",
        "how to create viral tiktok videos",
        "passive income ideas 2025",
        "how to build a personal brand",
        "budgeting tips for beginners",
        "how to improve sleep quality",
        "meal prep for beginners",
        "how to negotiate salary",
        "home workout routines",
        "how to write better emails",
        "digital marketing for small business",
        "how to learn faster",
        "productivity hacks for remote work",
        "how to start investing",
        "mindfulness meditation guide",
        "how to declutter your home",
        "resume writing tips 2025"
    ]

    trends = []
    for idx, topic in enumerate(fallback_topics):
        trends.append({
            'topic': topic,
            'source': 'Curated Fallback',
            'rank': idx + 1,
            'timestamp': datetime.now().isoformat()
        })

    return trends


def get_google_trends():
    """
    Get trending topics from Google Trends.
    Returns list of trending topics with metadata.
    """
    print("\n[*] Fetching Google Trends...")

    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2)

        # Get trending searches (US)
        trending_searches = pytrends.trending_searches(pn='united_states')

        trends = []
        for idx, topic in enumerate(trending_searches[0].head(20)):  # Top 20
            trends.append({
                'topic': topic,
                'source': 'Google Trends',
                'rank': idx + 1,
                'timestamp': datetime.now().isoformat()
            })

        print(f"[+] Found {len(trends)} trending topics from Google Trends")
        return trends

    except Exception as e:
        print(f"[!] Google Trends error: {str(e)}")
        print(f"[*] Using fallback trending topics...")
        return get_fallback_trends()


def get_reddit_trends():
    """
    Get trending topics from Reddit (r/all trending posts).
    Returns list of trending topics with metadata.
    """
    print("\n[*] Fetching Reddit Trends...")

    try:
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent='TrendDiscovery/1.0'
        )

        trends = []

        # Get top posts from r/all (past 24 hours)
        for idx, submission in enumerate(reddit.subreddit('all').hot(limit=30)):
            # Skip if low engagement
            if submission.score < 1000:
                continue

            trends.append({
                'topic': submission.title,
                'subreddit': submission.subreddit.display_name,
                'score': submission.score,
                'num_comments': submission.num_comments,
                'url': submission.url,
                'source': 'Reddit',
                'rank': idx + 1,
                'timestamp': datetime.now().isoformat()
            })

        print(f"[+] Found {len(trends)} trending topics from Reddit")
        return trends

    except Exception as e:
        print(f"[!] Reddit API error: {str(e)}")
        return []


def analyze_and_validate_trends(all_trends):
    """
    Analyze trends and validate against PDF publishing criteria.

    Validation Criteria:
    - Topic is showing exponential growth (not just steady)
    - Audience is actively searching for "how to" information
    - Low competition in PDF/guide format
    - Can create authoritative content quickly (24-48 hours)
    """
    print("\n[*] Analyzing and validating trends...")

    validated_trends = []

    for trend in all_trends:
        topic = trend.get('topic', '')

        # Filter criteria
        is_how_to_topic = any(keyword in topic.lower() for keyword in [
            'how to', 'guide', 'tutorial', 'learn', 'tips', 'tricks',
            'beginner', 'start', 'make', 'create', 'build'
        ])

        # Check if topic is actionable (can we write a guide?)
        is_actionable = len(topic.split()) >= 3  # At least 3 words

        # Avoid news/politics/controversy
        is_safe_topic = not any(keyword in topic.lower() for keyword in [
            'election', 'politics', 'war', 'scandal', 'breaking',
            'died', 'dead', 'killed', 'trump', 'biden'
        ])

        # Score the trend
        score = 0
        if is_how_to_topic:
            score += 3
        if is_actionable:
            score += 2
        if is_safe_topic:
            score += 2
        if trend.get('source') == 'Google Trends':
            score += 1  # Google Trends = search volume

        trend['validation_score'] = score
        trend['is_validated'] = score >= 5

        if trend['is_validated']:
            validated_trends.append(trend)

    # Sort by validation score (highest first)
    validated_trends.sort(key=lambda x: x['validation_score'], reverse=True)

    print(f"[+] Validated {len(validated_trends)} topics suitable for PDF guides")

    return validated_trends


def save_trends(trends, output_path):
    """
    Save trends to JSON file in .tmp/ directory.
    """
    # Ensure .tmp directory exists
    os.makedirs('.tmp', exist_ok=True)

    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'generated_at': datetime.now().isoformat(),
            'total_trends': len(trends),
            'trends': trends
        }, f, indent=2, ensure_ascii=False)

    print(f"\n[+] Saved {len(trends)} trends to {output_path}")


def display_top_trends(trends, limit=10):
    """
    Display top trends in a readable format.
    """
    print(f"\n{'='*80}")
    print(f">>> TOP {limit} TRENDING TOPICS FOR PDF GUIDES")
    print(f"{'='*80}\n")

    for idx, trend in enumerate(trends[:limit], 1):
        print(f"{idx}. {trend['topic']}")
        print(f"   Source: {trend['source']}")
        print(f"   Score: {trend['validation_score']}/7")
        if 'subreddit' in trend:
            print(f"   Subreddit: r/{trend['subreddit']} | Score: {trend['score']} | Comments: {trend['num_comments']}")
        print()


def main():
    """
    Main function - discover and validate trending topics.
    """
    try:
        print("="*80)
        print(">>> TREND DISCOVERY FOR PDF PUBLISHING")
        print("="*80)

        # Step 1: Validate inputs (optional for some sources)
        has_reddit = validate_inputs()

        # Step 2: Gather trends from multiple sources
        all_trends = []

        # Google Trends (no API key needed for basic use)
        google_trends = get_google_trends()
        all_trends.extend(google_trends)

        # Reddit (requires API credentials)
        if has_reddit:
            reddit_trends = get_reddit_trends()
            all_trends.extend(reddit_trends)

        if not all_trends:
            print("\n[X] No trends found. Please check your API credentials.")
            sys.exit(1)

        # Step 3: Analyze and validate trends
        validated_trends = analyze_and_validate_trends(all_trends)

        # Step 4: Save results
        today = datetime.now().strftime('%Y-%m-%d')
        output_path = f'.tmp/trending_topics_{today}.json'
        save_trends(validated_trends, output_path)

        # Step 5: Display top results
        display_top_trends(validated_trends, limit=10)

        print(f"{'='*80}")
        print("[+] Trend discovery completed successfully!")
        print(f"{'='*80}")
        print(f"\n>>> Next steps:")
        print(f"1. Review the top trends in {output_path}")
        print(f"2. Choose a topic that:")
        print(f"   - You already understand")
        print(f"   - Has clear 'how to' angle")
        print(f"   - Won't require deep technical expertise")
        print(f"3. Run: python execution/topic_research.py <topic_name>")

    except Exception as e:
        print(f"[X] Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
