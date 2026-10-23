# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly',
    'https://www.googleapis.com/auth/webmasters.readonly',
]

def get_token():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    req = google.auth.transport.requests.Request()
    creds.refresh(req)
    return creds.token

def test_search_console(token):
    print("\n--- [1] Checking Google Search Console Sites ---")
    url = "https://www.googleapis.com/webmasters/v3/sites"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Search Console Sites found:")
            entries = data.get('siteEntry', [])
            for e in entries:
                print(f"  - {e.get('siteUrl')} (Permission: {e.get('permissionLevel')})")
            return entries
    except urllib.error.HTTPError as e:
        print(f"Search Console Error {e.code}: {e.read().decode('utf-8')}")
        return []

def test_ga4(token):
    print("\n--- [2] Checking GA4 Account Summaries ---")
    url = "https://analyticsadmin.googleapis.com/v1beta/accountSummaries"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("GA4 Account Summaries found:")
            summaries = data.get('accountSummaries', [])
            for acc in summaries:
                acc_name = acc.get('displayName')
                print(f"Account: {acc_name}")
                for prop in acc.get('propertySummaries', []):
                    prop_id = prop.get('property').replace('properties/', '')
                    print(f"  - Property: {prop.get('displayName')} (Property ID: {prop_id})")
            return summaries
    except urllib.error.HTTPError as e:
        print(f"GA4 Admin API Error {e.code}: {e.read().decode('utf-8')}")
        return []

if __name__ == '__main__':
    print(f"Authenticating with {KEY_FILE}...")
    token = get_token()
    print("Authentication successful! Token obtained.")
    sc_sites = test_search_console(token)
    ga_summaries = test_ga4(token)
