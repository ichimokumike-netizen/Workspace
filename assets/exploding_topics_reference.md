# Exploding Topics - Reference Guide for AI Agents

**Purpose:** This guide explains how to interpret Exploding Topics data for PDF product research  
**Last Updated:** 2025-11-29

---

## Overview

Exploding Topics is a trend tracking platform with a database of **1.1M+ trends** updated daily. It uses machine learning and data analytics to spot emerging trends before they go mainstream.

### What Makes It Valuable for PDF Research

- **Early Detection:** Spot trends before competitors
- **Growth Signals:** Identify explosive growth opportunities
- **Market Validation:** Search volume confirms demand
- **Channel Insights:** Know where your audience is
- **Forecast Data:** Predict trend longevity

---

## Data Structure & Key Columns

When you export Exploding Topics data, you'll receive these columns:

| Column | Description | How to Use for PDF Research |
|--------|-------------|----------------------------|
| **Keyword** | The trend/topic name | Topic for your PDF guide |
| **Description** | AI-generated summary | Understand target audience & use case |
| **Categories** | Industry tags | Identify PDF-friendly niches |
| **Growth** | % increase over timeframe | Higher = more opportunity |
| **Volume** | Monthly search volume | Market size validation |
| **Growth Indicator** | Exploding/Regular/Peaked | Timing urgency |
| **Speed Indicator** | Exponential/Constant/Stationary | Growth velocity |
| **Seasonality** | High/Medium/Low | Evergreen vs seasonal |
| **Volatility** | High/Average/Low | Trend stability |
| **Sentiment** | Positive/Neutral/Negative | Market reception |
| **Forecast** | Growing/Stationary/Declining | Future direction |
| **Channel Breakdown** | Social media scores | Marketing strategy |

---

## Key Indicators Explained

### 1. Growth Indicator
Measures the trend's growth over time based on rate and trend line.

- **Exploding** ⚡ - Rapid upward trend, sharp increase
  - *PDF Opportunity:* HIGH - Move fast, first-mover advantage
  - *Example:* ChatGPT prompts (+500% in 3 months)
  
- **Regular** 📈 - Consistent growth over measured period
  - *PDF Opportunity:* MEDIUM-HIGH - Stable market, evergreen potential
  - *Example:* Notion templates (steady growth)
  
- **Peaked** 📉 - Downward trend or already peaked
  - *PDF Opportunity:* LOW - Avoid unless you have unique angle
  - *Example:* NFTs (post-hype decline)

### 2. Speed Indicator
Evaluates the speed of growth focusing on exponential behavior.

- **Exponential** 🚀 - Growing at exponential rate
  - *Action:* Create quick guide immediately (Tier 1, 2-4 hours)
  
- **Constant** ➡️ - Upward trajectory, constant rate
  - *Action:* More time for comprehensive guide (Tier 2, 6-10 hours)
  
- **Stationary** ⏸️ - No growth or decline, flat
  - *Action:* Avoid for trending content, consider evergreen angle

### 3. Seasonality Indicator
Measures recurring patterns that occur periodically.

- **High** 🎄 - Significant seasonal variation
  - *PDF Strategy:* Time launch for peak season OR create "year-round" guide
  - *Example:* "Tax preparation" peaks Jan-Apr
  
- **Medium** 🌤️ - Some seasonal patterns
  - *PDF Strategy:* General guide with seasonal sections
  
- **Low** ☀️ - No seasonal variation, evergreen
  - *PDF Strategy:* BEST for long-term sales, create comprehensive guide

### 4. Volatility Indicator
Measures degree of variation or unpredictability.

- **High** 📊 - Large fluctuations, unstable
  - *Risk:* Topic could crash quickly
  - *Strategy:* Quick guide only, don't invest 20+ hours
  
- **Average** 📉 - Moderate fluctuations
  - *Risk:* Medium
  - *Strategy:* Standard guides (Tier 1-2)
  
- **Low** 📏 - Stable, gradual change
  - *Risk:* Low
  - *Strategy:* Safe for premium guides (Tier 3)

### 5. Sentiment Indicator
Overall feeling/attitude towards a trend.

- **Positive** 😊 - Favorable consumer view
  - *PDF Opportunity:* HIGH - People want to learn more
  - *Pricing:* Can charge premium
  
- **Neutral** 😐 - Balanced feelings
  - *PDF Opportunity:* MEDIUM - Educational angle needed
  
