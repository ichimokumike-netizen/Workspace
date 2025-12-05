# Google Places API Setup Guide

**Purpose:** Get accurate business data from Google Maps legally and reliably
**Cost:** $0-200/month (depending on volume)
**Time to setup:** 5 minutes

---

## Why Google Places API Instead of Outscraper?

**Problems with Outscraper:**
- Tasks consistently timeout (status: unknown)
- Unreliable for production use
- Can't debug what's wrong

**Benefits of Google Places API:**
- Official Google API (100% legal, supported)
- Reliable and fast (sub-second responses)
- Better data quality (direct from Google)
- Generous free tier (first $200/month free)
- Easy to use

---

## Cost Analysis

**Google Places API Pricing:**
- Text Search: $32 per 1000 requests
- Place Details: $17 per 1000 requests
- Total: ~$49 per 1000 businesses

**With $200/month free credit:**
- ~4,000 businesses FREE per month
- That's 40 directories with 100 businesses each
- More than enough to start

**After free tier:**
- Still only $49 per 1000 businesses
- For 10,000 businesses: $490/month
- But you'd be making $200/business/month = $2M/month revenue
- API cost is 0.025% of revenue

---

## Setup Steps

### 1. Enable Google Places API (2 minutes)

1. Go to: https://console.cloud.google.com/apis/library/places-backend.googleapis.com
2. Click "Enable"
3. Go to: https://console.cloud.google.com/apis/credentials
4. Click "Create Credentials" > "API Key"
5. Copy the API key
6. Add to `.env`:
   ```
   GOOGLE_PLACES_API_KEY=AIzaSy...
   ```

### 2. Run the Scraper (Instant)

```bash
python execution/scrape_google_places.py "therapist accepting medicaid" "Philadelphia, PA"
```

That's it! You'll get:
- Business name
- Full address (accurate)
- Phone number
- Website
- Rating & reviews
- Business hours
- Latitude/longitude
- Google Maps URL

All uploaded to Google Sheets automatically.

---

## Example Output

```json
{
  "name": "Philadelphia Mental Health Services",
  "address": "1234 Market St, Philadelphia, PA 19107",
  "phone": "(215) 555-1234",
  "website": "https://example.com",
  "rating": 4.5,
  "reviews": 127,
  "hours": "Mon-Fri: 9am-5pm",
  "maps_url": "https://maps.google.com/?cid=12345",
  "lat": 39.9526,
  "lng": -75.1652
}
```

---

## Why This is Better Than What We Had

**Psychology Today scraper:**
- Violates robots.txt (can't use)
- Inaccurate locations (suburbs included)
- Missing contact info
- No emails
- Limited to one source

**Outscraper:**
- Unreliable (timeouts)
- Can't debug
- Expensive per use
- No idea what's wrong

**Google Places API:**
- Works every time
- Fast (< 1 second per query)
- Accurate data direct from Google
- Official and legal
- Free tier generous
- Can scale to millions of businesses

---

## Next Steps

1. **Setup API (5 min):** Enable Places API, get key
2. **Test it (1 min):** Run script for Philadelphia therapists
3. **Scale it (ongoing):** Use for all 500 directories

This is the foundation for the entire directory business.

---

## Alternative: Just Do It Manually

If you don't want to set up the API, here's the manual approach:

1. Go to Google Maps
2. Search "therapist accepting medicaid Philadelphia PA"
3. Export first 20 results manually
4. Put in Google Sheet
5. Call them to sell featured listings

This gets you first revenue TODAY without any API setup.

**Revenue potential:** 20 therapists × 10% conversion = 2 customers × $200/month = $400/month recurring

**Time investment:** 2 hours to collect data + 2 hours to call them = first revenue in 4 hours

---

Choose your path:
- **Fast to revenue:** Manual collection (4 hours to first customer)
- **Scalable:** Google Places API (5 min setup, unlimited scale)
- **Outscraper:** Don't use (unreliable for us)
