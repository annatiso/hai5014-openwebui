#!/usr/bin/env python3
import requests
import json
import sys

def get_shuttle_bus_location():
    url = "http://route.hellobus.co.kr:8787/pub/routeView/skku/getSkkuLoc.aspx"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Return the JSON response
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {str(e)}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decoding error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

if __name__ == "__main__":
    result = get_shuttle_bus_location()
    print(json.dumps(result, indent=4, ensure_ascii=False))