- **Negative** 😟 - Negative consumer feelings
  - *PDF Opportunity:* LOW - Avoid unless solving a pain point
  - *Exception:* "How to avoid X" or "Alternatives to X"

### 6. Forecast Indicator
Predicts trend direction over next 12 months (ML-based).

- **Growing** 📈 - Expected to increase
  - *Action:* INVEST - Create comprehensive guide, build authority
  - *Timeline:* You have time to do it right
  
- **Stationary** ➖ - Expected to remain flat
  - *Action:* Quick guide only, don't overinvest
  
- **Declining** 📉 - Expected to decrease
  - *Action:* AVOID - Don't create new content
  - *Exception:* "What went wrong with X" retrospective

---

## Channel Breakdown Interpretation

Channel scores range from 0.00 to 1.00 (0-100%). Use these to determine where to market your PDF.

### High-Performing Channels (0.70-1.00)

- **Pinterest (0.95):** Visual products, DIY guides, templates, planners
  - *Strategy:* Create pin-worthy graphics, infographics
  
- **TikTok (0.91):** Trending topics, how-to content, younger demographics
  - *Strategy:* Short video teasers, behind-the-scenes of PDF creation
  
- **YouTube (0.81):** Educational content, tutorials, in-depth topics
  - *Strategy:* Video walkthrough of PDF, link in description
  
- **Instagram (0.74):** Lifestyle, wellness, aesthetic products
  - *Strategy:* Carousel posts, story highlights, link in bio

### Medium-Performing Channels (0.40-0.69)

- **Facebook (0.57):** Broad demographics, groups, communities
  - *Strategy:* Join relevant groups, provide value before promoting
  
- **Reddit (0.46):** Niche communities, authentic discussion
  - *Strategy:* Answer questions, build reputation, subtle promotion

### Lower-Performing Channels (0.00-0.39)

- **LinkedIn (0.32):** Professional/B2B topics only
  - *Strategy:* If B2B product, focus here; otherwise skip
  
- **Twitter (0.28):** Breaking news, real-time trends
  - *Strategy:* Tweet threads with value, link to PDF

---

## How to Use This Data for PDF Research

### Step 1: Score Topics for PDF Potential

Use this formula (automated in `research_pdf_products.py`):

```
PDF Potential Score = 
  + Keyword Match (30 max) - "guide", "template", "tutorial", etc.
  + Growth % (20 max) - Higher = better
  + Volume (15 max) - Market validation
  + Forecast (10 max) - Growing > Stationary > Declining
  + Growth Indicator (10 max) - Exploding > Regular > Peaked
  + Categories (10 max) - Education, business, productivity, etc.
  - Seasonality penalty (5) - If highly seasonal
  - Physical product penalty (15) - If hardware, toys, food, etc.
```

**Ideal Score:** 70-100  
**Good Score:** 50-69  
**Avoid:** Below 50

### Step 2: Determine Product Tier

Based on indicators:

| Indicators | Recommended Tier | Time Investment | Price |
|-----------|------------------|-----------------|-------|
| Exploding + Growing + Low Seasonality | Tier 2-3 (authority play) | 10-30 hrs | $37-$97 |
| Exploding + Stationary + High Volume | Tier 1 (quick win) | 2-4 hrs | $17 |
| Regular + Growing + Low Volatility | Tier 2 (comprehensive) | 6-10 hrs | $27-$47 |
| Peaked + Declining | Skip or retrospective only | N/A | N/A |

### Step 3: Marketing Strategy from Channels

**Example: Candle Warmer Lamp**
- Pinterest: 0.95
- TikTok: 0.91
- Instagram: 0.67

**Strategy:**
1. Create Pinterest board with candle safety tips
2. Post TikTok videos showing ambient lighting setups
3. Instagram carousel: "5 Ways to Use Candle Warmers"
4. PDF: "Ultimate Home Ambiance Guide" ($27)

---

## Related Trends Feature

Exploding Topics shows "Related Trends" - micro trends within your main topic.

**How to Use:**
1. Main Topic: "AI productivity"
2. Related Trends: "ChatGPT prompts", "AI writing tools", "automation workflows"
3. **PDF Bundle Opportunity:** Create 3 guides, sell as bundle

**Example Structure:**
- Individual guides: $17 each
- Bundle: $39 (33% discount)
- Upsell path: Buy one → email bundle offer

---

## Meta Trends Concept

Meta Trends are macro trends that contain multiple micro trends.

