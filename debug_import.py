
import sys
import os

print("CWD:", os.getcwd())
print("PYTHONPATH:", os.environ.get("PYTHONPATH"))

try:
    print("Importing SafetyManager...")
    from spine.chapters.admin.safety import SafetyManager
    print("SafetyManager Imported.")
except Exception as e:
    print("Failed to import SafetyManager:", e)

try:
    print("Importing Valve...")
    from spine.chapters.action.valve import Valve
    print("Valve Imported.")
except Exception as e:
    print("Failed to import Valve:", e)
    import traceback
    traceback.print_exc()
