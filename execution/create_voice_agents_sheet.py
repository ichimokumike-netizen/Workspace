"""
Create Google Sheet with AI Voice Agent Platform Comparison
This script creates a comprehensive comparison sheet of AI voice agent platforms
"""

import os
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_voice_agents_sheet():
    """Create a Google Sheet with voice agent platform comparison data"""

    # Voice agent platforms data
    platforms_data = [
        {
            "Platform": "Vapi AI",
            "URL": "https://vapi.ai",
            "API": "Yes",
            "Pricing": "$0.05/min base + $0.15-$0.50/min total (includes STT, TTS, LLM, telephony)",
            "Monthly Plans": "Agency: $500/mo, Startup: $1,000/mo, Enterprise: Custom",
            "Key Features": "Ultra-low latency, flexible integration, developer-focused, requires third-party services",
            "Best For": "Developers, tech companies with engineering resources",
            "Latency": "~1 second",
            "Compliance": "HIPAA/SOC 2 ($1,000/mo add-on)",
            "Free Trial": "$10 credit (30-75 mins)",
            "White Label": "Unknown",
            "Notes": "Complex pricing with 5+ invoices/month, $40K-$70K annual budget for enterprise"
        },
        {
            "Platform": "Retell AI",
            "URL": "https://www.retellai.com",
            "API": "Yes",
            "Pricing": "Usage-based (not publicly disclosed)",
            "Monthly Plans": "Contact for pricing",
            "Key Features": "800ms response time, turn-taking model, warm transfers, appointment scheduling, multilingual (18+ languages)",
            "Best For": "Contractors, service businesses, contact centers",
            "Latency": "~800ms",
            "Compliance": "SOC 2 Type 1&2, HIPAA, GDPR",
            "Free Trial": "Available",
            "White Label": "Yes (integration capabilities)",
            "Notes": "Excellent for contractor use case - scheduling, routing, 24/7 availability, integrates with Cal.com, Salesforce, HubSpot"
        },
        {
            "Platform": "Bland AI",
            "URL": "https://www.bland.ai",
            "API": "Yes",
            "Pricing": "$0.09/min + $0.015 outbound attempt fee + $0.02/SMS + $0.025/min transfers",
            "Monthly Plans": "Free tier, up to $499/mo, Enterprise custom",
            "Key Features": "Voice cloning, webhook triggers, mid-call API access, multilingual, workflow automation",
            "Best For": "Large tech teams, high-volume enterprise",
            "Latency": "~1-2 seconds",
            "Compliance": "Enterprise-grade",
            "Free Trial": "Free plan available",
            "White Label": "Limited",
            "Notes": "True cost $200-$300/mo with add-ons (voice cloning, GPT-4, transcription). NOT ideal for small businesses or resellers"
        },
        {
            "Platform": "Synthflow AI",
            "URL": "https://synthflow.ai",
            "API": "Yes",
            "Pricing": "$0.08/min (all-inclusive: voice, testing, multilingual, LLM)",
            "Monthly Plans": "Volume discounts: $0.12/min at 20K mins, $0.07/min at 400K+ mins",
            "Key Features": "No-code platform, 130+ integrations (Zapier, Salesforce, HubSpot), appointment scheduling, lead qualification",
            "Best For": "Agencies, contractors, small-medium businesses",
            "Latency": "~1-2 seconds",
            "Compliance": "Enterprise-grade",
            "Free Trial": "Available",
            "White Label": "Yes (Agency program)",
            "Notes": "Best no-code option, $15K/year minimum budget, excellent for contractor answering service"
        },
        {
            "Platform": "My AI Front Desk",
            "URL": "https://www.myaifrontdesk.com",
            "API": "Limited",
            "Pricing": "$79/month flat rate",
            "Monthly Plans": "$79/mo (all-inclusive)",
            "Key Features": "5-minute setup, appointment scheduling, Q&A automation, calendar integration",
            "Best For": "Small businesses, salons, clinics, contractors",
            "Latency": "Standard",
            "Compliance": "Standard business",
            "Free Trial": "Yes",
            "White Label": "No",
            "Notes": "BEST VALUE for simple contractor use case - fixed $79/mo pricing, ultra-simple setup"
        },
        {
            "Platform": "Goodcall",
            "URL": "https://www.goodcall.com",
            "API": "Limited",
            "Pricing": "Subscription-based (pricing not public)",
            "Monthly Plans": "Contact for pricing",
            "Key Features": "Skills/flows/documents system, Google hackathon origin, backed by top investors",
            "Best For": "Service businesses",
            "Latency": "Standard",
            "Compliance": "Standard",
            "Free Trial": "Available",
            "White Label": "Unknown",
            "Notes": "Good for service CX, custom response control"
        },
        {
            "Platform": "ElevenLabs",
            "URL": "https://elevenlabs.io",
            "API": "Yes",
            "Pricing": "TTS pricing varies by plan, Conversational AI separate",
            "Monthly Plans": "Multiple tiers from free to enterprise",
            "Key Features": "Ultra-realistic voice synthesis, voice cloning, emotional tone control, 29+ languages, 400ms API response",
            "Best For": "Premium voice quality needs, content creators, enterprises",
            "Latency": "~400ms (TTS), 1-3s (Conversational AI)",
            "Compliance": "Enterprise",
            "Free Trial": "Yes",
            "White Label": "Via API integration",
            "Notes": "Industry-leading voice quality, owns TTS/STT models in-house, can be integrated with other platforms like Voiceflow"
        },
        {
            "Platform": "Voiceflow",
            "URL": "https://www.voiceflow.com",
            "API": "Yes",
            "Pricing": "Freemium model, paid plans available",
            "Monthly Plans": "Free, Pro, Team, Enterprise (custom)",
            "Key Features": "Visual conversation builder, collaborative design platform, prototyping, no-code/low-code",
            "Best For": "Product teams, designers, rapid prototyping",
            "Latency": "1-3 seconds (depends on integrations)",
            "Compliance": "Enterprise options",
            "Free Trial": "Free tier available",
            "White Label": "Via custom deployment",
            "Notes": "Best for building/testing conversational interfaces before deployment, integrates with ElevenLabs for voice"
        },
        {
            "Platform": "Smith.ai",
            "URL": "https://smith.ai",
            "API": "No (service-based)",
            "Pricing": "Plans from $240/mo",
            "Monthly Plans": "$240/mo - $900+/mo",
            "Key Features": "AI + live North American receptionists, call answering, intake, scheduling",
            "Best For": "Small businesses wanting human backup",
            "Latency": "Human-assisted",
            "Compliance": "Business standard",
            "Free Trial": "14-day trial",
            "White Label": "No",
            "Notes": "Hybrid AI + human model since 2015, NOT pure API - managed service"
        },
        {
            "Platform": "Upfirst",
            "URL": "https://upfirst.ai",
            "API": "Limited",
            "Pricing": "Starting at $14/month",
            "Monthly Plans": "Tiered pricing from $14/mo",
            "Key Features": "Google Calendar integration, call summaries, low latency, natural AI",
            "Best For": "Budget-conscious small businesses",
            "Latency": "Low",
            "Compliance": "Standard",
            "Free Trial": "Yes",
            "White Label": "No",
            "Notes": "Most affordable option, good for basic appointment setting"
        },
        {
            "Platform": "GoTo Connect",
            "URL": "https://www.goto.com/connect",
            "API": "Limited",
            "Pricing": "Part of GoTo Connect subscription",
            "Monthly Plans": "Contact for pricing",
            "Key Features": "Call routing, real-time reporting, 10+ languages, customizable tone, CRM integration",
            "Best For": "SMBs needing full business phone system",
            "Latency": "Standard",
            "Compliance": "Enterprise",
            "Free Trial": "Yes",
            "White Label": "No",
            "Notes": "Part of broader business communication platform, not standalone API"
        },
        {
            "Platform": "CloudTalk",
            "URL": "https://www.cloudtalk.io",
            "API": "Yes (business phone API)",
            "Pricing": "Call center pricing model",
            "Monthly Plans": "Starter: $25/user/mo, Essential: $30/user/mo, Expert: $50/user/mo",
            "Key Features": "Customizable AI receptionist, smart routing, CRM integration, local presence",
            "Best For": "SMBs with existing call center needs",
            "Latency": "Standard",
            "Compliance": "GDPR, enterprise",
            "Free Trial": "14-day trial",
            "White Label": "Limited",
            "Notes": "Business phone platform with AI features, not pure voice AI"
        }
    ]

    try:
        # Try to load credentials
        creds = None
        token_path = 'token.json'
        creds_path = 'credentials.json'

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/spreadsheets'])
        elif os.path.exists(creds_path):
            creds = service_account.Credentials.from_service_account_file(
                creds_path, scopes=['https://www.googleapis.com/auth/spreadsheets'])

        if not creds:
            print("ERROR: No Google credentials found.")
            print("Please ensure you have either:")
            print("  1. token.json (OAuth token) or")
            print("  2. credentials.json (Service account credentials)")
            print("\nYou can create these at: https://console.cloud.google.com/")
            return None

        service = build('sheets', 'v4', credentials=creds)

        # Create a new spreadsheet
        spreadsheet = {
            'properties': {
                'title': 'AI Voice Agent Platforms Comparison'
            }
        }

        spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId,spreadsheetUrl').execute()
        spreadsheet_id = spreadsheet.get('spreadsheetId')
        spreadsheet_url = spreadsheet.get('spreadsheetUrl')

        print(f"Created spreadsheet: {spreadsheet_url}")

        # Prepare the header row
        headers = [
            "Platform",
            "URL",
            "API",
            "Pricing",
            "Monthly Plans",
            "Key Features",
            "Best For",
            "Latency",
            "Compliance",
            "Free Trial",
            "White Label",
            "Notes"
        ]

        # Prepare data rows
        rows = [headers]
        for platform in platforms_data:
            row = [platform.get(header, "") for header in headers]
            rows.append(row)

        # Write data to sheet
        body = {
            'values': rows
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='A1',
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"Updated {result.get('updatedCells')} cells")

        # Format the sheet (make header row bold, freeze it)
        requests = [
            {
                'repeatCell': {
                    'range': {
                        'sheetId': 0,
                        'startRowIndex': 0,
                        'endRowIndex': 1
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.6},
                            'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },
            {
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': 0,
                        'gridProperties': {'frozenRowCount': 1}
                    },
                    'fields': 'gridProperties.frozenRowCount'
                }
            },
            {
                'autoResizeDimensions': {
                    'dimensions': {
                        'sheetId': 0,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': len(headers)
                    }
                }
            }
        ]

        body = {'requests': requests}
        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

        print("\nFormatting applied successfully!")
        print(f"\n✅ Google Sheet created: {spreadsheet_url}")

        return spreadsheet_url

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    print("Creating AI Voice Agent Platforms Comparison Sheet...\n")
    url = create_voice_agents_sheet()
    if url:
        print(f"\n🎉 Success! Open your sheet here: {url}")
    else:
        print("\n❌ Failed to create sheet. Check credentials and try again.")
