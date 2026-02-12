
import sys
import subprocess

print("sys.executable:", sys.executable)
try:
    import sqlmodel
    print("sqlmodel imported successfully")
except ImportError:
    print("sqlmodel NOT FOUND")
    sys.exit(1)
