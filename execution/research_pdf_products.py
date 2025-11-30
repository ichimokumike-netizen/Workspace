"""
Script: research_pdf_products.py
Purpose: Automated research on high-volume PDF information products with Exploding Topics integration
Inputs: 
    - Niche/topic to research (CLI argument)
    - Exploding Topics data (CSV/JSON from assets/)
    - Search queries configuration
Outputs: 
    - Comprehensive research report in .tmp/
    - Structured data in JSON format
Author: AI Agent (Gemini)
Created: 2025-11-29
Updated: 2025-11-29 - Enhanced with full Exploding Topics data parsing
"""

import os
import sys
import json
import csv
import argparse
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class PDFProductResearcher:
    """Automated PDF product research engine with Exploding Topics integration."""
    
    def __init__(self, niche=None, output_dir=None):
        """
        Initialize the researcher.
        
        Args:
            niche (str): Specific niche/topic to research (optional, uses trending if not provided)
            output_dir (str): Output directory for reports (defaults to .tmp/)
        """
        self.niche = niche
        self.output_dir = output_dir or ".tmp"
        self.workspace_root = Path(__file__).parent.parent
        self.assets_dir = self.workspace_root / "assets"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Storage for research data
        self.exploding_topics_data = []
        self.web_research_data = {}
        self.product_examples = []
        self.pricing_data = []
        
    def validate_inputs(self):
        """
        Validate all required inputs and environment variables.
        Raise an exception if any critical requirement is missing.
        """
        print("✓ Validating inputs...")
        
        # Check if assets directory exists
        if not self.assets_dir.exists():
            print(f"⚠ Assets directory not found at {self.assets_dir}")
            print("  Creating assets directory for Exploding Topics data...")
            os.makedirs(self.assets_dir, exist_ok=True)
        
        # Note: Google Search API is optional - will provide instructions if missing
        google_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        if not google_api_key:
            print("⚠ GOOGLE_SEARCH_API_KEY not found in .env")
            print("  Script will use manual search queries instead of automated API calls")
            print("  To enable automated search: Add GOOGLE_SEARCH_API_KEY to .env")
        
        print("✓ Validation complete\n")
    
    def load_exploding_topics_data(self):
        """
        Load Exploding Topics data from assets folder.
        Supports CSV and JSON formats with full data parsing.
        """
        print("📊 Loading Exploding Topics data...")
        
        # Look for CSV or JSON files with "exploding", "trends", or "topics" in the name
        data_files = []
        for ext in ['*.csv', '*.json']:
            data_files.extend(self.assets_dir.glob(ext))
        
        # Filter for relevant files
        relevant_files = [
            f for f in data_files 
            if any(keyword in f.name.lower() for keyword in ['exploding', 'trend', 'topic'])
        ]
        
        if not relevant_files:
            print("⚠ No Exploding Topics data found in assets/")
            print("  Place CSV or JSON files with 'exploding', 'trends', or 'topics' in filename")
            print("  Example: assets/trends.csv")
            return []
        
        # Load the most recent file
        latest_file = max(relevant_files, key=lambda f: f.stat().st_mtime)
        print(f"  Loading: {latest_file.name}")
        
        if latest_file.suffix == '.csv':
            self.exploding_topics_data = self._load_csv_rich(latest_file)
        elif latest_file.suffix == '.json':
            self.exploding_topics_data = self._load_json(latest_file)
        
        print(f"✓ Loaded {len(self.exploding_topics_data)} trending topics\n")
        return self.exploding_topics_data
    
    def _parse_growth_percentage(self, growth_str):
        """Parse growth string like '+276%' to numeric value."""
        if not growth_str:
            return 0
        # Extract number from string like "+276%" or "-90%"
        match = re.search(r'([+-]?\d+)', str(growth_str))
        if match:
            return int(match.group(1))
        return 0
    
    def _parse_volume(self, volume_str):
        """Parse volume string like '246000' or '14.8K' to numeric."""
        if not volume_str:
            return 0
        volume_str = str(volume_str).strip()
        # Handle K suffix
        if 'K' in volume_str.upper():
            num = float(volume_str.upper().replace('K', ''))
            return int(num * 1000)
        # Handle M suffix
        if 'M' in volume_str.upper():
            num = float(volume_str.upper().replace('M', ''))
            return int(num * 1000000)
        # Try direct conversion
        try:
            return int(float(volume_str))
        except:
            return 0
    
    def _parse_channel_breakdown(self, channel_str):
        """Parse channel breakdown string to dictionary."""
        channels = {}
        if not channel_str:
            return channels
        
        # Format: "Facebook: 0.82, Instagram: 0.74, ..."
        parts = str(channel_str).split(',')
        for part in parts:
            if ':' in part:
                name, score = part.split(':', 1)
                try:
                    channels[name.strip()] = float(score.strip())
                except:
                    pass
        return channels
    
    def _load_csv_rich(self, filepath):
        """Load CSV data from Exploding Topics export with full data parsing."""
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse numeric fields
                growth_pct = self._parse_growth_percentage(row.get('Growth', '0'))
                volume = self._parse_volume(row.get('Volume', '0'))
                channels = self._parse_channel_breakdown(row.get('Channel Breakdown', ''))
                
                # Build enriched data structure
                topic_data = {
                    'keyword': row.get('Keyword', ''),
                    'description': row.get('Description', ''),
                    'categories': row.get('Categories', '').split(','),
                    'brand': row.get('Brand', 'No'),
                    'growth_pct': growth_pct,
                    'growth_raw': row.get('Growth', ''),
                    'volume': volume,
                    'growth_indicator': row.get('Growth Indicator', ''),
                    'speed_indicator': row.get('Speed Indicator', ''),
                    'seasonality': row.get('Seasonality Indicator', ''),
                    'volatility': row.get('Volatility Indicator', ''),
                    'sentiment': row.get('Sentiment Indicator', ''),
                    'forecast': row.get('Forecast Indicator', ''),
                    'timeframe': row.get('Timeframe', ''),
                    'url': row.get('URL', ''),
                    'channels': channels,
                    'search_history': row.get('Search History', '')
                }
                data.append(topic_data)
        return data
    
    def _load_json(self, filepath):
        """Load JSON data from Exploding Topics export."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_trending_topics(self):
        """
        Analyze Exploding Topics data to identify PDF product opportunities.
        Uses enhanced scoring with volume, growth, and forecast indicators.
        Returns prioritized list of topics suitable for PDF products.
        """
        print("🔍 Analyzing trending topics for PDF product opportunities...")
        
        if not self.exploding_topics_data:
            print("⚠ No trending data available for analysis")
            return []
        
        opportunities = []
        
        for topic in self.exploding_topics_data:
            # Calculate comprehensive PDF potential score
            score = self._calculate_pdf_potential_score_enhanced(topic)
            
            # Get top marketing channels
            top_channels = self._get_top_channels(topic.get('channels', {}))
            
            opportunities.append({
                'keyword': topic.get('keyword', ''),
                'description': topic.get('description', ''),
                'categories': topic.get('categories', []),
                'growth_pct': topic.get('growth_pct', 0),
                'volume': topic.get('volume', 0),
                'growth_indicator': topic.get('growth_indicator', ''),
                'forecast': topic.get('forecast', ''),
                'seasonality': topic.get('seasonality', ''),
                'pdf_potential_score': score,
                'top_channels': top_channels,
                'raw_data': topic
            })
        
        # Sort by PDF potential score
        opportunities.sort(key=lambda x: x['pdf_potential_score'], reverse=True)
        
        print(f"✓ Identified {len(opportunities)} potential PDF topics")
        print(f"  Top 5 opportunities:")
        for i, opp in enumerate(opportunities[:5], 1):
            print(f"    {i}. {opp['keyword']} (Score: {opp['pdf_potential_score']:.1f}, "
                  f"Growth: {opp['growth_pct']:+d}%, Vol: {opp['volume']:,})")
        print()
        
        return opportunities
    
    def _calculate_pdf_potential_score_enhanced(self, topic):
        """
        Enhanced PDF potential scoring using all available data.
        Factors: keywords, growth %, volume, forecast, seasonality, categories.
        Score range: 0-100
        """
        score = 40  # Base score
        
        keyword = str(topic.get('keyword', '')).lower()
        description = str(topic.get('description', '')).lower()
        combined_text = keyword + ' ' + description
        
        # 1. KEYWORD ANALYSIS (+30 max)
        pdf_positive_keywords = [
            'guide', 'tutorial', 'template', 'planner', 'how to',
            'course', 'learning', 'training', 'tips', 'strategies',
            'workflow', 'system', 'framework', 'method', 'checklist',
            'tracker', 'workbook', 'blueprint', 'manual', 'handbook'
        ]
        
        keyword_score = 0
        for kw in pdf_positive_keywords:
            if kw in combined_text:
                keyword_score += 3
        score += min(keyword_score, 30)  # Cap at +30
        
        # 2. GROWTH ANALYSIS (+20 max)
        growth_pct = topic.get('growth_pct', 0)
        if growth_pct >= 200:
            score += 20
        elif growth_pct >= 100:
            score += 15
        elif growth_pct >= 50:
            score += 10
        elif growth_pct >= 0:
            score += 5
        else:  # Negative growth
            score -= 10
        
        # 3. VOLUME ANALYSIS (+15 max)
        volume = topic.get('volume', 0)
        if volume >= 100000:
            score += 15
        elif volume >= 50000:
            score += 12
        elif volume >= 10000:
            score += 10
        elif volume >= 5000:
            score += 7
        elif volume >= 1000:
            score += 5
        elif volume >= 100:
            score += 3
        
        # 4. FORECAST INDICATOR (+10 max)
        forecast = str(topic.get('forecast', '')).lower()
        if 'growing' in forecast:
            score += 10
        elif 'stationary' in forecast:
            score += 5
        elif 'declining' in forecast:
            score -= 5
        
        # 5. GROWTH INDICATOR (+10 max)
        growth_ind = str(topic.get('growth_indicator', '')).lower()
        if 'exploding' in growth_ind:
            score += 10
        elif 'regular' in growth_ind:
            score += 5
        elif 'peaked' in growth_ind:
            score -= 5
        
        # 6. CATEGORY ANALYSIS (+10 max)
        categories = [str(c).lower().strip() for c in topic.get('categories', [])]
        pdf_friendly_categories = [
            'education', 'business', 'productivity', 'health', 'finance',
            'marketing', 'lifestyle', 'self-improvement', 'career', 'training'
        ]
        
        category_score = 0
        for cat in pdf_friendly_categories:
            if any(cat in c for c in categories):
                category_score += 5
        score += min(category_score, 10)
        
        # 7. SEASONALITY PENALTY (if highly seasonal, harder to sell year-round)
        seasonality = str(topic.get('seasonality', '')).lower()
        if 'high' in seasonality:
            score -= 5  # Seasonal products harder for evergreen PDFs
        
        # 8. NEGATIVE INDICATORS
        negative_keywords = [
            'physical', 'hardware', 'device', 'game', 'video game',
            'toy', 'clothing', 'food', 'restaurant', 'app store'
        ]
        
        for neg_kw in negative_keywords:
            if neg_kw in combined_text:
                score -= 15
                break  # Only penalize once
        
        # Clamp score between 0-100
        return max(0, min(100, score))
    
    def _get_top_channels(self, channels_dict, top_n=3):
        """Get top N marketing channels by score."""
        if not channels_dict:
            return []
        
        # Sort channels by score
        sorted_channels = sorted(channels_dict.items(), key=lambda x: x[1], reverse=True)
        return [{'name': name, 'score': score} for name, score in sorted_channels[:top_n]]
    
    def generate_search_queries(self, topic):
        """
        Generate strategic search queries for researching PDF products in the given topic.
        
        Args:
            topic (str): The topic/niche to research
            
        Returns:
            list: List of search query dictionaries
        """
        queries = [
            {
                'query': f'{topic} PDF guide bestselling Gumroad',
                'purpose': 'Find successful Gumroad products',
                'priority': 'high'
            },
            {
                'query': f'{topic} digital download template Etsy bestseller',
                'purpose': 'Identify Etsy bestsellers',
                'priority': 'high'
            },
            {
                'query': f'{topic} information product revenue case study',
                'purpose': 'Find revenue examples',
                'priority': 'high'
            },
            {
                'query': f'{topic} Notion template selling',
                'purpose': 'Research Notion templates',
                'priority': 'medium'
            },
            {
                'query': f'{topic} ChatGPT prompts guide',
                'purpose': 'AI prompt products',
                'priority': 'medium'
            },
            {
                'query': f'how to create {topic} digital product',
                'purpose': 'Understand product creation',
                'priority': 'low'
            }
        ]
        
        return queries
    
    def execute_research(self, topic=None):
        """
        Execute the full research workflow.
        
        Args:
            topic (str): Specific topic to research (uses self.niche if not provided)
        """
        research_topic = topic or self.niche
        
        # Analyze all topics first
        opportunities = self.analyze_trending_topics()
        
        if not research_topic:
            # Use top trending topic from Exploding Topics
            if opportunities:
                research_topic = opportunities[0]['keyword']
                print(f"🎯 Auto-selected trending topic: {research_topic}\n")
            else:
                research_topic = "digital products"  # Fallback
                print(f"⚠ Using fallback topic: {research_topic}\n")
        
        print(f"🚀 Starting research for: {research_topic}")
        print("=" * 60 + "\n")
        
        # Find matching opportunity or create basic one
        matching_opp = next(
            (o for o in opportunities if research_topic.lower() in o['keyword'].lower()),
            None
        )
        
        # Generate search queries
        queries = self.generate_search_queries(research_topic)
        
        # Display queries for manual or AI-assisted research
        print("📋 Recommended search queries (execute with AI agent or manually):\n")
        for i, q in enumerate(queries, 1):
            print(f"{i}. [{q['priority'].upper()}] {q['query']}")
            print(f"   Purpose: {q['purpose']}\n")
        
        # Prepare research structure
        research_data = {
            'topic': research_topic,
            'timestamp': self.timestamp,
            'topic_details': matching_opp if matching_opp else {},
            'all_opportunities': opportunities[:20],  # Top 20
            'search_queries': queries,
            'product_categories': self._get_product_categories(),
            'pricing_guidelines': self._get_pricing_guidelines(),
            'template_recommendations': self._get_template_recommendations(research_topic, matching_opp)
        }
        
        return research_data
    
    def _get_product_categories(self):
        """Return standard PDF product categories for analysis."""
        return [
            {
                'name': 'Notion Templates',
                'revenue_potential': 'Highest ($500K+ proven)',
                'price_range': '$2-$199',
                'characteristics': 'All-in-one systems, niche-specific, visual dashboards'
            },
            {
                'name': 'ChatGPT Prompt Guides',
                'revenue_potential': 'High ($10K/month possible)',
                'price_range': '$7-$147',
                'characteristics': 'Niche-focused, problem-solving, bundled with resources'
            },
            {
                'name': 'Digital Planners',
                'revenue_potential': 'Evergreen (steady volume)',
                'price_range': '$2-$75',
                'characteristics': 'Hyperlinked, app-compatible, aesthetic design'
            },
            {
                'name': 'Social Media Templates',
                'revenue_potential': 'High volume',
                'price_range': '$7-$97',
                'characteristics': 'Canva-based, creator economy, reusable'
            },
            {
                'name': 'Educational Guides',
                'revenue_potential': 'Moderate-High',
                'price_range': '$7-$97',
                'characteristics': 'Actionable, niche-specific, includes templates'
            },
            {
                'name': 'Business Templates',
                'revenue_potential': 'B2B pricing premium',
                'price_range': '$5-$297',
                'characteristics': 'Professional, legal/compliance, time-saving'
            }
        ]
    
    def _get_pricing_guidelines(self):
        """Return pricing strategy guidelines."""
        return {
            'tier_1_quick_guides': {'price': '$7-$17', 'pages': '20-30', 'time': '2-4 hours'},
            'tier_2_comprehensive': {'price': '$27-$47', 'pages': '30-60', 'time': '6-10 hours'},
            'tier_3_ultimate_packs': {'price': '$67-$197', 'pages': '60-100+', 'time': '15-30 hours'},
            'launch_strategy': '30% discount for first 48 hours',
            'sweet_spot': '$7-$47 for most categories'
        }
    
    def _get_template_recommendations(self, topic, opportunity_data=None):
        """Generate specific template recommendations for the topic."""
        recommendations = []
        
        if opportunity_data:
            volume = opportunity_data.get('volume', 0)
            growth_pct = opportunity_data.get('growth_pct', 0)
            categories = opportunity_data.get('categories', [])
            
            # Tailor recommendations based on data
            if volume > 50000:
                recommendations.append(f'{topic} - Comprehensive Guide (Tier 2, $37, 8-12 hours) - HIGH VOLUME market')
            if growth_pct > 100:
                recommendations.append(f'{topic} - Quick Start Guide (Tier 1, $17, 2-4 hours) - EXPLOSIVE GROWTH (move fast!)')
            if 'business' in ', '.join(categories).lower():
                recommendations.append(f'{topic} - Business Templates Pack (Tier 2, $47, 6-10 hours)')
            if 'lifestyle' in ', '.join(categories).lower() or 'health' in ', '.join(categories).lower():
                recommendations.append(f'{topic} - Digital Planner & Tracker (Tier 1, $15, 3-5 hours)')
        
        # Add generic recommendations
        recommendations.extend([
            f'{topic} - ChatGPT Prompt Guide (Tier 1, $17, 2-4 hours)',
            f'{topic} - Notion Template System (Tier 2, $37, 8-12 hours)',
            f'{topic} - Social Media Content Bundle (Tier 1, $15, 3-5 hours)',
            f'{topic} - Ultimate Resource Pack (Tier 3, $97, 20-30 hours)'
        ])
        
        return recommendations[:5]  # Top 5
    
    def generate_report(self, research_data):
        """
        Generate comprehensive markdown report from research data.
        
        Args:
            research_data (dict): Compiled research findings
        """
        print("\n📝 Generating comprehensive research report...")
        
        topic = research_data['topic']
        filename = f"pdf_research_{topic.replace(' ', '_')}_{self.timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        # Build markdown report
        report = f"""# PDF Product Research Report: {topic}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Research Focus:** {topic}  
