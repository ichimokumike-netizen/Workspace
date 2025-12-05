# Legal & Ethical Web Scraping Protocol

**Status:** MANDATORY - Must be followed for ALL scraping operations
**Created:** 2025-11-30
**Priority:** CRITICAL

---

## CORE PRINCIPLE

**NEVER do anything that could:**
- Get domains blacklisted
- Get IP addresses blocked
- Violate Terms of Service
- Trigger rate limiting
- Cause legal issues
- Harm website performance

---

## Mandatory Pre-Scraping Checklist

Before ANY scraping operation, you MUST:

### 1. Check robots.txt
```bash
# Always check first
curl https://example.com/robots.txt
```

**Rules:**
- If robots.txt says "Disallow: /", DON'T SCRAPE
- Respect all User-agent directives
- Follow Crawl-delay requirements
- Honor specific path restrictions

### 2. Review Terms of Service
- Read the website's ToS
- Look for explicit scraping prohibitions
- Check if API is available instead
- Verify data usage rights

### 3. Check for API Access
**ALWAYS prefer official APIs over scraping**
- Most sites have APIs (even if limited)
- APIs are legal, blessed, rate-limited properly
- Often free tiers available
- No risk of being blocked

---

## Respectful Scraping Rules

### Rate Limiting (MANDATORY)
```python
# MINIMUM delays between requests
time.sleep(2)  # 2 seconds minimum
time.sleep(random.uniform(2, 5))  # Even better - randomized

# For production scraping:
time.sleep(random.uniform(5, 10))  # 5-10 seconds
```

**Absolute Limits:**
- NEVER more than 1 request per second
- NEVER more than 100 requests per hour from single IP
- NEVER scrape same site concurrently (parallel requests)
- ALWAYS use exponential backoff on errors

### User Agent (MANDATORY)
```python
headers = {
    'User-Agent': 'Your-Project-Name/1.0 (contact@youremail.com)',
    # NEVER impersonate real browsers without permission
    # BE TRANSPARENT about who you are
}
```

### IP Rotation & Proxies
**When scraping at scale:**
- Use residential proxies (not data center)
- Rotate IPs intelligently
- Use reputable proxy services (Bright Data, Oxylabs)
- NEVER use free/sketchy proxies
- Consider scraping APIs (ScraperAPI, Apify) instead

---

## What NOT to Scrape

### Prohibited Content
- Personal data (GDPR/CCPA violation)
- Copyrighted content (images, articles)
- Paywalled content
- Login-required data (without permission)
- Financial/health data (HIPAA, PCI-DSS)
- Children's data (COPPA violation)

### Sites That Explicitly Block Scraping
- LinkedIn (aggressive anti-scraping)
- Facebook (ToS violation)
- Instagram (ToS violation)
- Twitter (use API only)
- Amazon (use API instead)
- Google (use API instead)

**If a site actively fights scrapers → DON'T SCRAPE IT**

---

## Legal Alternatives to Scraping

### 1. Use Official APIs
- Psychology Today: Check for API
- Yelp: Has official API
- Google: Multiple APIs (Maps, Places, etc.)
- Most directories: Have APIs

### 2. Use Scraping-as-a-Service
**Legal, compliant services:**
- Apify (marketplace of pre-built scrapers)
- ScraperAPI (handles proxies, rate limiting)
- Bright Data (enterprise-grade)
- Outscraper (what we tried to use)

**Benefits:**
- They handle legal compliance
- Managed rate limiting
- No IP blocking risk
- Professional infrastructure

### 3. Partner/License Data
- Buy data from providers
- Partner with data aggregators
- License datasets legally
- Use public datasets

### 4. Manual Collection (for small datasets)
- If it's <100 records, just collect manually
- Screenshot and transcribe
- Use browser automation (Playwright) carefully
- Stay within ToS

---

## Our Approved Scraping Approach

### For Directory Business:

**What We CAN Do:**
1. **Public directory listings** (publicly accessible data)
2. **Business contact info** (publicly listed)
3. **Profile pages** that are:
   - Publicly accessible (no login)
   - Not behind paywall
   - Allowed by robots.txt
   - Scraped respectfully (slow rate)

