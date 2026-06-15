import os
import requests
import json
import argparse
from urllib.parse import quote_plus

API_KEY = "AIzaSyCgfjc35Ah1eCVyF8lPLNmpBhX26i5MQrs"
CSE_ID = "c369c352f440840cb"

def google_dork(query, num_results=10):
    """
    Perform a Google Custom Search using the provided Dork query.
    """
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CSE_ID}&q={quote_plus(query)}&num={num_results}"
    
    print(f"[*] Executing Dork: {query}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("items", [])
        
        if not results:
            print("[-] No results found.")
            return []
            
        print(f"[+] Found {len(results)} results.\n")
        
        parsed_results = []
        for i, item in enumerate(results, 1):
            title = item.get("title", "")
            link = item.get("link", "")
            snippet = item.get("snippet", "").replace('\n', ' ')
            
            print(f"{i}. {title}")
            print(f"   URL: {link}")
            print(f"   Snippet: {snippet}\n")
            
            parsed_results.append({
                "title": title,
                "link": link,
                "snippet": snippet
            })
            
        return parsed_results

    except requests.exceptions.RequestException as e:
        print(f"[!] HTTP Error during search: {e}")
        if response.text:
            print(f"[!] Response detail: {response.text}")
        return []
    except Exception as e:
        print(f"[!] An error occurred: {e}")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google CSE Dorking Tool")
    parser.add_argument("-q", "--query", required=True, help="Google Dork query to execute")
    parser.add_argument("-n", "--num", type=int, default=10, help="Number of results to fetch (max 10 per request)")
    
    args = parser.parse_args()
    
    # max 10 per API request for CSE
    num = min(args.num, 10) 
    
    google_dork(args.query, num)