**Data Sources:** Exploding Topics (Enhanced), Web Research, Market Analysis

---

## 🎯 Executive Summary

This automated research report analyzes opportunities for creating high-volume PDF information products focused on **{topic}**.

"""
        
        # Add topic-specific insights if available
        topic_details = research_data.get('topic_details', {})
        if topic_details:
            report += f"""### 📊 Selected Topic Insights:

- **Keyword:** {topic_details.get('keyword', 'N/A')}
- **PDF Potential Score:** {topic_details.get('pdf_potential_score', 0):.1f}/100
- **Growth:** {topic_details.get('growth_pct', 0):+d}%
- **Monthly Volume:** {topic_details.get('volume', 0):,} searches
- **Growth Indicator:** {topic_details.get('growth_indicator', 'N/A')}
- **Forecast:** {topic_details.get('forecast', 'N/A')}
- **Seasonality:** {topic_details.get('seasonality', 'N/A')}

**Description:**  
{topic_details.get('description', 'No description available')}

"""
            
            # Add channel marketing recommendations
            top_channels = topic_details.get('top_channels', [])
            if top_channels:
                report += f"""### 📱 Top Marketing Channels for "{topic}":

"""
                for i, channel in enumerate(top_channels, 1):
                    score_pct = int(channel['score'] * 100)
                    bars = '█' * int(channel['score'] * 10)
                    report += f"{i}. **{channel['name']}** {bars} {score_pct}%\n"
                
                report += f"""