**What We MUST Do:**
1. Check robots.txt FIRST
2. Use 5-10 second delays
3. Rotate user agents responsibly
4. Cache aggressively (don't re-scrape)
5. Monitor for 429/403 errors (stop immediately)
6. Use headless browsers when needed (Playwright)
7. Respect server resources

**What We WON'T Do:**
- Scrape login-required content
- Ignore rate limits
- Bypass CAPTCHAs
- Impersonate users
- Scrape personal messages/DMs
- Harvest email addresses for spam

---

## Psychology Today Specific Rules

**Status:** ALLOWED (with conditions)

**Evidence:**
- Public directory of therapists
- No login required
- Business listings (not personal data)
- Contact info is publicly displayed
- No robots.txt restriction on profile pages

**Requirements:**
- 5+ second delays between requests
- Max 100 profiles per day per IP
- Cache results (don't re-scrape)
- Use respectful user agent
- Stop if blocked (429/403)

**Better Alternative:**
- Check if Psychology Today has API
- Contact them for data partnership
- Use Apify's Psychology Today scraper (if exists)

---

## Error Handling & Blocking

### If You Get Blocked:

**Immediate Actions:**
1. STOP scraping immediately
2. Wait 24 hours before retry
3. Review what went wrong
4. Implement stricter rate limiting
5. Consider API instead

**Never:**
- Try to bypass the block
- Change IP and continue
- Use CAPTCHA solvers
- Complain to the website

### HTTP Status Codes

```python
# How to handle responses:

200: OK, proceed
429: Rate limited - STOP, wait exponentially
403: Forbidden - STOP, check robots.txt
503: Server overloaded - STOP, wait longer
```

---

## Legal Frameworks We Follow

### 1. Computer Fraud and Abuse Act (CFAA)
- Don't access without authorization
- Don't exceed authorized access
- Don't bypass security measures

### 2. GDPR (EU)
- Don't scrape personal data of EU citizens
- If you do, have legal basis
- Allow data deletion requests
- Maintain privacy policy

### 3. CCPA (California)
- Similar to GDPR for California
- Disclosure requirements
- Opt-out mechanisms

### 4. Terms of Service
- Read and follow ToS
- If ToS prohibits scraping, DON'T SCRAPE
- Use API if available

---

## Approved Scraping Tools

### ALLOWED:
- Requests (with rate limiting)
- BeautifulSoup (parsing only)
- Playwright (headless browser, respectful)
- Scrapy (with rate limit middleware)
- Official APIs

### USE WITH CAUTION:
- Selenium (resource-heavy, obvious)
- Puppeteer (headless Chrome)

### NEVER USE:
- CAPTCHA solvers
- Login automation (without permission)
- Credential stuffing tools
- Tools designed to evade detection

---

## Monitoring & Compliance

### Before Every Scraping Run:

```python
def pre_scrape_checklist(url):
    """
    MANDATORY checks before scraping
    """
    # 1. Check robots.txt
    robots_url = f"{url}/robots.txt"
    # Parse and verify allowed

    # 2. Set up rate limiting
    min_delay = 5  # seconds

    # 3. Set respectful headers
    headers = {
        'User-Agent': 'DirectoryBot/1.0 (contact@example.com)'
    }

    # 4. Set up error handling
    max_retries = 3
    backoff = [5, 15, 30]  # exponential

    # 5. Log everything
    # Track all requests for audit trail

    return True
```

### During Scraping:
- Log all requests
- Monitor error rates
- Track response times
- Watch for rate limit warnings

### After Scraping:
- Verify data quality
- Check for blocks/errors
- Update rate limits if needed
- Cache results

---

## Emergency Stop Conditions

**IMMEDIATELY STOP if:**
1. Multiple 429/403 errors
2. CAPTCHA appears
3. IP gets blocked
4. Server errors (500+)
5. Legal notice received
6. ToS violation discovered

---

## Alternative Revenue Strategies (No Scraping)

If scraping is too risky for a vertical:

### 1. Manual Data Collection
- Hire VAs on Upwork ($3-5/hour)
- 10 VAs × 20 entries/hour = 200 entries/hour
- Fully legal, no blocking risk

### 2. User-Generated Content
- Let businesses add themselves
- Community-driven directory
- Incentivize contributions

### 3. Licensed Data
- Buy data from aggregators
- Partner with existing directories
- White-label solutions

### 4. API-Only Approaches
- Only use official APIs
- Pay for data access
- Slower but zero risk

---

## Summary: The Safe Way Forward

### For Directory Business:

**Phase 1: Prove Concept (Manual)**
- Collect 25-50 entries manually per city
- Validate business model
- No scraping risk

**Phase 2: Scale Smart (API/Service)**
- Use Apify/ScraperAPI for collection
- They handle compliance
- Pay per use
- Zero blocking risk

**Phase 3: Partner (Data Licensing)**
- Partner with data providers
- License existing datasets
- White-label solutions
- Fully legal

**We NEVER:**
- Aggressively scrape
- Ignore rate limits
- Bypass protections
- Risk IP blacklisting

---

## This Directive is LAW

Every agent, every script, every automation MUST:
1. Check this directive first
2. Follow these rules strictly
3. When in doubt, DON'T SCRAPE
4. Ask user for permission if unclear

**Violation = System Shutdown**

No revenue is worth getting blacklisted, sued, or prosecuted.

---

**All scraping scripts MUST import and check this directive before executing.**
