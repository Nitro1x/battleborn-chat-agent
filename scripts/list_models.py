#!/usr/bin/env python3
"""
List available Google Generative AI models and their supported methods.
Usage:
  - Set GOOGLE_API_KEY in environment and run: python3 scripts/list_models.py
  - Or pass the key as an argument: python3 scripts/list_models.py --key YOUR_KEY
"""
import os
import argparse

try:
    import google.generativeai as genai
except Exception as e:
    print("ERROR: google.generativeai not installed:", e)
    raise SystemExit(1)

parser = argparse.ArgumentParser()
parser.add_argument("--key", help="Google API key (optional)")
args = parser.parse_args()

api_key = args.key or os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("No API key provided. Set GOOGLE_API_KEY env var or use --key.")
    raise SystemExit(1)

try:
    genai.configure(api_key=api_key)
    models = genai.list_models()
    if not models:
        print("No models returned by the API.")
        raise SystemExit(0)
    for m in models:
        name = getattr(m, "name", None)
        supported = getattr(m, "supported_generation_methods", None)
        print("NAME:", name)
        print("SUPPORTED:", supported)
        print("---")
except Exception as e:
    print("Error while listing models:", e)
    raise SystemExit(1)