**Marketing Strategy:**
- Focus on {top_channels[0]['name']} for primary promotion (highest engagement: {int(top_channels[0]['score']*100)}%)
- Use {top_channels[1]['name']} for secondary outreach
- Consider paid ads on {top_channels[0]['name']} during launch

"""
        
        report += """---

## 🔥 Top 20 PDF Product Opportunities

Based on comprehensive analysis of growth, volume, and PDF suitability:

"""
        
        # Add top opportunities table
        opportunities = research_data.get('all_opportunities', [])
        for i, opp in enumerate(opportunities[:20], 1):
            report += f"""### {i}. {opp['keyword']} (Score: {opp['pdf_potential_score']:.1f}/100)

- **Growth:** {opp['growth_pct']:+d}% ({opp['growth_indicator']})
- **Volume:** {opp['volume']:,} monthly searches
- **Forecast:** {opp['forecast']}
- **Categories:** {', '.join(opp['categories'][:5])}
- **Top Channels:** {', '.join([c['name'] for c in opp['top_channels']])}

"""
        
        # Add search queries section
        report += """---

## 🔍 Recommended Research Queries

Execute these searches (manually or via AI agent) to gather specific product examples:

"""
        for i, query in enumerate(research_data.get('search_queries', []), 1):
            report += f"{i}. **[{query['priority'].upper()}]** `{query['query']}`\n"
            report += f"   - Purpose: {query['purpose']}\n\n"
        
        # Add product categories
        report += """---

