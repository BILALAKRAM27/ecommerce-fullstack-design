#!/usr/bin/env python3
"""
Test script to verify export functionality
"""
import requests
import json

def test_export_functionality():
    """Test the export functionality"""
    
    # Test URL
    base_url = "http://127.0.0.1:8000"
    
    # Test data
    test_data = {
        "export_type": "products",
        "start_date": "",
        "end_date": "",
        "format": "csv"
    }
    
    print("Testing export functionality...")
    print(f"URL: {base_url}/export-data/")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    
    try:
        # Make the request
        response = requests.post(
            f"{base_url}/export-data/",
            json=test_data,
            headers={
                "Content-Type": "application/json",
                "X-CSRFToken": "test-token"  # This will be handled by Django
            }
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Export request successful!")
            print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")
            print(f"Content-Length: {len(response.content)} bytes")
            
            # Save the response to a file for inspection
            with open("test_export_output.csv", "wb") as f:
                f.write(response.content)
            print("✅ Export file saved as 'test_export_output.csv'")
            
        else:
            print(f"❌ Export request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_export_functionality() 