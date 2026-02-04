import sys
import traceback

print("Starting direct model test...")
try:
    from backend.model import analyze_text
    print("Import successful. Calling analyze_text...")
    result = analyze_text("I feel deep darkness.")
    print("Result:", result)
except Exception:
    traceback.print_exc()