## 📦 Product Category Analysis

"""
        for cat in research_data.get('product_categories', []):
            report += f"### {cat['name']}\n\n"
            report += f"- **Revenue Potential:** {cat['revenue_potential']}\n"
            report += f"- **Price Range:** {cat['price_range']}\n"
            report += f"- **Key Characteristics:** {cat['characteristics']}\n\n"
        
        # Add pricing guidelines
        report += """---

## 💰 Pricing Strategy Guidelines

"""
        pricing = research_data.get('pricing_guidelines', {})
        for tier, details in pricing.items():
            if isinstance(details, dict):
                report += f"### {tier.replace('_', ' ').title()}\n"
                for key, value in details.items():
                    report += f"- **{key.title()}:** {value}\n"
                report += "\n"
            else:
                report += f"- **{tier.replace('_', ' ').title()}:** {details}\n"
        
        # Add template recommendations
        report += f"""---

## 🎨 Recommended Templates for "{topic}"

"""
        for i, template in enumerate(research_data.get('template_recommendations', []), 1):
            report += f"{i}. {template}\n"
        
        # Add action items
        report += """

---

## ✅ Next Steps

1. **Execute Research Queries** - Run the recommended searches above
2. **Analyze Competitors** - Identify 3-5 successful products in each category
3. **Select Template** - Choose highest-ROI template from recommendations
4. **Create Outline** - Structure your PDF based on competitive analysis
5. **Set Pricing** - Use guidelines above for your tier level
6. **Build MVP** - Create Tier 1 Quick Guide first (2-4 hours)
7. **Launch & Iterate** - 30% discount for 48 hours, gather feedback
8. **Market on Top Channels** - Focus on highest-scoring channels from analysis