**Example:**
- **Meta Trend:** Sleep Tech
- **Micro Trends:** weighted eye mask, sleep tracking apps, white noise machines, lofi music

**PDF Opportunity:**
Create comprehensive "Ultimate Sleep Optimization Guide" covering all micro trends as chapters.

**Pricing:** $47-$97 (premium positioning)

---

## Best Practices for AI Agents

### When Analyzing Exploding Topics Data:

1. **Prioritize by Score:** Focus on 70+ PDF potential scores
2. **Check Forecast:** Only invest in "Growing" or "Stationary" forecasts
3. **Validate Volume:** Minimum 500 monthly searches for viability
4. **Match Channels:** Recommend marketing based on top 3 channels
5. **Consider Volatility:** Low volatility = safe for bigger investment
6. **Seasonal Timing:** If high seasonality, create guide 2-3 months before peak
7. **Bundle Related Trends:** Look for 3-5 related micro trends for bundles

### Red Flags (Avoid These):

- ❌ Peaked + Declining + Negative sentiment
- ❌ High volatility + Low volume
- ❌ Exploding + High seasonality (unless timed perfectly)
- ❌ Physical products without educational angle
- ❌ Negative sentiment + Declining forecast

### Green Lights (Pursue These):

- ✅ Exploding + Growing + Positive sentiment
- ✅ Regular + Low volatility + Low seasonality
- ✅ High volume + Growing forecast
- ✅ Educational categories + Multiple related trends
- ✅ High Pinterest/YouTube scores (visual learners)

---

## Subscription Levels & Limits

| Plan | Price | Tracked Trends | Analyses/Month | CSV Export | Forecast |
|------|-------|----------------|----------------|------------|----------|
| Entrepreneur | $39/mo | 100 | 10 | ❌ | ❌ |
| Investor | $99/mo | 500 | 100 | ✅ | ✅ |
| Business | $249/mo | 2,000 | 500 | ✅ | ✅ |

**Recommendation for PDF Business:** 
- Start: Entrepreneur plan ($39/mo) - 10 analyses = 10 PDF opportunities/month
- Scale: Investor plan ($99/mo) - CSV export enables automation
- Enterprise: Business plan ($249/mo) - For high-volume PDF production

---

## Automation Tips

### Efficient Use of Analysis Limits:

1. **Batch Research:** Analyze 10-20 topics at once, compare scores
2. **Export CSV:** Download all data for offline analysis
3. **Track High Performers:** Only track topics scoring 70+
4. **Monthly Refresh:** Limits reset on 1st of month - plan accordingly
5. **Related Trends:** One analysis gives you 10+ related micro trends (multiplier!)

### Integration with PDF Pipeline:

```
Exploding Topics Export (CSV)
    ↓
research_pdf_products.py (analyze & score)
    ↓
Select top 3 topics (70+ score)
    ↓
generate_content.py (create PDFs)
    ↓
Market on top 3 channels per topic
```

---

## Frequently Asked Questions

**Q: How often should I check for new trends?**  
A: Weekly. Database updates daily, but significant trends emerge weekly.

**Q: What's the minimum viable data for a PDF?**  
A: 500+ monthly volume, Growing/Stationary forecast, 60+ PDF score.

**Q: Should I create PDFs for multiple related trends?**  
A: Yes! Bundle them. Related trends = cross-sell opportunity.

**Q: What if a trend has high volume but declining forecast?**  
A: Create quick guide only (Tier 1, 2-4 hours). Don't overinvest.

**Q: How do I use Meta Trends?**  
A: Create comprehensive bundles covering all micro trends within the meta trend.

---

## Quick Reference: PDF Decision Matrix

| Growth | Forecast | Volume | Seasonality | **Decision** |
|--------|----------|--------|-------------|--------------|
| Exploding | Growing | High | Low | ✅ INVEST (Tier 2-3) |
| Exploding | Stationary | High | Any | ✅ Quick Win (Tier 1) |
| Regular | Growing | Medium | Low | ✅ Standard (Tier 2) |
| Regular | Stationary | Low | High | ⚠️ Seasonal Only |
| Peaked | Declining | Any | Any | ❌ AVOID |
| Any | Declining | Low | High | ❌ AVOID |

---

*This reference guide is designed to help AI agents interpret Exploding Topics data and make informed decisions about PDF product opportunities.*

**File Location:** `assets/exploding_topics_reference.md`  
**Usage:** Reference this guide when analyzing trends.csv exports from Exploding Topics
