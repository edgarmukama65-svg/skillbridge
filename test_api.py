# test_api.py - Test Google Gemini API

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("=" * 50)
print("TESTING GOOGLE GEMINI API")
print("=" * 50)

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: No API key found in .env file!")
    print("   Please add: GEMINI_API_KEY=your_key_here")
else:
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        # Configure API
        genai.configure(api_key=api_key)
        
        # List available models first
        print("📋 Checking available models...")
        for m in genai.list_models():
            print(f"  - {m.name}")
        
        # Try the newer model name
        print("\n🤖 Calling Gemini API with model: gemini-1.5-flash...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Say 'Hello, API is working correctly!'")
        
        print("✅ SUCCESS!")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")