---

*Generated by: research_pdf_products.py (Enhanced)*  
*Workspace: {self.workspace_root}*  
*Output: {filepath}*
"""
        
        # Write report to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✓ Report generated: {filepath}")
        
        # Also save JSON data
        json_filename = f"pdf_research_{topic.replace(' ', '_')}_{self.timestamp}.json"
        json_filepath = os.path.join(self.output_dir, json_filename)
        
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, indent=2)
        
        print(f"✓ Data saved: {json_filepath}\n")
        
        return filepath, json_filepath


def main():
    """
    Main function - execute PDF product research workflow.
    """
    parser = argparse.ArgumentParser(
        description='Automated PDF product research with Exploding Topics integration (Enhanced)'
    )
    parser.add_argument(
        '--niche',
        type=str,
        help='Specific niche/topic to research (e.g., "AI productivity tools")',
        default=None
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output directory for reports (default: .tmp/)',
        default='.tmp'
    )
    
    args = parser.parse_args()
    
    try:
        print("\n" + "="*60)
        print("  PDF PRODUCT RESEARCH AUTOMATION (ENHANCED)")
        print("="*60 + "\n")
        
        # Initialize researcher
        researcher = PDFProductResearcher(niche=args.niche, output_dir=args.output)
        
        # Step 1: Validate inputs
        researcher.validate_inputs()
        
        # Step 2: Load Exploding Topics data
        researcher.load_exploding_topics_data()
        
        # Step 3: Execute research (includes analysis)
        research_data = researcher.execute_research()
        
        # Step 4: Generate report
        report_path, data_path = researcher.generate_report(research_data)
        
        print("="*60)
        print("✅ RESEARCH COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"\n📄 Report: {report_path}")
        print(f"📊 Data: {data_path}")
        print(f"\n💡 Next: Review the report for:")
        print("     - PDF potential scores (higher = better opportunity)")
        print("     - Top marketing channels for your niche")
        print("     - Tailored template recommendations")
        print("     - Comprehensive trend analysis\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
